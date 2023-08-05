"""I'm throwing this in because it is often useful in testing.

I often find module mock from the standard library overcomplicated for my
purposes.
"""


class MonkeyPatcher(object):

    _unset = object()

    def __init__(self, add_cleanup):
        self._add_cleanup = add_cleanup

    def monkey_patch(self, obj, name, value):
        orig_value = getattr(obj, name, self._unset)
        def revert():
            if orig_value is self._unset:
                delattr(obj, name)
            else:
                setattr(obj, name, orig_value)
        setattr(obj, name, value)
        self._add_cleanup(revert)
        return orig_value

    def add_to_list(self, list_, value):
        was_there_before = value in list_
        def revert():
            try:
                list_.remove(value)
            except ValueError:
                pass
        if not was_there_before:
            list_.append(value)
            self._add_cleanup(revert)
        return was_there_before
