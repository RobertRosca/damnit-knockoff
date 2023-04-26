import importlib.util
import inspect

from beanie import Document, UnionDoc


def load_user_context():
    spec = importlib.util.spec_from_file_location(
        "context", "/home/roscar/work/git.xfel.eu/roscar/damnit-knockoff/example.py"
    )

    assert spec is not None
    module = importlib.util.module_from_spec(spec)

    assert module is not None and spec.loader is not None
    spec.loader.exec_module(module)

    return module


def get_models():
    context = load_user_context()

    classes = inspect.getmembers(context, inspect.isclass)

    return [c[1] for c in classes if issubclass(c[1], (Document, UnionDoc))]
