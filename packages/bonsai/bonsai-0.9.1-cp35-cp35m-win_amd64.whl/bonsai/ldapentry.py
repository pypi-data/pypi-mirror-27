from enum import IntEnum
from typing import Union

from ._bonsai import ldapentry
from .errors import InvalidDN
from .ldapdn import LDAPDN
from .ldapvaluelist import LDAPValueList

class LDAPModOp(IntEnum):
    """ Enumeration for LDAP modification operations. """
    ADD = 0  #: For adding new values to the attribute.
    DELETE = 1  #: For deleting existing values from the attribute list.
    REPLACE = 2  #: For replacing the existing attribute values.

class LDAPEntry(ldapentry):
    def __init__(self, dn: Union[LDAPDN, str], conn=None) -> None:
        try:
            super().__init__(str(dn), conn)
            self.__extended_dn = None
        except InvalidDN:
            # InvalidDN error caused by extended DN control.
            splitted_dn = str(dn).split(';')
            super().__init__(splitted_dn[-1], conn)
            self.__extended_dn = dn

    def delete(self, timeout: float = None,
               recursive: bool=False) -> Union[bool, int]:
        """
        Remove LDAP entry from the dictionary server.

        :param float timeout: time limit in seconds for the operation.
        :param bool recursive: remove every entry of the given subtree \
        recursively.
        :return: True, if the operation is finished.
        :rtype: bool
        """
        res = self.connection.delete(self.dn, timeout, recursive)
        for value in self.values():
            value.status = 2
        return res

    def modify(self, timeout: float = None) -> Union[bool, int]:
        """
        Send entry's modifications to the dictionary server.

        :param float timeout: time limit in seconds for the operation.
        :return: True, if the operation is finished.
        :rtype: bool
        """
        return self.connection._evaluate(super().modify(), timeout)

    def rename(self, newdn: Union[str, LDAPDN],
               timeout: float = None) -> Union[bool, int]:
        """
        Change the entry's distinguished name.

        :param str|LDAPDN newdn: the new DN of the entry.
        :param float timeout: time limit in seconds for the operation.
        :return: True, if the operation is finished.
        :rtype: bool
        """
        if type(newdn) == LDAPDN:
            newdn = str(newdn)
        return self.connection._evaluate(super().rename(newdn), timeout)

    def update(self, *args, **kwds) -> None:
        """
        Update the LDAPEntry with the key/value pairs from other, overwriting existing keys.
        (Same as dict's update method.)
        """
        if args:
            if hasattr(args[0], "keys"):
                # Working with a dict on the parameter list.
                for key, value in args[0].items():
                    self.__setitem__(key, value)
            else:
                # Working with a sequence.
                for tup in args[0]:
                    if len(tup) != 2:
                        raise ValueError("Sequence element has more then 2 element.")
                    self.__setitem__(tup[0], tup[1])
        if kwds:
            # Key/value pairs are listed on the parameter list.
            for key, value in kwds.items():
                self.__setitem__(key, value)

    def clear(self) -> None:
        """ Remove all items from the dictionary. """
        keys = list(self.keys())
        for key in keys:
            del self[key]

    def get(self, key, default=None):
        """
        Return the value for `key` if `key` is in the LDAPEntry,
        else `default`. (Same as dict's get method.)
        """
        try:
            return self[key]
        except KeyError:
            return default

    def pop(self, *args):
        """
        LDAPEntry.pop(k[,d]) -> v, remove specified key and return the
        corresponding value. If key is not found, d is returned if given,
        otherwise KeyError is raised.

        :param key: the key.
        :param dflt: if key is not found, d is returned.
        :return: the value from the LDAPEntry.
        """
        if len(args) > 2:
            raise TypeError("pop expected at most 2 arguments, got %d" % len(args))
        try:
            key = args[0]
            value = self[key]
            del self[key]
            return value
        except IndexError:
            raise TypeError("pop expected at least 1 arguments, got 0")
        except KeyError as err:
            try:
                dflt = args[1]
                return dflt
            except IndexError:
                raise err

    def popitem(self):
        """
        LDAPEntry.popitem() -> (k, v), remove and return some (key, value)
        pair as a 2-tuple; but raise KeyError if LDAPEntry is empty.
        """
        try:
            key = list(self.keys()).pop(0)
            value = self[key]
            del self[key]
            return (key, value)
        except IndexError:
            raise KeyError("popitem(): LDAPEntry is empty")

    def __eq__(self, other):
        """
        Two LDAPEntry objects are considered equals, if their DN is the same.

        :param other: the other comparable object.
        :return: True if the two object are equals.
        :rtype: bool
        """
        if isinstance(other, self.__class__):
            return self.dn == other.dn
        else:
            return super().__eq__(other)

    def _status(self):
        status = {}
        for key, value in self.items():
            status[key] = value._status_dict
        status['@deleted_keys'] = self.deleted_keys
        return status

    @property
    def extended_dn(self):
        """
        The extended DN of the entry. It is None, if the extended DN control
        is not set or not supported. The attribute is read-only.
        """
        return self.__extended_dn

    @extended_dn.setter
    def extended_dn(self, value):
        raise ValueError("Extended_dn attribute cannot be set.")

    def change_attribute(self, name: str, optype: int, *values) -> None:
        """
        Change an attribute of the entry with explicit LDAP modification type
        by listing the values as parameters.
        An attribute can be removed entirely if the `optype` is delete and no
        `values` are passed.
        This method can be useful for changing write-only attributes (e.g.
        passwords).

        :param str name: the name of the attribute.
        :param int optype: the operation type, 0 for adding, 1 for deleting \
        and 2 for replacing. An :class:`LDAPModOp` also can be used as value.
        :param \*values: the new value or values of the attribute.
        """
        lvl = self.get(name, LDAPValueList())
        if optype == LDAPModOp.ADD:
            lvl.added.extend(values)
        elif optype == LDAPModOp.DELETE:
            if len(values) == 0:
                self.__setitem__(name, None)
                del self[name]
                return
            else:
                lvl.deleted.extend(values)
        elif optype == LDAPModOp.REPLACE:
            lvl.extend(values)
        else:
            raise ValueError("Wrong operation type.")
        self[name] = lvl
        lvl.status = 2 if optype == 2 else 1

    def clear_attribute_changes(self, name: str) -> None:
        """
        Clear all added and deleted changes of an attribute.

        :param str name: the name of the attribute.
        """
        lvl = self.get(name, LDAPValueList())
        lvl.added.clear()
        lvl.deleted.clear()
        self[name] = lvl
        lvl.status = 0
