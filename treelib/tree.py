#!/usr/bin/env python
import json
from copy import deepcopy
try:
    from .node import Node
except:
    from node import Node 

__author__ = 'chenxm'


class NodeIDAbsentError(Exception):
    pass

class MultipleRootError(Exception):
    pass

class DuplicatedNodeIdError(Exception):
    pass

class LinkPastRootNodeError(Exception):
    pass


class Tree(object):

    (ROOT, DEPTH, WIDTH, ZIGZAG) = list(range(4))


    def __init__(self, tree=None, deep=False):
        """
        Initiate a new tree or copy another tree with a shallow or deep copy.
        """
        self._nodes = {}
        self.root = None
        if tree is not None:
            self.root = tree.root
            if deep:
                for nid in tree._nodes:
                    self._nodes[nid] = deepcopy(tree._nodes[nid])
            else:
                self._nodes = tree._nodes


    @property
    def nodes(self):
        '''
        Return a dict form of nodes in a tree
        '''
        return self._nodes


    def all_nodes(self):
        """
        Return all nodes in a list
        """
        return list(self._nodes.values())


    def size(self, level=None):
        """
        Get the number of nodes in this tree
        """
        return len(self._nodes)


    def depth(self, node=None):
        """
        Get the maximum level of this tree or the level of the given node
        @param node Node
        @return int
        @throw OSError, NodeIDAbsentError
        """
        def cal_depth(identifier):
            ret = 0
            parent = self.parent(identifier)
            while parent is not None:
                parent = self.parent(parent.identifier)
                ret += 1
            return ret

        ret = 0
        if node is None:
            # Get maximum level of this tree
            leaves = self.leaves()
            for leave in leaves:
                level = cal_depth(leave.identifier)
                ret = level if level >= ret else ret
        else:
            # Get level of the given node
            if not isinstance(node, Node):
                raise OSError("Second parameter must be object of Class::Node.")
            nid = node.identifier
            if not self.contains(nid):
                raise NodeIDAbsentError("Node '%s' is not in the tree" % nid)
            ret = cal_depth(node.identifier)
        return ret

    def get_node(self, nid):
        """
        Return the node with nid.
        None returned if nid not exists.
        """
        if nid is None or not self.contains(nid):
            return None
        return self._nodes[nid]


    def contains(self, nid):
        """
        Check if the tree contains node of given id
        """
        return True if nid in self._nodes else False


    def parent(self, nid):
        """
        Get parent node object of given id
        """
        if not self.contains(nid):
            raise NodeIDAbsentError("Node '%s' is not in the tree" % nid)
        pid = self[nid].bpointer
        if pid is None or not self.contains(pid):
            return None
        return self[pid]


    def is_branch(self, nid):
        """
        Return the children (only sons and daughters) IDs of nid.
        Empty list is returned if nid does not exist
        """
        if nid is None:
            raise OSError("First parameter can't be None")
        if not self.contains(nid):
            raise NodeIDAbsentError("Node '%s' is not in the tree" % nid)

        try:
            fpointer = self[nid].fpointer
        except KeyError:
            fpointer = []
        return fpointer


    def siblings(self, nid):
        """
        Return the siblings of given @nid.
        If @nid is root or there are no siblings, an empty list is returned.
        """
        siblings = []
        if nid != self.root:
            pid = self[nid].bpointer
            siblings = [i for i in self[pid].fpointer if i != nid]
        return siblings


    def leaves(self, root=None):
        """
        Get leaves of the whole tree of a subtree.
        """
        leaves = []
        if root is None:
            for node in self._nodes.values():
                if node.is_leaf():
                    leaves.append(node)
        else:
            for node in self.expand_tree(root):
                if self[node].is_leaf():
                    leaves.append(node)
        return leaves


    def link_past_node(self, nid):
        """
        Delete a node by linking past it.
        For example, if we have a -> b -> c
        and delete node b, we are left with a -> c
        """
        if not self.contains(nid):
            raise NodeIDAbsentError("Node '%s' is not in the tree" % nid)
        if self.root == nid:
            raise LinkPastRootNodeError("Cannot link past the root node, delete it with remove_node()")
        #Get the parent of the node we are linking past
        parent = self[self[nid].bpointer]
        #Set the children of the node to the parent
        for child in self[nid].fpointer:
            self[child].update_bpointer(parent.identifier)
        #Link the children to the parent
        parent.fpointer += self[nid].fpointer
        #Delete the node
        parent.update_fpointer(nid, mode=parent.DELETE)
        del(self._nodes[nid])


    def add_node(self, node, parent=None):
        """
        Add a new node to tree.
        The 'node' parameter refers to an instance of Class::Node
        """
        if not isinstance(node, Node):
            raise OSError("First parameter must be object of Class::Node.")

        if node.identifier in self._nodes:
            raise DuplicatedNodeIdError("Can't create node with ID '%s'" % node.identifier)

        if parent is None:
            if self.root is not None:
                raise MultipleRootError("A tree takes one root merely.")
            else:
                self.root = node.identifier
        elif not self.contains(parent):
            raise NodeIDAbsentError("Parent node '%s' is not in the tree" % parent)

        self._nodes.update({node.identifier : node})
        self.__update_fpointer(parent, node.identifier, Node.ADD)
        self.__update_bpointer(node.identifier, parent)


    def create_node(self, tag=None, identifier=None, parent=None, data=None):
        """
        Create a child node for given @parent node.
        """
        node = Node(tag=tag, identifier=identifier,data=data)
        self.add_node(node, parent)
        return node


    def expand_tree(self, nid=None, mode=DEPTH, filter=None, key=None, reverse=False):
        """
        Python generator. Loosly based on an algorithm from 'Essential LISP' by
        John R. Anderson, Albert T. Corbett, and Brian J. Reiser, page 239-241
        UPDATE: the @filter function is performed on Node object during traversing.
        UPDATE: the @key and @reverse are present to sort nodes at each level.
        """
        nid = self.root if (nid is None) else nid
        if not self.contains(nid):
            raise NodeIDAbsentError("Node '%s' is not in the tree" % nid)

        filter = self._real_true if (filter is None) else filter
        if filter(self[nid]):
            yield nid
            queue = [self[i] for i in self[nid].fpointer if filter(self[i])]
            if mode in [self.DEPTH, self.WIDTH]:
                queue.sort(key=key, reverse=reverse)
                while queue:
                    yield queue[0].identifier
                    expansion = [self[i] for i in queue[0].fpointer if filter(self[i])]
                    expansion.sort(key=key, reverse=reverse)
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


    def move_node(self, source, destination):
        """
        Move a node indicated by @source parameter to be a child of @destination.
        """
        if not self.contains(source) or not self.contains(destination):
            raise NodeIDAbsentError

        parent = self[source].bpointer
        self.__update_fpointer(parent, source, Node.DELETE)
        self.__update_fpointer(destination, source, Node.ADD)
        self.__update_bpointer(source, destination)


    def paste(self, nid, new_tree, deepcopy=False):
        """
        Paste a @new_tree to the original one by linking the root
        of new tree to given node (nid).
        Update: add @deepcopy of pasted tree.
        """
        assert isinstance(new_tree, Tree)
        if nid is None:
            raise OSError("First parameter can't be None")

        if not self.contains(nid):
            raise NodeIDAbsentError("Node '%s' is not in the tree" % nid)

        set_joint = set(new_tree._nodes) & set(self._nodes) # joint keys
        if set_joint:
            # TODO: a deprecated routine is needed to avoid exception
            raise ValueError('Duplicated nodes %s exists.' % list(set_joint))

        if deepcopy:
            for node in new_tree._nodes:
                self._nodes.update({node.identifier: deepcopy(node)})
        else:
            self._nodes.update(new_tree._nodes)
        self.__update_fpointer(nid, new_tree.root, Node.ADD)
        self.__update_bpointer(new_tree.root, nid)


    def remove_node(self, identifier):
        """
        Remove a node indicated by 'identifier'; all the successors are removed as well.
        Return the number of removed nodes.
        """
        removed = []
        if identifier is None: return 0

        if not self.contains(identifier):
            raise NodeIDAbsentError("Node '%s' is not in the tree" % identifier)

        parent = self[identifier].bpointer
        for id in self.expand_tree(identifier):
            # TODO: implementing this function as a recursive function:
            #       check if node has children
            #       true -> run remove_node with child_id
            #       no -> delete node
            removed.append(id)
        cnt = len(removed)
        for id in removed:
            del(self._nodes[id])
        # Update its parent info
        self.__update_fpointer(parent, identifier, Node.DELETE)
        return cnt


    def rsearch(self, nid, filter=None):
        """
        Traverse the tree branch along the branch from nid to its ancestors (until root).
        """
        if nid is None: return
        if not self.contains(nid):
            raise NodeIDAbsentError("Node '%s' is not in the tree" % nid)

        filter = (self._real_true) if (filter is None) else filter

        current = nid
        while current is not None:
            if filter(self[current]):
                yield current
            current = self[current].bpointer


    def save2file(self, filename, nid=None, level=ROOT, idhidden=True, filter=None, key=None, reverse=False):
        """
        Update 20/05/13: Save tree into file for offline analysis
        """
        leading = ''
        lasting = '|___ '
        nid = self.root if (nid is None) else nid
        if not self.contains(nid):
            raise NodeIDAbsentError
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
            queue.sort(key=key, reverse=reverse)
            level += 1
            for element in queue:
                self.save2file(filename, element.identifier, level, idhidden, filter, key, reverse)


    def _real_true(self, p):
        return True


    def show(self, nid=None, level=ROOT, idhidden=True, filter=None, key=None, reverse=False):
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
        UPDATE: the @key @reverse is present to sort node at each level.
        """
        leading = ''
        lasting = '|___ '

        nid = self.root if (nid is None) else nid
        if not self.contains(nid):
            raise NodeIDAbsentError("Node '%s' is not in the tree" % nid)

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
            queue.sort(key=key, reverse=reverse)
            level += 1
            for element in queue:
                self.show(element.identifier, level, idhidden, filter, key, reverse)


    def subtree(self, nid):
        """
        Return a shallow COPY of subtree with nid being the new root.
        If nid is None, return an empty tree.
        If you are looking for a deepcopy, please create a new tree with this shallow copy,
        e.g.
            new_tree = Tree(t.subtree(t.root), deep=True)
        This line creates a deep copy of the entire tree.
        """
        st = Tree()
        if nid is None:
            return st

        if not self.contains(nid):
            raise NodeIDAbsentError("Node '%s' is not in the tree" % nid)

        st.root = nid
        for node_n in self.expand_tree(nid):
            st._nodes.update({self[node_n].identifier : self[node_n]})
        return st


    def remove_subtree(self, nid):
        """
        Return a subtree deleted from this tree. If nid is None, an empty tree is returned.
        For the original tree, this method is similar to `remove_node(self,nid)`, because given node and
        its children are removed from the original tree in both methods.
        For the returned value and performance, these two methods are different:
            `remove_node` returns the number of deleted nodes;
            `remove_subtree` returns a subtree of deleted nodes;
        You are always suggested to use `remove_node` if your only to delete nodes from a tree, as the other
        one need memory allocation to store the new tree.
        """
        st = Tree()
        if nid is None: return st

        if not self.contains(nid):
            raise NodeIDAbsentError("Node '%s' is not in the tree" % nid)
        st.root = nid

        parent = self[nid].bpointer
        self[nid].bpointer = None # reset root parent for the new tree
        removed = []
        for id in self.expand_tree(nid):
            removed.append(id)
        for id in removed:
            st._nodes.update({id: self._nodes.pop(id)})
        # Update its parent info
        self.__update_fpointer(parent, nid, Node.DELETE)
        return st


    def _to_dict(self, nid=None, key=None, reverse=False):

        nid = self.root if (nid is None) else nid
        tree_dict = {self[nid].tag: {"children": []}}

        if self[nid].expanded:
            queue = [self[i] for i in self[nid].fpointer]
            key = (lambda x: x) if (key is None) else key
            queue.sort(key=key, reverse=reverse)

            for elem in queue:
                tree_dict[self[nid].tag]["children"].append(
                    self._to_dict(elem.identifier))
            if tree_dict[self[nid].tag]["children"] == []:
                tree_dict = self[nid].tag
            return tree_dict


    def to_json(self):
        return json.dumps(self._to_dict())


    def __contains__(self, identifier):
        return [node.identifier for node in self._nodes
                if node.identifier is identifier]


    def __getitem__(self, key):
        return self._nodes[key]


    def __len__(self):
        return len(self._nodes)


    def __setitem__(self, key, item):
        self._nodes.update({key: item})


    def __update_bpointer(self, nid, parent_id):
        self[nid].update_bpointer(parent_id)


    def __update_fpointer(self, nid, child_id, mode):
        if nid is None:
            return
        else:
            self[nid].update_fpointer(child_id, mode)



if __name__ == '__main__':
    pass