"""
Copy and paste data based on an element's `save()` and `load()` methods.

The `copy()` function will return all values serialized, either as string
values or reference id's.

The `paste()` function will resolve those values. Based on the elements
that are already in the model,

The copy() function returns only data that has to be part of the copy buffer.
the `paste()` function will load this data in a model.
"""

from __future__ import annotations

from functools import singledispatch
from typing import (
    Callable,
    Dict,
    NamedTuple,
    Optional,
    Set,
    Tuple,
    Type,
    TypeVar,
    Union,
)

import gaphas

from gaphor.core.modeling import Diagram, Element, Presentation
from gaphor.core.modeling.collection import collection

T = TypeVar("T")


@singledispatch
def copy(obj: Element) -> T:
    """
    Create a copy of an element (or list of elements).
    The returned type should be distinct, so the `paste()`
    function can properly dispatch.
    """
    raise ValueError(f"No copier for {obj}")


@singledispatch
def paste(copy_data: T, diagram: Diagram, lookup: Callable[[str], Element]):
    """
    Paste previously copied data. Based on the data type created in the
    `copy()` function, try to duplicate the copied elements.
    """
    raise ValueError(f"No paster for {copy_data}")


def serialize(value):
    if isinstance(value, (Element, gaphas.Item)):
        return ("r", value.id)
    elif isinstance(value, collection):
        return ("c", [serialize(v) for v in value])
    else:
        if isinstance(value, bool):
            value = int(value)
        return ("v", str(value))


def deserialize(ser, lookup):
    vtype, value = ser
    if vtype == "r":
        e = lookup(value)
        if e:
            yield e
    elif vtype == "c":
        # TODO: should apply elements to model one at a time
        for v in value:
            yield from deserialize(v, lookup)
    elif vtype == "v":
        yield value


class ElementCopy(NamedTuple):
    cls: Type[Element]
    id: Union[str, bool]
    data: Dict[str, Tuple[str, str]]


@copy.register
def copy_element(item: Element) -> ElementCopy:
    buffer = {}

    def save_func(name, value):
        # do not copy Element.presentation, to avoid cyclic dependencies
        if name != "presentation":
            buffer[name] = serialize(value)

    item.save(save_func)
    return ElementCopy(cls=item.__class__, id=item.id, data=buffer)


@paste.register
def paste_element(copy_data: ElementCopy, diagram, lookup):
    cls, id, data = copy_data
    item = diagram.model.create_as(cls, id)
    for name, ser in data.items():
        for value in deserialize(ser, lookup):
            item.load(name, value)
    item.postload()
    return item


class PresentationCopy(NamedTuple):
    cls: Type[Element]
    data: Dict[str, Tuple[str, str]]


@copy.register
def _copy_presentation(item: Presentation) -> PresentationCopy:
    buffer = {}

    def save_func(name, value):
        buffer[name] = serialize(value)

    item.save(save_func)
    return PresentationCopy(cls=item.__class__, data=buffer)


@paste.register
def _paste_presentation(copy_data: PresentationCopy, diagram, lookup):
    cls, data = copy_data
    item = diagram.create(cls)
    for name, ser in data.items():
        for value in deserialize(ser, lookup):
            item.load(name, value)
    item.canvas.update_matrices([item])
    item.postload()
    return item


class CopyData(NamedTuple):
    items: Dict[str, object]
    elements: Dict[str, object]


@copy.register
def _copy_all(items: set) -> CopyData:
    return CopyData(
        items={item.id: copy(item) for item in items},
        elements={
            item.subject.id: copy(item.subject)
            for item in items
            if isinstance(item, Presentation) and item.subject
        },
    )


@paste.register
def _paste_all(copy_data: CopyData, diagram, lookup) -> Set[Presentation]:
    new_items: Dict[str, Presentation] = {}
    new_elements: Dict[str, Optional[Element]] = {}

    # element_lookup prefers elements already in the model
    def element_lookup(ref: str):
        if ref in new_elements:
            return new_elements[ref]
        looked_up = lookup(ref)
        if looked_up:
            return looked_up
        if ref in copy_data.elements:
            new_elements[ref] = None
            new_elements[ref] = paste(copy_data.elements[ref], diagram, element_lookup)
            return new_elements[ref]

    # item_lookup copies items. Elements are looked up
    def item_lookup(ref: str):
        if ref in new_items:
            return new_items[ref]
        elif ref in copy_data.items:
            new_items[ref] = paste(copy_data.items[ref], diagram, item_lookup)
            return new_items[ref]
        return element_lookup(ref)

    for old_id, data in copy_data.items.items():
        if old_id in new_items:
            continue
        new_items[old_id] = paste(data, diagram, item_lookup)

    return set(new_items.values())
