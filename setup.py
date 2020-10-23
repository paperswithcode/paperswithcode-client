import io
from setuptools import setup, find_packages
from paperswithcode import __version__

name = "paperswithcode-client"
author = "Viktor Kerkez"
author_email = "alefnula@gmail.com"
url = "https://github.com/paperswithcode/paperswithcode-client"


setup(
    name=name,
    version=__version__,
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
