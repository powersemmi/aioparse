#!/bin/env python3
class Borg(object):
    _dict = None

    def __new__(cls, *args, **kwargs):
        obj = super().__new__(cls, *args, **kwargs)
        if cls._dict is None:
            cls._dict = obj.__dict__
        else:
            obj.__dict__ = cls._dict
        return obj


if __name__ == '__main__':
    borg = Borg()
    borg.lol = 6757575

    new_borg = Borg()
    print(new_borg.lol)

