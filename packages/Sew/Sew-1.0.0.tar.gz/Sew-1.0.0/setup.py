try:
    from setuptools import setup
except ImportError:
    from distutils.core import setup
import sys

if sys.version_info.major == 2:
    raise RuntimeError(
        "Python 2 not supported! Maybe run `pip3 install sew`?"
    )

setup(
    name="Sew",
    description="Python threading tools",
    version="1.0.0",

    url="https://github.com/coal0/sew",

    license="MIT",

    classifiers=[
        "Development Status :: 5 - Production/Stable",
        "License :: OSI Approved :: MIT License",
        "Programming Language :: Python :: 3",
        "Intended Audience :: Developers",
        "Topic :: Software Development"
    ],
    keywords=["sew", "thread", "threading"],

    packages=["sew"]
)
