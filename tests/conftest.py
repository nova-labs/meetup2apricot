"""Test fixtures."""

from pathlib import Path
import os
import pytest

@pytest.fixture(scope="module")
def module_dir_path(request):
    """Assure a directory exists in this module.
    The directory name is given by the environment variable
    combining the module name and "_DIR".  For example,
    module test_foo.py will use the environment variable
    named TEST_FOO_DIR.  Return the path to the directory
    or None if the environment variable is not set."""
    module_file_path = Path(request.module.__file__)
    env_var_name = "{}_{}".format(module_file_path.stem, "DIR").upper()
    module_dir_name = os.environ.get(env_var_name)
    if not module_dir_name:
        return None
    test_dir = module_file_path.parent
    module_dir = test_dir / module_dir_name
    module_dir.mkdir(mode = 0o775, exist_ok = True)
    return module_dir

@pytest.fixture()
def module_file_path(request, module_dir_path):
    """Return a path in the module's directory to a file
    named for the test function.  Skip the test if there
    is no module directory."""
    if module_dir_path is None:
        pytest.skip("No module directory for this test")
    test_name = request.function.__name__
    return module_dir_path / test_name

# vim: tabstop=8 expandtab shiftwidth=4 softtabstop=4 autoindent
