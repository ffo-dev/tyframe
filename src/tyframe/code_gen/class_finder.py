import ast
import importlib
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
        source_path.read_text(encoding='utf-8'),
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
        module_path = getattr(module, '__file__', None)
        if (
            isinstance(module_path, str)
            and Path(module_path).resolve() == file_path
            and not module.__name__.startswith('_tyframe_class_finder_')
        ):
            return module

    for module_name in _module_names(file_path):
        try:
            module = importlib.import_module(module_name)
        except ModuleNotFoundError as error:
            if error.name is not None and (
                error.name == module_name or module_name.startswith(f'{error.name}.')
            ):
                continue
            raise
        module_path = getattr(module, '__file__', None)
        if isinstance(module_path, str) and Path(module_path).resolve() == file_path:
            return module

    raise ImportError(
        f'Cannot import {file_path} from any Python module path on sys.path'
    )


def _module_names(file_path: Path) -> list[str]:
    candidates: list[tuple[int, str]] = []
    for entry in sys.path:
        root = Path(entry or Path.cwd()).resolve()
        try:
            relative_path = file_path.relative_to(root)
        except ValueError:
            continue
        if relative_path.suffix != '.py':
            continue
        parts = list(relative_path.parts)
        parts[-1] = Path(parts[-1]).stem
        if parts[-1] == '__init__':
            parts = parts[:-1]
        if parts and all(part.isidentifier() for part in parts):
            candidates.append((len(root.parts), '.'.join(parts)))

    return [name for _, name in sorted(candidates, reverse=True)]
