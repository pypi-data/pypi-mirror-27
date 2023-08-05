import functools
import inspect


class Factory(object):
    """Factory for test fixtures.

    Fixtures (arbitrary Python objects) are made by calling 'makers'.  A maker
    is a callable that takes one argument, a Factory instance.  A fixture is
    instantiated like this:

    >>> factory.window

    The Factory will call the maker function to make the fixture, and cache it,
    so that the next reference to .window will be the same object.  Here is a
    maker function for a window (note make_window is NOT a maker function
    because it does not take a factory as its argument):

    def window(factory):
        return make_window(double_glazed=True)

    Makers may reference other makers by instantiating fixtures using attribute
    lookup.  Here is a maker for a house, which depends on the window:

    def house(factory):
        return make_house(factory.window)

    In this way an implicit dependency graph is declared.  Then, in test code,
    to make fixtures that have dependencies, it is not necessary to explicitly
    construct the dependencies:

    >>> factory.house

    It is still possible to have control of dependencies by use of the set
    method:

    >>> factory.set('window', MyWindow())
    >>> factory.house  # uses MyWindow() from above

    You should only call .set for a named fixture if it has not yet been
    instantiated (if you do this an exception is raised).

    Where possible the makers return "the one and only" item of that type (one
    sale order, one product, etc.).  This is useful because it makes it easy to
    deal with relationships between the fixtures, and easy to refer to fixtures
    in tests -- no need to specify which one.

    When you do need more than one instance of a fixture, use the partial_copy
    method.

    Note: self.test is for use only as a temporary means of migrating old tests
    to use this class.  It is better for tests to depend on fixtures, and for
    fixtures to not depend on tests.

    A test is usually formed of setup code that creates fixtures, followed by
    code that performs some action that may trigger a side-effect, which is
    then checked using test assertion methods.  So that that action only calls
    as much code as is needed to trigger the side-effect, it is better to call
    setup code on a separate line so that it is clear it did not trigger the
    side effect.  Sometimes this setup code may itself be used just for the
    fixture instantiation side-effect:

    def test_pushing_button_launches_missiles(self, factory):
        factory.button  # shouldn't launch missiles
        launches = self.subscribe_to_launch_missile()
        factory.button.push()
        self.assert_len(launches, 1)

    Some makers may customize a fixture made by another maker:

    def seal(factory):
        return Seal()

    def broken_seal(factory):
        seal = factory.seal
        seal.break()
        return seal

    Then:

    >>>> assert factory.seal is factory.broken_seal

    and iff factory.broken_seal is never referenced, the seal is intact.  If
    necessary another maker can be defined that is unambigously unbroken:

    def intact_seal(factory):
        return Seal()

    Fixtures can themselves be Factory instances.  This forms a tree (it would
    be possible to form some other graph: not encouraged!).  There is special
    support for this:

    1. Factory instances know their 'root' factory.  This is the root of the
    tree.  Maker functions are called with the root factory as their argument.

    2. .partial_copy() supports dotted names:

    factory.partial_copy(['cr', 'products', 'sales.so'])
    """

    _Missing = object()

    def __init__(self, add_cleanup, test=None, root=None):
        self.__dict__['_makers'] = {}
        self.add_cleanup = add_cleanup
        self.test = test
        # Note that the tree of Factory instances is defined by self._makers.
        # This class has little knowledge of that tree except for navigation
        # down the tree via attribute lookup.  In particular because child
        # factories are just fixtures, there is no way for this class to
        # navigate from child to parent to find the 'root' factory.  For that
        # reason self._root, a reference to the 'root' factory, is stored
        # separately.  It is there only so that the very top-level factory can
        # be found in order to pass it to maker functions.
        if root is None:
            root = self
        self._root = root
        self._made = {}

    def make_child_factory(self, makers):
        return make_factory(self.add_cleanup, self.test, self._root, makers)

    def add_maker(self, name, maker):
        """Add a maker.

            Args:
                name (string): attribute name by which the made fixture will be
                available on the Factory instance
                maker (callable): one-argument function that instantiates a new
                fixture

        Use of 'is_finder' attribute on maker functions is experimental!
        """
        if name in self._makers:
            raise ValueError(
                'Too late to add object %s because it is already added: '
                '%s' % (name, self._makers[name]))
        self._makers[name] = maker

    def __getattr__(self, name):
        try:
            maker = self._makers[name]
        except KeyError:
            # Raise AttributeError
            getattr(type(self), name)
        obj = self._made.get(name, self._Missing)
        if getattr(maker, 'is_finder', False):
            obj = maker(self._root)
        elif obj is self._Missing:
            obj = maker(self._root)
            self._made[name] = obj
        return obj

    def force_set(self, name, value):
        """Set a fixture, regardless of whether or not it is already made.

        Only use this for value objects.  Otherwise it causes surprising
        dependencies:

        door = factory.door
        factory.house
        factory.set('door', my_door)
        assert factory.house.door is factory.door  # Fails
        """
        if name not in self._makers:
            raise ValueError(
                'Cannot set object %s because there is no maker defined '
                'for it: call factory.add_maker or fix maker name' % (name, ))
        self._made[name] = value

    def __setattr__(self, name, value):
        if name in self.__dict__['_makers']:
            raise AttributeError(
                'Cannot set object %s because there a maker defined '
                'for it: call factory.set(name, value) instead' % (name, ))
        super(Factory, self).__setattr__(name, value)

    def set(self, name, value):
        if name not in self._makers:
            raise ValueError(
                'Cannot set object %s because there is no maker defined '
                'for it: call factory.add_maker or fix maker name' % (name, ))
        elif name in self._made:
            raise ValueError(
                'Too late to set object %s because it is already made: %s' %
                (name, self._made[name]))
        self._made[name] = value

    def _partial_copy(self, to_copy, new_root):
        new = make_factory(self.add_cleanup, self.test, new_root,
                           self._makers.items())
        if new_root is None:
            new_root = new
        children_to_copy = {}
        leaf_names = set()
        for name in to_copy:
            names = name.split('.', 1)
            if len(names) == 1:
                # Leaf name of requested copy.  This is not necessarily a leaf
                # of the tree of fixture factories: the fixture may be a
                # Factory instance.
                leaf_names.add(name)
                fixture = getattr(self, name)
                new.set(name, fixture)
            else:
                # Assemble names to recurse on
                first, rest = names
                if first in leaf_names:
                    # If say 'widgets' AND 'widgets.spam' is specified, ignore
                    # 'widgets.spam'.
                    continue

                children_to_copy.setdefault(first, []).append(rest)

        # Recurse
        for name, to_copy in children_to_copy.items():
            child = getattr(self, name)
            if not isinstance(child, type(self)):
                raise ValueError(name)

            new_child = child._partial_copy(to_copy, new_root)
            new.set(name, new_child)
        return new

    def partial_copy(self, to_copy):
        """Return a new Factory that has named fixtures to_copy already set.

        This allows for constructing non-identical copies of fixtures that
        still are related in some way: say when you need two windows in the
        same house.
        """
        # None here means make the new factory a root factory
        new_root = None if self is self._root else self._root
        return self._partial_copy(to_copy, new_root)


class MakerSetHelper(object):

    def __init__(self):
        self.makers = []

    def add_maker(self, func, name=None):
        if name is None:
            name = func.__name__
        self.makers.append((name, func))

    def add_finder(self, func, name=None):
        func.is_finder = True
        self.add_maker(func, name)

    def add_constant(self, name, const):
        self.add_maker(lambda factory: const, name)


def adapt_class(class_):
    """Return function to make makers, given makers defined by a class.

    Each method defines a maker function.

    The returned function is suitable to pass to with_factory -- i.e. this
    serves the same purpose as MakerSetHelper.
    """
    return lambda: inspect.getmembers(class_(), inspect.ismethod)


def make_factory(add_cleanup, test, root, makers):
    factory = Factory(add_cleanup, test, root)
    for name, maker in makers:
        factory.add_maker(name, maker)
    return factory


def is_test_method(obj):
    return inspect.ismethod(obj) and obj.__name__.startswith('test')


def compose_make_makers(*funcs):

    def composed():
        makers = []
        for make_makers in funcs:
            makers.extend(make_makers())
        return makers

    return composed


def make_factory_maker(makers):

    def maker(factory):
        return factory.make_child_factory(makers)

    return maker


def _with_factory(make_makers):
    """Return a decorator for test methods or classes.

    Args:
        make_makers (callable): Return an iterable over (name, maker) pairs,
          where maker (callable): Return a fixture (arbitrary object) given
          Factory as single argument
    """

    def wrap(test_func):

        @functools.wraps(test_func)
        def wrapper(self, *args, **kwargs):
            factory = make_factory(
                self.addCleanup, test=self, root=None, makers=make_makers())
            return test_func(self, factory, *args, **kwargs)

        return wrapper

    def decorator(test_func_or_class):
        if inspect.isclass(test_func_or_class):
            class_ = test_func_or_class
            for name, method in inspect.getmembers(class_, is_test_method):
                wrapped_method = wrap(method)
                setattr(class_, name, wrapped_method)
            return class_
        else:
            method = test_func_or_class
            return wrap(method)

    return decorator


def with_factory(*make_makers_funcs):
    """Return a decorator for test methods or classes.

    The decorated test method or methods should take an extra factory argument:

    class Test(TransactionCase):
        @with_factory(fixtures.standard)
        def test_something(self, factory):
            ...

    @with_factory(fixtures.standard)
    class Test(TransactionCase):
        def test_something(self, factory)
            ...
        def test_something_else(self, factory)
            ...

    The arguments are callables that return an iterable over (name, maker)
      pairs, where:
      maker (callable): Return a fixture (arbitrary object) given
        Factory as single argument
    """
    make_all_makers = compose_make_makers(*make_makers_funcs)
    return _with_factory(make_all_makers)
