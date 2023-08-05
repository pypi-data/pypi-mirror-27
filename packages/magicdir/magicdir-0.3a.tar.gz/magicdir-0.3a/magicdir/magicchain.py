import keyword
from copy import copy


class MagicList(list):
    """List-like class that collects attributes and applies functions
    but functions like a list in every other regard.

    .. code-block:: python

        m1 = MagicList(["string1   ", "   string2"])
        m1.strip().upper() # ["STRING1", "STRING2"]
    """

    def __getattr__(self, item):
        return MagicList([getattr(x, item) for x in self])

    def __call__(self, *args, **kwargs):
        return MagicList([x(*args, **kwargs) for x in self])


def magiclist(fxn):
    """Decorator that turns a returned value from a list to a MagicList (if possible)"""

    def magiclist_wrapper(*args, **kwargs):
        ret = fxn(*args, **kwargs)
        try:
            iter(ret)
            ret = MagicList(ret)
        except TypeError:
            # not iterable
            pass
        return ret

    return magiclist_wrapper


class MagicChain(object):
    """
    A tree-like class for chaining commands and attributes together with special
    root/head handling.

    Each attribute creates a new MagicChain instance (a 'node') which acts like a node in a
    linked list.

    .. code-block:: python

        root.child1.child2.child3 # etc.

    New nodes can be 'pushed_up'
    """

    def __init__(self, push_up=None):
        """
        Chainer constructor

        :param parent: parent node that called this object
        :type parent: MagicChain
        :param push_up: whether to push up attributes to the root node
        :type push_up: boolean
        """
        self._parent = None
        self._children = {}
        self._grandchildren = {}
        self._push_up = False
        if push_up is not None:
            self._push_up = push_up

    # TODO: add dynamic attr that looks at parent? It would be really slow...

    @property
    def attr(self):
        """The name for this node from the parent's reference."""
        if self.parent:
            for k, v in self.parent._children.items():
                if v is self:
                    return k

    @property
    def parent(self):
        """This nodes parent"""
        return self._parent

    @property
    @magiclist
    def children(self):
        """This nodes descendent notes"""
        return self._children.values()

    @property
    def root(self):
        """The root/head node"""
        if self.parent is None:
            return self
        return self.parent.root

    def is_root(self):
        """Whether this node is the root/head node"""
        return self is self.root

    @magiclist
    def descendents(self, include_self=False):
        """
        All descendent nodes

        :param include_self: Whether to include this node in the return list
        :type include_self: boolean
        :return: list of descendent nodes (list of MagicChain instances)
        :rtype: list
        """
        c = []
        if include_self:
            c = [self]
        if not self._children == {}:
            children = list(self._children.values())
            c += children
            for child in children:
                c += child.descendents()
        return c

    @magiclist
    def ancestors(self, include_self=False):
        """
        All ancestral nodes

        :param include_self: Whether to include this node in the return list
        :type include_self: boolean
        :return: list of ancestor nodes (list of MagicChain instances)
        :rtype: list
        """
        p = []
        if self.parent is not None:
            p += self.parent.ancestors(include_self=True)
        if include_self:
            p += [self]
        return p

    # def ancestor_attrs(self, attr, include_self=False):
    #     nodes = self.ancestors(include_self=include_self)
    #     return [getattr(n, attr) for n in nodes]
    #
    # def descendent_attrs(self, attr, include_self=False):
    #     nodes = self.descendents(include_self=include_self)
    #     return [getattr(n, attr) for n in nodes]

    # def connect(self, other, push_up=None):
    #     raise NotImplemented("Connect is not yet implemented.")
    #     # if push_up is None:
    #     #     push_up = self._push_up
    #     # other.remove()
    #     # self._add_child(other, push_up=push_up)

    def remove_parent(self):
        """Remove this node's parent, effectively breaking the chain"""
        if self.parent is not None:
            parent = self.parent
            rm = parent._remove_child(self.attr)
            rm._parent = None
            parent._update_grandchildren()
            rm._update_grandchildren()
            return rm

    def _sanitize_identifier(self, iden):
        """Validates the identifier to ensure it is not a reserve keyword 
        used in python ('which', 'in', 'class', 'else', etc.). Other strings
        such as 'something.else' that cannot be translated into an attribute
        are also disallowed."""
        if keyword.iskeyword(iden):
            raise AttributeError("\"{}\" is reserved and is not a valid identified.".format(iden))
        if not iden.isidentifier():
            raise AttributeError("\"{}\" is not a valid identifier.".format(iden))

    def _validate_attr(self, attr, push_up=None):
        """Validates the attribute name for a node and checks if that attribute
        (i) already exists or (ii) already exists in the root attributes (if push_up=True)

        param attr: attribute name for potential node
        :type attr: str
        :param push_up: whether to validate if the attribute exists in the list of root attributes
        :type push_up: boolean
        :return: None
        :rtype: None
        """
        if push_up is None:
            push_up = self._push_up
        if hasattr(self, attr):
            raise AttributeError("Attribute \"{}\" already exists".format(attr))
        if push_up:
            if hasattr(self.root, attr):
                raise AttributeError("Cannot push up attr \"{}\". Attribute already exists".format(attr))

    # def _add_as_child(self, child):
    #     # self._validate_child(child)
    #     self._children[child.attr] = child
    #     return child

    # def _validate_child(self, child):
    #     if child.attr in self._children:
    #         raise AttributeError("Cannot add attr {}. Try using a unique attr.".format(child.attr))

    # def _add_as_grandchild(self, child):
    #     # self._validate_grandchild(child)
    #     self.root._grandchildren[child.attr] = child
    #     return child

    # def _validate_grandchild(self, child):
    #     if child.attr in self.root._grandchildren:
    #         raise AttributeError("Cannot push attr {} to root. Try using a unique attr.".format(child.attr))

    def _add(self, attr, child, push_up=None, make_attr=True):
        """
        Adds child node to this node.

        :param attr: name to use to reference the child
        :type attr: str
        :param child: child node to add
        :type child: MagicChain
        :param push_up: whether to add the child node to the root node. If True, the
        child will be able to be accessed from the root node.
        :type push_up: boolean
        :param make_attr: whether to give access to this node via attribute format. For
        example, with attr='mynode', parent.mynode would give access to the child node
        :type make_attr: boolean
        :return: the child node
        :rtype: MagicChain
        """
        if make_attr:
            self._sanitize_identifier(attr)
        if push_up is None:
            push_up = self._push_up
        self._validate_attr(attr, push_up)
        self._children[attr] = child
        if push_up:
            if attr not in self.root._children:
                self.root._grandchildren[attr] = child
        return child

    def _create_child(self, with_attributes=None):
        """
        Create a new copy node with with a set of attributes

        :param with_attributes: list of attributes to apply to child
        :type with_attributes: dict
        :return: child node
        :rtype: MagicChain
        """
        c = copy(self)
        c._parent = self
        c._children = {}
        c._grandchildren = {}
        if with_attributes is None:
            with_attributes = {}
        for k, v in with_attributes.items():
            setattr(c, k, v)
        return c

    def _create_and_add_child(self, attr, with_attributes=None, push_up=None, make_attr=True):
        """
        Copy this node and adds the node as a child

        :param attr: name of the new node
        :type attr: str
        :param with_attributes: attribute to apply to the new node
        :type with_attributes: dict
        :param push_up: whether to push the new node to root.
        :type push_up: boolean
        :param make_attr: whether to give parent nodes access to this node via an attribute
        :type make_attr: boolean
        :return: the newly added child node
        :rtype: MagicChain
        """
        if push_up is None:
            push_up = self._push_up
        child = self._create_child(with_attributes)
        return self._add(attr, child, push_up=push_up, make_attr=make_attr)

    def _remove_child(self, attr):
        """
        Removes a child from this node

        :param attr: the attribute name of the node
        :type attr: str
        :return: the removed child, else return None
        :rtype: MagicChain or None
        """
        if attr in self._children:
            return self._children.pop(attr)

    # TODO: push_up is never really used
    def _update_grandchildren(self, push_up=None):
        """ Updates accessible children """
        if push_up is None:
            push_up = self._push_up
        if push_up:
            self.root._grandchildren = {}
            for c in self.children:
                d = c.descendents(include_self=False)
                for gc in d:
                    self._add_grandchild(gc)

    def _attributes(self):
        """List of all attributes accessible"""
        return list(self._children.keys()) + list(self._grandchildren.keys())

    def _add_grandchild(self, child):
        """Adds a node to the roots grandchildren"""
        self.root._grandchildren[child.attr] = child
        return child

    def get(self, attr):
        """Short for getattr(self, attr)"""
        return getattr(self, attr)

    def has(self, attr):
        """Short for hasattr(self, attr)"""
        return hasattr(self, attr)

    # def _remove_grandchild(self, attr):
    #     gc = self.root._grandchildren
    #     if attr in gc:
    #         return gc.pop(attr)

    def __getattr__(self, name):
        """Override for getattr that will retrieve the node from an attribute"""
        c = {}
        c.update(object.__getattribute__(self, "_children"))
        c.update(object.__getattribute__(self, "_grandchildren"))
        if name in c:
            return c[name]
        return object.__getattribute__(self, name)

    def __setattr__(self, name, value):
        """Override for setattr that raise AttributeError if the attribute name
        is found in the list of available node name's. Cannot overwrite a
        a node using setattr."""
        ckey = '_children'
        gckey = '_grandchildren'
        if ckey in self.__dict__ and gckey in self.__dict__:
            c = {}
            c.update(object.__getattribute__(self, "_children"))
            c.update(object.__getattribute__(self, "_grandchildren"))
            if name in c:
                raise AttributeError("Cannot set attribute \"{}\".".format(name))
        return object.__setattr__(self, name, value)

    def __dir__(self):
        """Gives dynamic interpreters access to available nodes"""
        return super().__dir__() + list(self._children.keys()) + list(self._grandchildren.keys())

