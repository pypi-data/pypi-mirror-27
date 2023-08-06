import sys
from setuptools import setup

packages = ['mod', 'pkg']

if any('bdist' in arg for arg in sys.argv):
    from nuitka_setuptools import Nuitka, Compile

    build_settings = dict(
        # Compile module
        cmdclass={'build_ext': Nuitka},
        ext_modules=Compile(packages),
    )
else:
    build_settings = {}

setup(
    name='nuitka_setuptools_test',
    py_modules=['mod'],
    packages=['pkg'],
    description='Test module build for nuitka_setuptools',
    author='Andrew Leech',
    author_email='andrew@alelec.net',
    url='https://gitlab.com/alelec/nuitka-setuptools',
    version="0.1",
    include_package_data=True,
    **build_settings
)