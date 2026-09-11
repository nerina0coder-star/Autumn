import copy
from inspect import isclass
import threading
from warnings import warn

from markupsafe import escape

from Autumn.abstract_base import AbstractBase
from Autumn.decorators import no_lock


class AbstractTag(AbstractBase):
    type _comparison = AbstractTag | int | float
    __hash__ = object.__hash__

    __no_new__ = True

    def __init__(self):
        """
        The base of most, if not all, of tags in Autumn.
        Be aware that dynamic is based on children's status.
        If none of the children are dynamic, it defaults to False.
        """

        self._lock = threading.RLock()

        # Please note that this is because user's code is unpredictable, therefore using RLock's flexibility
        # is REQUIRED. Even I consider RLock a code smell, but in this case, it cannot be helped.

        self._reverse_addition = False  # reverse addition
        self._mock_cls = None

        if not (hasattr(self, "tags") and isinstance(self.tags, list)):
            self.tags = []
        if not (hasattr(self, "identifier") and isinstance(self.identifier, str)):
            self.identifier = None
        if not (hasattr(self, "classes") and isinstance(self.classes, list)):
            self.classes = []
        if not (hasattr(self, "_cache") and isinstance(self._cache, list)):
            self._cache = []
        if not (hasattr(self, "worth") and isinstance(self.worth, (float, int))):
            self.worth = 0

        if not (hasattr(self, "name") and isinstance(self.name, str)):
            self.name = ""
        if not (hasattr(self, "attributes") and isinstance(self.attributes, dict)):
            self.attributes = {}
        if not (hasattr(self, "closable") and isinstance(self.closable, bool)):
            self.closable = False

        if not (
                hasattr(self, "preferred_parent") and
                self.preferred_parent is not None and  # type: ignore
                isinstance(self.preferred_parent, AbstractTag
                           )
        ):
            def default():
                return []

            self.preferred_parent = default

        self.dynamic = getattr(self, "dynamic", False) or any(  # type: ignore[annotation-unchecked,unused-ignore]
            tag.dynamic if isinstance(tag, AbstractTag) else False for tag in self.tags  # type: ignore[has-type]
        )

    def identifiers(self):
        """
        Returns all identifiers.
        """

        out = []

        if self.identifier:
            out.append(self.identifier)

        for i in self.tags:
            if isinstance(i, AbstractTag):
                out.extend(i.identifiers())

        return out

    def duplicate_identifiers(self):
        """
        Catches duplicate identifiers.

        :return: The duplicates.
        """

        identifiers = self.identifiers()
        checked = []
        duplicates = []

        for i in identifiers:
            if i not in checked:
                checked.append(i)
                continue

            if i in duplicates:
                continue

            duplicates.append(i)

        return duplicates

    def delete_cache(self):
        """
        Deletes all the caches for build, and all the caches from the
        children tags.
        """

        self._cache.clear()
        for i in self.tags:
            if isinstance(i, AbstractTag):
                try:
                    i.delete_cache()
                except RecursionError:
                    break

    def build(self, cache_if_possible = True, /, **kwargs):
        """
        Builds the tag and all sub tags.

        :param cache_if_possible: If true, the returned value will be cached if this tag is not dynamic.
        :param kwargs: The kwargs to pass to all sub tags.
        :return: The built tag.
        """

        if kwargs.get("recursion", 0) > 512:
            raise RecursionError("Recursion depth exceed(512). Please lower the nesting.")

        if not self.dynamic and self._cache:
            return self._cache[-1]

        if not (
            kwargs.get("prod", False) or kwargs.get("production", False)
        ):
            err = []
            if any(i.startswith("on") for i in self.attributes.keys()):
                err.append(f"Use of on attribute in class {self.__class__.__name__}. Please don't use on* attributes, instead, "
                     f"use javascript's addEventListener, as it can introduce XSS security issues.")

            if "style" in self.attributes:
                err.append(f"Use of style attribute in class {self.__class__.__name__}. Please use a CSS stylesheet, as inline "
                     f"style attributes are hard to find and manage in a huge DOM, and can introduce CSS Injection issues.")

            if err:
                e = "".join(f"{e}\n" for e in err)

                if kwargs.get("strict", False):
                    raise ValueError(e)
                warn(e)

        if (result := self.before_build(**kwargs)) is not None:
            if cache_if_possible and not self._cache and not self.dynamic:
                self._cache.append(result)
            return result

        name = self.name
        closable = self.closable
        tags = self.tags.copy()
        dynamic = self.dynamic
        attributes = self.attributes.copy()
        classes = self.classes.copy()
        identifier = str(self.identifier) if self.identifier is not None else None


        all_ = [f"<{name}"]
        if classes:
            all_.append(f' class="{"".join(f"{cls} " for cls in self.classes)}"')
        if identifier:
            all_.append(f' id="{self.identifier}"')
        if attributes:
            for attr, val in attributes.items():
                attr = escape(attr.replace(" ", ""))
                if val == True:
                    # Do not simplify. We want to see if the val is LITERALLY True.
                    # But if we do "if val", it will be the same for a string, a list, etc.
                    all_.append(f' {attr}')
                    continue
                all_.append(f' {attr}="{escape(str(val))}"')

        all_.append(f">")

        if closable:
            if tags:
                for tag in tags:
                    all_.append(f"{tag.build(dynamic if cache_if_possible else False, recursion=kwargs.get("recursion", 0) + 1, **kwargs)
                    if isinstance(tag, AbstractTag) else tag}")
            all_.append(f"</{name}>")

        out = "".join(all_)

        if not self.dynamic and cache_if_possible and not self._cache:
            self._cache.append(out)

        return out

    def _new(self):
        """
        Used when trying to create a new instance from the class of this instance.

        :return: A new tag, exactly like self.
        """

        return copy.deepcopy(self)

    def __mul__(self, other):
        """
        Multiplies this tag by `other` times.

        :param other: An int to multiply self by.
        :return: A list or the preferred parent.
        """
        if not isinstance(other, int):
            raise TypeError(f"Expected int, but given {type(other).__name__}")

        out = []

        for i in range(other - 1):
            mock = self._new()
            out.append(mock)
        lst = [*out, self]
        parent = self._resolve_parent(lst)

        return parent

    @no_lock
    def __rmul__(self, other):
        """
        Same as tag * other.

        :param other: An int to multiply self by.
        :return: The result of the multiplication.
        """
        return self * other

    def __add__(self, other):
        """
        Adds together the given tags.
        :param other: The others to join.
        :return: The self + other(prepended) in a list or the preferred parent.
        """
        return self._shared_plus(other)

    def __radd__(self, other):
        """
        Same as self + other, but reversed.
        :param other: The other to join.
        :return: The other + self(appended) in a list or the preferred parent.
        """
        self._reverse_addition = True
        return self._shared_plus(other)

    def __lshift__(self, other):
        """
        Puts other in self(append).
        :param other: The one to put in self's tags.
        :return: Self, for chaining operations.
        """
        self.tags.append(other)
        return self

    @no_lock
    def __rrshift__(self, other):
        """
        Same as self << other.
        :param other: The one to put in self's tags.
        :return: Self, for chaining operations.
        """
        return self << other

    def __sub__(self, other):
        """
        Removes the given other from the tags. The given other can be
        a type of AbstractTag, or a list of type of AbstractTags.
        This function will remove instances of the other in order from end to start,
        one for each class.

        Example:
            where tags = sequence of div1, div2, div3, p1, p2, span1, div4, span2
            where tags is my_tag.tags
            when my_tag - [Div, Div, Span, P]
            changed tags to sequence of div1, div2, p1, span1

        :return: The ones not removed, for any reasons.
        """
        if isinstance(other, type):
            other = [other]
        else:
            other = copy.deepcopy(other)


        def do(tag):
            allowed = not any(isinstance(tag, j) for j in other)
            if not allowed:
                other.remove(type(tag))
            return allowed

        new = list(reversed(
            list(filter(do, reversed(self.tags)))
        ))
        self.tags = new

        return other

    def __eq__(self, other):
        """
        Checks if worth of self is equal to the other or the other's worth.

        :param other: Int, Float, or AbstractTag.
        :return: True or False.
        """
        return self.worth == (other.worth if isinstance(other, AbstractTag) else other)

    def __ne__(self, other):
        """
        Same as not self == other.
        """
        return not self == other

    def __lt__(self, other):
        """
        Checks if worth of self is less than the other or the other's worth.

        :param other: Int, Float, or AbstractTag.
        :return: True or False.
        """
        return self.worth < (other.worth if isinstance(other, AbstractTag) else other)

    def __gt__(self, other):
        """
        Same as not (self < other or self == other)
        """
        return self.worth > (other.worth if isinstance(other, AbstractTag) else other)

    def __le__(self, other):
        """
        Same as self < other or self == other
        """
        return self < other or self == other

    def __ge__(self, other):
        """
        Same as self > other or self == other
        """
        return self > other or self == other

    def __contains__(self, item):
        """
        Checks if item or any instance of it is in self.tags.
        :param item: a class for instance check or an instance for literal check.
        :return: True or False.
        """
        if not (isinstance(item, AbstractTag) or issubclass(item, AbstractTag) or isinstance(item, str)):
            raise ValueError(f"expected (type of or instance of) AbstractTag, or str, but given {item}")

        if isclass(item):
            if issubclass(item, AbstractTag):
                return any(issubclass(type(i), item) for i in self.tags)
        return item in self.tags

    def _resolve_parent(self, lst):
        """
        Does NOT hold the lock, assuming it is already held.
        Resolves a parent after an arithmetic operation(e.g., mul/add).
        """

        if isinstance((parent := self.preferred_parent()), AbstractTag):
            # ----------------------------
            parent.tags.extend(lst)
            # -----------------------------
        elif isinstance((parent := self.preferred_parent()), (list, set, dict, tuple)):
            # -----------------------------
            if isinstance(parent, list):
                parent.extend(lst)
            elif isinstance(parent, set):
                for i in lst:
                    parent.add(i)
            elif isinstance(parent, dict):
                for i in range(len(parent), len(lst) + len(parent)):
                    parent[i] = lst[i]
            else:
                parent = copy.deepcopy(lst)
            # -----------------------------
        else:
            parent = copy.deepcopy(lst)
        return parent

    def _shared_plus(self, other):
        out = None

        if isinstance(other, AbstractTag):
            out = self._resolve_parent([self, other] if not self._reverse_addition else [other, self])
        elif isinstance(other, list):
            out = self._resolve_parent([self, *other] if not self._reverse_addition else [*other, self])

        self._reverse_addition = False

        return out

