#!/usr/bin/env python
"""Django's command-line utility for administrative tasks."""
import os
import subprocess
import sys
from pathlib import Path

BASE_DIR = Path(__file__).resolve().parent
VENV_DIR = BASE_DIR / '.venv'
VENV_PYTHON = VENV_DIR / ('Scripts/python.exe' if os.name == 'nt' else 'bin/python')


def _running_in_target_venv():
    # Compare sys.prefix (the venv's own directory), not sys.executable:
    # a venv's bin/python is usually a symlink to the base interpreter, so
    # resolving executables makes a venv and its base interpreter look
    # identical.
    return Path(sys.prefix).resolve() == VENV_DIR.resolve()


def _bootstrap_venv():
    """Create ./.venv (if missing) and install dependencies into it."""
    if not VENV_DIR.exists():
        print(f"No virtual environment found; creating one at {VENV_DIR} ...", file=sys.stderr)
        subprocess.run([sys.executable, '-m', 'venv', str(VENV_DIR)], check=True)

        requirements = BASE_DIR / 'requirements-dev.txt'
        if not requirements.exists():
            requirements = BASE_DIR / 'requirements.txt'
        print(f"Installing dependencies from {requirements.name} ...", file=sys.stderr)
        subprocess.run(
            [str(VENV_PYTHON), '-m', 'pip', 'install', '-q', '-r', str(requirements)],
            check=True,
        )


def main():
    """Run administrative tasks."""
    os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'src.settings')

    # Transparently create/use the project's local virtual environment so
    # nobody has to remember to activate one by hand. Docker builds set
    # MANAGE_PY_SKIP_VENV since they already install dependencies globally.
    if not _running_in_target_venv() and not os.environ.get('MANAGE_PY_SKIP_VENV'):
        _bootstrap_venv()
        os.execv(str(VENV_PYTHON), [str(VENV_PYTHON), str(BASE_DIR / 'manage.py'), *sys.argv[1:]])

    try:
        from django.core.management import execute_from_command_line
    except ImportError as exc:
        raise ImportError(
            "Couldn't import Django. Are you sure it's installed and "
            "available on your PYTHONPATH environment variable? Did you "
            "forget to activate a virtual environment?"
        ) from exc
    execute_from_command_line(sys.argv)


if __name__ == '__main__':
    main()
