from node import Node


(_ADD, _DELETE, _INSERT) = range(3)
(_ROOT, _DEPTH, _WIDTH) = range(3)


class MultipleRootError(Exception):
    pass


class Tree(object):
    """
    tree = Tree()
    tree.create_node("Harry", "harry")  # root node
    tree.create_node("Jane", "jane", parent="harry")
    tree.create_node("Bill", "bill", parent="harry")
    tree.create_node("Diane", "diane", parent="jane")
    tree.create_node("George", "george", parent="diane")
    tree.create_node("Mary", "mary", parent="diane")
    tree.create_node("Jill", "jill", parent="george")
    tree.create_node("Mark", "mark", parent="jane")

    tree.show()

    for node in tree.expand_tree(mode=_DEPTH):
        print tree[node].name

    for node in tree.expand_tree(filter=lambda x: x != 'diane', mode=_DEPTH):
        print tree[node].name

    sub_t = tree.subtree('diane')
        sub_t.show()

    print tree.is_branch('diane')

    new_tree = Tree()
    new_tree.create_node("n1", "1")  # root node
    new_tree.create_node("n2", "2", parent="1")
    new_tree.create_node("n3", "3", parent="1")
    tree.paste('jill', new_tree)
    tree.show()

    tree.remove_node('1')
    tree.show()

    tree.move_node('jill', 'harry')
    tree.show()

    for node in tree.rsearch('george', filter=lambda x: x != 'harry'):
        print node
    """
    def __init__(self):
        self.nodes = {}
        self.root = None


    def add_node(self, node, parent=None):
        """
        Add a new node to tree.
        The 'node' parameter refers to an instance of Class::Node
        """
        if parent is None:
            if self.root is not None:
                raise MultipleRootError
            else:
                self.root = node.identifier
        self.nodes.update({node.identifier : node})
        self.__update_fpointer(parent, node.identifier, _ADD)
        node.bpointer = parent


    def create_node(self, tag, identifier=None, parent=None):
        """
        Create a child node for the node indicated by the 'parent' parameter
        """
        node = Node(tag, identifier)
        self.add_node(node, parent)
        return node


    def expand_tree(self, nid=None, mode=_DEPTH, filter=None):
        # Python generator. Loosly based on an algorithm from 'Essential LISP' by
        # John R. Anderson, Albert T. Corbett, and Brian J. Reiser, page 239-241
        def real_true(pos):
            return True

        if nid is None:
            nid = self.root
        if filter is None:
            filter = real_true

        if filter(nid):
            yield nid
            queue = self[nid].fpointer
            while queue:
                if filter(queue[0]):
                    yield queue[0]
                    expansion = self[queue[0]].fpointer
                    if mode is _DEPTH:
                        queue = expansion + queue[1:]  # depth-first
                    elif mode is _WIDTH:
                        queue = queue[1:] + expansion  # width-first
                else:
                    queue = queue[1:]


    def get_node(self, nid):
        return self.nodes[nid]


    def is_branch(self, nid):
        """
        Return the following nodes of [nid]
        """
        return self[nid].fpointer


    def move_node(self, source, destination):
        """
        Move a node indicated by the 'source' parameter to the parent node
        indicated by the 'dest' parameter
        """
        parent = self[source].bpointer
        self.__update_fpointer(parent, source, _DELETE)
        self.__update_fpointer(destination, source, _ADD)
        self.__update_bpointer(source, destination)


    def paste(self, nid, new_tree):
        """
        Paste a new tree to the original one by linking the root
        of new tree to nid.
        """
        assert isinstance(new_tree, Tree)

        if set(new_tree.nodes) & set(self.nodes):
            raise ValueError('Duplicated nodes exists.')

        new_tree[new_tree.root].bpointer = nid
        self.__update_fpointer(nid, new_tree.root, _ADD)
        self.nodes.update(new_tree.nodes)


    def remove_node(self, identifier):
        """
        Remove a node indicated by 'identifier'. All the successors are removed, too.
        """
        parent = self[identifier].bpointer
        remove = []
        for id in self.expand_tree(identifier):
            # TODO: implementing this function as a recursive function:
            #       check if node has children
            #       true -> run remove_node with child_id
            #       no -> delete node
            remove.append(id)

        for id in remove:
            del(self.nodes[id])

        self.__update_fpointer(parent, identifier, _DELETE)


    def rsearch(self, nid, filter=None):
        """
        Search the tree from nid to the root along links reversedly.
        """

        def real_true(p):
            return True

        if filter is None:
            filter = real_true
        current = nid
        while current is not None:
            if filter(current):
                yield current
            current = self[current].bpointer


    def show(self, nid=None, level=_ROOT):
        """"
            Another implementation of printing tree using Stack
            Print tree structure in hierarchy style.
            For example:
                Root
                |___ C01
                |	 |___ C11
                |		  |___ C111
                |		  |___ C112
                |___ C02
                |___ C03
                |	 |___ C31
            A more elegant way to achieve this function using Stack structure,
            for constructing the Nodes Stack push and pop nodes with additional level info.
        """
        leading = ''
        lasting = '|___ '

        if nid is None:
            nid = self.root
        label = "{0}[{1}]".format(self[nid].tag, self[nid].identifier)

        queue = self[nid].fpointer

        if level == _ROOT:
            print(label)
        else:
            if level <= 1:
                leading += ('|' + ' ' * 4) * (level - 1)
            else:
                leading += ('|' + ' ' * 4) + (' ' * 5 * (level - 2))
            print("{0}{1}{2}".format(leading, lasting, label))

        if self[nid].expanded:
            level += 1
            for element in queue:
                self.show(element, level)


    def subtree(self, nid):
        """
        Return a COPY of subtree of the whole tree with the nid being the new root.
        And the structure of the subtree is maintained from the old tree.
        """
        st = Tree()
        st.root = nid
        for node_n in self.expand_tree(nid):
            st.nodes.update({self[node_n].identifier : self[node_n]})
        return st


    def __contains__(self, identifier):
        return [node.identifier for node in self.nodes
                if node.identifier is identifier]


    def __getitem__(self, key):
        return self.nodes[key]


    def __len__(self):
        return len(self.nodes)


    def __setitem__(self, key, item):
        self.nodes.update({key: item})


    def __update_bpointer(self, nid, identifier):
        self[nid].bpointer = identifier


    def __update_fpointer(self, nid, identifier, mode):
        if nid is None:
            return
        else:
            self[nid].update_fpointer(identifier, mode)
