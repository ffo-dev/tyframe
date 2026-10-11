import ast
import importlib.util
import sys
from pathlib import Path
from types import ModuleType


def find_child_classes[T](
    file_path: str | Path,
    base_class: type[T],
) -> list[type[T]]:
    """Return class objects declared in the file that inherit from ``base_class``."""
    source_path = Path(file_path).resolve()
    module_ast = ast.parse(
        source_path.read_text(encoding="utf-8"),
        filename=str(source_path),
    )
    module = _load_module(source_path)
    namespace = vars(module)
    found: list[type[T]] = []

    for declaration in module_ast.body:
        if not isinstance(declaration, ast.ClassDef):
            continue
        candidate = namespace.get(declaration.name)
        if isinstance(candidate, type) and issubclass(candidate, base_class):
            found.append(candidate)

    return found


def _load_module(file_path: Path) -> ModuleType:
    for module in tuple(sys.modules.values()):
        module_path = getattr(module, "__file__", None)
        if isinstance(module_path, str) and Path(module_path).resolve() == file_path:
            return module

    module_name = f"_tyframe_class_finder_{abs(hash(file_path))}"
    spec = importlib.util.spec_from_file_location(module_name, file_path)
    if spec is None or spec.loader is None:
        raise ImportError(f"Cannot load Python module from {file_path}")

    module = importlib.util.module_from_spec(spec)
    sys.modules[module_name] = module
    try:
        spec.loader.exec_module(module)
    except BaseException:
        del sys.modules[module_name]
        raise
    return module
