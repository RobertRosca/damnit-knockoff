import asyncio
import importlib.util
import inspect
from types import FunctionType
from typing import Any, Type

from beanie import Document, Insert, before_event
from pydantic import Extra, create_model


class BaseRun(Document, extra=Extra.allow):
    proposal: int
    run: int
    comment: str


def load_user_context():
    """Load the context file as a module."""
    spec = importlib.util.spec_from_file_location(
        "context",
        "/home/roscar/work/github.com/RobertRosca/damnit-knockoff/context.py",
    )

    assert spec is not None
    module = importlib.util.module_from_spec(spec)

    assert module is not None and spec.loader is not None
    spec.loader.exec_module(module)

    return module


def pseudo_property_decorator(func):
    async def wrapper(self, *args, **kwargs):
        if asyncio.iscoroutinefunction(func):
            val = await func(self, *args, **kwargs)
        else:
            val = func(self, *args, **kwargs)

        setattr(self, func.__name__, val)

    return wrapper


def parse_methods_as_fields(cls: Type[Document]):
    """Read class methods, prepend "def_" to their name, using the return type
    annotation of the method create a field with the same name and type."""
    fields: dict[str, tuple[Type, Any]] = {}
    methods: dict[str, FunctionType] = {}

    for method in inspect.getmembers(cls, inspect.isfunction):
        if method[0].startswith("_") or method in inspect.getmembers(
            BaseRun, inspect.isfunction
        ):
            continue

        if annotation := method[1].__annotations__.get("return", None):
            fields[method[0]] = (annotation, None)
            methods["def_" + method[0]] = method[1]

    new_cls = create_model(
        cls.__name__,
        __base__=cls.__base__,
        __module__=cls.__module__,
        **fields,
    )

    for name, method in methods.items():
        decorated = pseudo_property_decorator(method)
        decorated = before_event(Insert)(decorated)
        setattr(new_cls, name, decorated)

    return new_cls


def get_classes():
    context = load_user_context()

    classes = inspect.getmembers(context, inspect.isclass)

    return [c[1] for c in classes if issubclass(c[1], Document)]


def get_models():
    classes = get_classes()

    return [parse_methods_as_fields(cls) for cls in classes if cls != BaseRun]


MODELS = get_models()
