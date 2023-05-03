import asyncio
import importlib.util
import inspect
from functools import wraps
from pathlib import Path
from types import FunctionType
from typing import Any, Callable, Type

from beanie import Document, before_event
from beanie.odm.actions import EventTypes
from pydantic import create_model

from damnit_knockoff.db import Run


def load_user_context(file: Path):
    """Load the context file as a module."""
    spec = importlib.util.spec_from_file_location("context", file)

    assert spec is not None
    module = importlib.util.module_from_spec(spec)

    assert module is not None and spec.loader is not None
    spec.loader.exec_module(module)

    return module


def field(
    *args,
    direction: Callable = before_event,
    event: EventTypes = EventTypes.INSERT,
):
    def decorator(func):
        @wraps(func)
        async def wrapper(self, *args, **kwargs):
            if asyncio.iscoroutinefunction(func):
                val = await func(self, *args, **kwargs)
            else:
                val = func(self, *args, **kwargs)
            setattr(self, func.__name__, val)

        wrapped = direction(event)(wrapper)
        wrapped.__is_field__ = True
        return wrapped

    if len(args) == 1 and callable(args[0]):
        return decorator(args[0])
    else:
        return decorator


def parse_methods_as_fields(cls: Type[Document]):
    """Read class methods, prepend "def_" to their name, using the return type
    annotation of the method create a field with the same name and type."""
    fields: dict[str, tuple[Type, Any]] = {}
    methods: dict[str, FunctionType] = {}

    for method in inspect.getmembers(cls, inspect.isfunction):
        if any(
            [
                method[0].startswith("_"),
                method in inspect.getmembers(Run, inspect.isfunction),
            ]
        ):
            continue

        if annotation := method[1].__annotations__.get("return", None):
            if hasattr(method[1], "__is_field__"):
                fields[method[0]] = (annotation, None)
                methods["def_" + method[0]] = method[1]

    new_cls = create_model(
        cls.__name__,
        __base__=cls.__base__,
        __module__=cls.__module__,
        **fields,
    )

    for method, func in methods.items():
        setattr(new_cls, method, func)

    return new_cls


def get_classes(file: Path = Path("./context.py")) -> list[Type[Document]]:
    context = load_user_context(file)

    classes = inspect.getmembers(context, inspect.isclass)

    return [c[1] for c in classes if issubclass(c[1], Document)]


def get_models(file: Path = Path("context.py")) -> list[Type[Document]]:
    classes = get_classes(file)

    return [parse_methods_as_fields(cls) for cls in classes if cls != Run]


MODELS = get_models()
