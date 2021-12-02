import io
import importlib
from pathlib import Path
from setuptools import setup, find_packages


name = "paperswithcode-client"
author = "Viktor Kerkez"
author_email = "alefnula@gmail.com"
url = "https://github.com/paperswithcode/paperswithcode-client"


def get_version():
    """Import the version module and get the project version from it."""
    version_py = Path(__file__).parent / "paperswithcode" / "version.py"
    spec = importlib.util.spec_from_file_location("version", version_py)
    version = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(version)
    return version.__version__


setup(
    name=name,
    version=get_version(),
    author=author,
    author_email=author_email,
    maintainer=author,
    maintainer_email=author_email,
    description="Python client for paperswithcode.com API.",
    long_description=io.open("README.md", "r", encoding="utf-8").read(),
    long_description_content_type="text/markdown",
    url=url,
    platforms=["Windows", "POSIX", "MacOSX"],
    license="Apache-2.0",
    packages=find_packages(),
    install_requires=io.open("requirements.txt").read().splitlines(),
    entry_points="""
        [console_scripts]
        pwc=paperswithcode.__main__:app
    """,
)
