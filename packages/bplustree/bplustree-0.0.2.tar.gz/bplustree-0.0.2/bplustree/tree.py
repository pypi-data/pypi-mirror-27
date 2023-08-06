from functools import partial
from logging import getLogger
from typing import Optional, Union, Iterator

from . import utils
from .const import TreeConf
from .entry import Record, Reference
from .memory import FileMemory
from .node import Node, LonelyRootNode, RootNode, InternalNode, LeafNode
from .serializer import Serializer, IntSerializer


logger = getLogger(__name__)


class BPlusTree:

    __slots__ = ['_filename', '_tree_conf', '_mem', '_root_node_page',
                 '_is_open', 'LonelyRootNode', 'RootNode', 'InternalNode',
                 'LeafNode', 'Record', 'Reference']

    # ######################### Public API ################################

    def __init__(self, filename: str, page_size: int= 4096, order: int=4,
                 key_size: int=16, value_size: int=16, cache_size: int=512,
                 serializer: Optional[Serializer]=None):
        self._filename = filename
        self._tree_conf = TreeConf(
            page_size, order, key_size, value_size,
            serializer or IntSerializer()
        )
        self._create_partials()
        self._mem = FileMemory(filename, self._tree_conf,
                               cache_size=cache_size)
        try:
            metadata = self._mem.get_metadata()
        except ValueError:
            self._initialize_empty_tree()
        else:
            self._root_node_page, self._tree_conf = metadata
        self._is_open = True

    def close(self):
        with self._mem.write_transaction:
            if not self._is_open:
                logger.info('Tree is already closed')
                return

            self._mem.close()
            self._is_open = False

    def __enter__(self):
        return self

    def __exit__(self, exc_type, exc_val, exc_tb):
        self.close()

    def checkpoint(self):
        with self._mem.write_transaction:
            self._mem.perform_checkpoint(reopen_wal=True)

    def insert(self, key, value: bytes, replace=False):
        """Insert a value in the tree.

        :param key: The key at which the value will be recorded, must be of the
                    same type used by the Serializer
        :param value: The value to record in bytes
        :param replace: If True, already existing value will be overridden,
                        otherwise a ValueError is raised.
        """
        if not isinstance(value, bytes):
            ValueError('Values must be bytes objects')

        with self._mem.write_transaction:
            node = self._search_in_tree(key, self._root_node)

            # Check if an entry with the key already exist
            try:
                existing_entry = node.get_entry(key)
            except ValueError:
                pass
            else:
                if not replace:
                    raise ValueError('Key {} already exists'.format(key))

                existing_entry.value = value
                self._mem.set_node(node)
                return

            if node.can_add_entry:
                node.insert_entry(self.Record(key, value))
                self._mem.set_node(node)
            else:
                node.insert_entry(self.Record(key, value))
                self._split_leaf(node)

    def get(self, key, default=None) -> bytes:
        with self._mem.read_transaction:
            node = self._search_in_tree(key, self._root_node)
            try:
                record = node.get_entry(key)
            except ValueError:
                return default
            else:
                assert isinstance(record.value, bytes)
                return record.value

    def __contains__(self, item):
        with self._mem.read_transaction:
            o = object()
            return False if self.get(item, default=o) is o else True

    def __setitem__(self, key, value):
        self.insert(key, value, replace=True)

    def __getitem__(self, item):
        with self._mem.read_transaction:

            if isinstance(item, slice):
                # Returning a dict is the most sensible thing to do
                # as a method cannot return a sometimes a generator
                # and sometimes a normal value
                rv = dict()
                for record in self._iter_slice(item):
                    rv[record.key] = record.value
                return rv

            else:
                rv = self.get(item)
                if rv is None:
                    raise KeyError(item)
                return rv

    def __len__(self):
        with self._mem.read_transaction:
            node = self._left_record_node
            rv = 0
            while True:
                rv += len(node.entries)
                if not node.next_page:
                    return rv
                node = self._mem.get_node(node.next_page)

    def __length_hint__(self):
        with self._mem.read_transaction:
            node = self._root_node
            if isinstance(node, LonelyRootNode):
                # Assume that the lonely root node is half full
                return node.max_children // 2
            # Assume that there are no holes in pages
            last_page = self._mem.last_page
            # Assume that 70% of nodes in a tree carry values
            num_leaf_nodes = int(last_page * 0.70)
            # Assume that every leaf node is half full
            num_records_per_leaf_node = int(
                (node.max_children + node.min_children) / 2
            )
            return num_leaf_nodes * num_records_per_leaf_node

    def __iter__(self, slice_: Optional[slice]=None):
        if not slice_:
            slice_ = slice(None)
        with self._mem.read_transaction:
            for record in self._iter_slice(slice_):
                yield record.key

    keys = __iter__

    def items(self, slice_: Optional[slice]=None) -> Iterator[tuple]:
        if not slice_:
            slice_ = slice(None)
        with self._mem.read_transaction:
            for record in self._iter_slice(slice_):
                yield record.key, record.value

    def values(self, slice_: Optional[slice]=None) -> Iterator[bytes]:
        if not slice_:
            slice_ = slice(None)
        with self._mem.read_transaction:
            for record in self._iter_slice(slice_):
                yield record.value

    def __bool__(self):
        with self._mem.read_transaction:
            for _ in self:
                return True
            return False

    def __repr__(self):
        return '<BPlusTree: {} {}>'.format(self._filename, self._tree_conf)

    # ####################### Implementation ##############################

    def _initialize_empty_tree(self):
        self._root_node_page = self._mem.next_available_page
        with self._mem.write_transaction:
            self._mem.set_node(self.LonelyRootNode(page=self._root_node_page))
        self._mem.set_metadata(self._root_node_page, self._tree_conf)

    def _create_partials(self):
        self.LonelyRootNode = partial(LonelyRootNode, self._tree_conf)
        self.RootNode = partial(RootNode, self._tree_conf)
        self.InternalNode = partial(InternalNode, self._tree_conf)
        self.LeafNode = partial(LeafNode, self._tree_conf)
        self.Record = partial(Record, self._tree_conf)
        self.Reference = partial(Reference, self._tree_conf)

    @property
    def _root_node(self) -> Union['LonelyRootNode', 'RootNode']:
        root_node = self._mem.get_node(self._root_node_page)
        assert isinstance(root_node, (LonelyRootNode, RootNode))
        return root_node

    @property
    def _left_record_node(self) -> Union['LonelyRootNode', 'LeafNode']:
        node = self._root_node
        while not isinstance(node, (LonelyRootNode, LeafNode)):
            node = self._mem.get_node(node.smallest_entry.before)
        return node

    def _iter_slice(self, slice_: slice) -> Iterator[Record]:
        if slice_.step is not None:
            raise ValueError('Cannot iterate with a custom step')

        if (slice_.start is not None and slice_.stop is not None and
                slice_.start >= slice_.stop):
            raise ValueError('Cannot iterate backwards')

        if slice_.start is None:
            node = self._left_record_node
        else:
            node = self._search_in_tree(slice_.start, self._root_node)

        while True:
            for entry in node.entries:
                if slice_.start is not None and entry.key < slice_.start:
                    continue

                if slice_.stop is not None and entry.key >= slice_.stop:
                    raise StopIteration()

                yield entry

            if node.next_page:
                node = self._mem.get_node(node.next_page)
            else:
                raise StopIteration()

    def _search_in_tree(self, key, node) -> 'Node':
        if isinstance(node, (LonelyRootNode, LeafNode)):
            return node

        page = None

        if key < node.smallest_key:
            page = node.smallest_entry.before

        elif node.biggest_key <= key:
            page = node.biggest_entry.after

        else:
            for ref_a, ref_b in utils.pairwise(node.entries):
                if ref_a.key <= key < ref_b.key:
                    page = ref_a.after
                    break

        assert page is not None

        child_node = self._mem.get_node(page)
        child_node.parent = node
        return self._search_in_tree(key, child_node)

    def _split_leaf(self, old_node: 'Node'):
        parent = old_node.parent
        new_node = self.LeafNode(page=self._mem.next_available_page,
                                 next_page=old_node.next_page)
        new_entries = old_node.split_entries()
        new_node.entries = new_entries
        ref = self.Reference(new_node.smallest_key,
                             old_node.page, new_node.page)

        if isinstance(old_node, LonelyRootNode):
            # Convert the LonelyRoot into a Leaf
            old_node = old_node.convert_to_leaf()
            self._create_new_root(ref)
        elif parent.can_add_entry:
            parent.insert_entry(ref)
            self._mem.set_node(parent)
        else:
            parent.insert_entry(ref)
            self._split_parent(parent)

        old_node.next_page = new_node.page

        self._mem.set_node(old_node)
        self._mem.set_node(new_node)

    def _split_parent(self, old_node: Node):
        parent = old_node.parent
        new_node = self.InternalNode(page=self._mem.next_available_page)
        new_entries = old_node.split_entries()
        new_node.entries = new_entries

        ref = new_node.pop_smallest()
        ref.before = old_node.page
        ref.after = new_node.page

        if isinstance(old_node, RootNode):
            # Convert the Root into an Internal
            old_node = old_node.convert_to_internal()
            self._create_new_root(ref)
        elif parent.can_add_entry:
            parent.insert_entry(ref)
            self._mem.set_node(parent)
        else:
            parent.insert_entry(ref)
            self._split_parent(parent)

        self._mem.set_node(old_node)
        self._mem.set_node(new_node)

    def _create_new_root(self, reference: Reference):
        new_root = self.RootNode(page=self._mem.next_available_page)
        new_root.insert_entry(reference)
        self._root_node_page = new_root.page
        self._mem.set_metadata(self._root_node_page, self._tree_conf)
        self._mem.set_node(new_root)
