from node import Node


class MultipleRootError(Exception):
    pass


class DuplicatedNodeIdError(Exception):
    pass


class Tree(object):

    (ROOT, DEPTH, WIDTH, ZIGZAG) = range(4)


    def __init__(self):
        self.nodes = {}
        self.root = None


    def add_node(self, node, parent=None):
        """
        Add a new node to tree.
        The 'node' parameter refers to an instance of Class::Node
        """
        if not isinstance(node, Node):
            raise OSError("First parameter must be object of Class::Node.")

        if node.identifier in self.nodes:
            node = self.get_node(node.identifier)
        else:
            self.nodes.update({node.identifier : node})

        if parent is None:
            if self.root is not None:
                raise MultipleRootError
            else:
                self.root = node.identifier
        else:
            parent = Node.sanitize_id(parent)

        self.__update_fpointer(parent, node.identifier, Node.ADD)
        self.__update_bpointer(parent, node.identifier, Node.ADD)


    def create_node(self, tag, identifier=None, parent=None):
        """
        Create a child node for the node indicated by the 'parent' parameter
        """
        node = Node(tag, identifier)
        self.add_node(node, parent)
        return node


    def expand_tree(self, nid=None, mode=DEPTH, filter=None, cmp=None, key=None, reverse=False):
        """
        Python generator. Loosly based on an algorithm from 'Essential LISP' by
        John R. Anderson, Albert T. Corbett, and Brian J. Reiser, page 239-241
        UPDATE: the @filter function is perform on Node object.
        UPDATE: the @cmp @key @reverse is present to sort node at each level.
        """
        nid = self.root if (nid is None) else Node.sanitize_id(nid)
        filter = self._real_true if (filter is None) else filter

        if filter(self[nid]):
            yield nid
            queue = [self[i] for i in self[nid].fpointer if filter(self[i])]
            if mode in [self.DEPTH, self.WIDTH]:
                queue.sort(cmp=cmp, key=key, reverse=reverse)
                while queue:
                    yield queue[0].identifier
                    expansion = [self[i] for i in queue[0].fpointer if filter(self[i])]
                    expansion.sort(cmp=cmp, key=key, reverse=reverse)
                    if mode is self.DEPTH:
                        queue = expansion + queue[1:]  # depth-first
                    elif mode is self.WIDTH:
                        queue = queue[1:] + expansion  # width-first
            elif mode is self.ZIGZAG:
                ## Suggested by Ilya Kuprik (ilya-spy@ynadex.ru).
                stack_fw = []
                queue.reverse()
                stack = stack_bw = queue
                direction = False
                while stack:
                    expansion = [self[i] for i in stack[0].fpointer if filter(self[i])]
                    yield stack.pop(0).identifier
                    if direction:
                        expansion.reverse()
                        stack_bw = expansion + stack_bw
                    else:
                        stack_fw = expansion + stack_fw
                    if not stack:
                        direction = not direction
                        stack = stack_fw if direction else stack_bw

    def get_node(self, nid):
        """
        Return the node with nid.
        None returned if nid not exists.
        """
        if nid is not None:
            nid = Node.sanitize_id(nid)
        try:
            node = self.nodes[nid]
        except KeyError:
            node = None
        return node


    def is_branch(self, nid):
        """
        Return the following nodes of nid.
        Empty list returned if nid not exists
        """
        if nid is not None:
            nid = Node.sanitize_id(nid)
        try:
            fpointer = self[nid].fpointer
        except KeyError:
            fpointer = []
        return fpointer


    def move_node(self, source, destination):
        """
        Move a node indicated by the 'source' parameter to the parent node
        indicated by the 'dest' parameter
        """
        source = Node.sanitize_id(source)
        destination = Node.sanitize_id(destination)
        parents = self[source].bpointer
        for parent in parents:
            self.__update_fpointer(parent, source, Node.DELETE)
            self.__update_bpointer(source, parent, Node.DELETE)
        self.__update_fpointer(destination, source, Node.ADD)
        self.__update_bpointer(source, destination, Node.ADD)


    def paste(self, nid, new_tree):
        """
        Paste a new tree to the original one by linking the root
        of new tree to nid.
        """
        assert isinstance(new_tree, Tree)

        if nid is None:
            raise OSError("First parameter can't be None")

        nid = Node.sanitize_id(nid)

        set_joint = set(new_tree.nodes) & set(self.nodes)
        if set_joint:
            raise ValueError('Duplicated nodes %s exists.' % list(set_joint))

        self.__update_bpointer(new_tree[new_tree.root].identifier, nid, Node.ADD)
        self.__update_fpointer(nid, new_tree.root, Node.ADD)
        self.nodes.update(new_tree.nodes)


    def remove_node(self, identifier):
        """
        Remove a node indicated by 'identifier'. All the successors are removed, too.
        """
        if identifier is None:
            return

        identifier = Node.sanitize_id(identifier)
        parents = self[identifier].bpointer
        remove = []
        for id in self.expand_tree(identifier):
            # TODO: implementing this function as a recursive function:
            #       check if node has children
            #       true -> run remove_node with child_id
            #       no -> delete node
            remove.append(id)

        for id in remove:
            del(self.nodes[id])

        for parent in parents:
            self.__update_fpointer(parent, identifier, Node.DELETE)


    def rsearch(self, nid, filter=None):
        """
        Search the tree from nid to the root along links reversedly.
        """
        if nid is None:
            return
        filter = (self._real_true) if (filter is None) else filter

        current = Node.sanitize_id(nid)
        while current is not None:
            if filter(self[current]):
                yield current
            current = self[current].bpointer


    def save2file(self, filename, nid=None, level=ROOT, idhidden=True, filter=None, cmp=None, key=None, reverse=False):
        """
        Update 20/05/13: Save tree into file for offline analysis
        """
        leading = ''
        lasting = '|___ '
        nid = self.root if (nid is None) else Node.sanitize_id(nid)
        label = ("{0}".format(self[nid].tag)) if idhidden else ("{0}[{1}]".format(self[nid].tag, self[nid].identifier))
        filter = (self._real_true) if (filter is None) else filter

        if level == self.ROOT:
            open(filename, 'ab').write(label + '\n')
        else:
            if level <= 1:
                leading += ('|' + ' ' * 4) * (level - 1)
            else:
                leading += ('|' + ' ' * 4) + (' ' * 5 * (level - 2))
            open(filename, 'ab').write("{0}{1}{2}\n".format(leading, lasting, label))

        if filter(self[nid]) and self[nid].expanded:
            queue = [self[i] for i in self[nid].fpointer if filter(self[i])]
            key = (lambda x: x) if (key is None) else key
            queue.sort(cmp=cmp, key=key, reverse=reverse)
            level += 1
            for element in queue:
                self.save2file(filename, element.identifier, level, idhidden, filter, cmp, key, reverse)


    def _real_true(self, p):
        return True


    def show(self, nid=None, level=ROOT, idhidden=True, filter=None, cmp=None, key=None, reverse=False):
        """"
        Another implementation of printing tree using Stack
        Print tree structure in hierarchy style.
        For example:
            Root
            |___ C01
            |    |___ C11
            |         |___ C111
            |         |___ C112
            |___ C02
            |___ C03
            |    |___ C31
        A more elegant way to achieve this function using Stack structure,
        for constructing the Nodes Stack push and pop nodes with additional level info.
        UPDATE: the @cmp @key @reverse is present to sort node at each level.
        """
        leading = ''
        lasting = '|___ '

        nid = self.root if (nid is None) else Node.sanitize_id(nid)
        label = ("{0}".format(self[nid].tag)) if idhidden else ("{0}[{1}]".format(self[nid].tag, self[nid].identifier))
        filter = (self._real_true) if (filter is None) else filter

        if level == self.ROOT:
            print(label)
        else:
            if level <= 1:
                leading += ('|' + ' ' * 4) * (level - 1)
            else:
                leading += ('|' + ' ' * 4) + (' ' * 5 * (level - 2))
            print("{0}{1}{2}".format(leading, lasting, label))

        if filter(self[nid]) and self[nid].expanded:
            queue = [self[i] for i in self[nid].fpointer if filter(self[i])]
            key = (lambda x: x) if (key is None) else key
            queue.sort(cmp=cmp, key=key, reverse=reverse)
            level += 1
            for element in queue:
                self.show(element.identifier, level, idhidden, filter, cmp, key, reverse)


    def subtree(self, nid):
        """
        Return a COPY of subtree of the whole tree with the nid being the new root.
        And the structure of the subtree is maintained from the old tree.
        """
        st = Tree()
        if nid is None:
            return st
        st.root = Node.sanitize_id(nid)
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


    def __update_bpointer(self, nid, identifier, mode):
        if nid is None:
            return
        else:
            self[nid].update_bpointer(identifier, mode)


    def __update_fpointer(self, nid, identifier, mode):
        if nid is None:
            return
        else:
            self[nid].update_fpointer(identifier, mode)
