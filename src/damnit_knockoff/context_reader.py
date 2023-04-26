import importlib.util
import inspect
from typing import Type

from beanie import Document, Insert, before_event
from pydantic import Extra, create_model


class BaseRun(Document, extra=Extra.allow):
    proposal: int
    run: int
    comment: str


def load_user_context():
    """Load the context file as a module."""
    spec = importlib.util.spec_from_file_location(
        "context", "/home/roscar/work/git.xfel.eu/roscar/damnit-knockoff/context.py"
    )

    assert spec is not None
    module = importlib.util.module_from_spec(spec)

    assert module is not None and spec.loader is not None
    spec.loader.exec_module(module)

    return module


def parse_methods_as_fields(cls: Type[Document]):
    """Read class methods, prepend "def_" to their name, using the return type
    annotation of the method create a field with the same name and type."""
    fields = {}
    methods = {}

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
        # __validators__=cls.__validators__,
        # **cls.__dict__["__annotations__"],
        **fields,
    )

    for method in methods:
        decorated = before_event(Insert)(methods[method])
        setattr(new_cls, method, decorated)

    return new_cls


def get_classes():
    context = load_user_context()

    classes = inspect.getmembers(context, inspect.isclass)

    return [c[1] for c in classes if issubclass(c[1], Document)]


def get_models():
    classes = get_classes()

    return [parse_methods_as_fields(cls) for cls in classes if cls != BaseRun]


MODELS = get_models()
