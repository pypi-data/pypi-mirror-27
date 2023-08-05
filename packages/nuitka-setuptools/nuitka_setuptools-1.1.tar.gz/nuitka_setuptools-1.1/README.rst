=================
nuitka-setuptools
=================

Extension to setuptools to run your package through nuitka to produce compiled, faster, obfuscated binary modules.

Nuitka [http://nuitka.net/pages/overview.html] is a python compiler with full language support and CPython compatibility.

    It's fully compatible with Python 2.6, 2.7, 3.2, 3.3, 3.4, 3.5, and 3.6.

    You feed it your Python app, it does a lot of clever things, and spits out an executable or extension module.

This module provides some hooks to add to your python packages setup.py to automatically run some/all of your code
through nuitka when building a binary dist. This will typically be done with `python setup.py bdist_wheel` to
create a wheel for distribution.

With nuitka-setuptools this wheel can be devoid of pure python and only contain compiled code which is not only faster
(quote: Nuitka is more than 2 times faster than CPython) but has a relatively high level of code security.

Basic Usage: setup.py::

    from setuptools import setup
    from nuitka_setuptools import Nuitka, Compile


    setup(
        name='nuitka_setuptools',
        py_modules=['nuitka_setuptools'],
        description='Extension to setuptools to run your package through nuitka to '
                    'produce compiled, faster, obfuscated binary modules.',
        long_description=long_description,
        author='Andrew Leech',
        author_email='andrew@alelec.net',
        url='https://gitlab.com/alelec/nuitka-setuptools',
        use_scm_version=True,
        include_package_data=True,
        install_requires=install_requires,
        setup_requires=['setuptools_scm'],
        cmdclass={'build_ext': Nuitka},
        ext_modules=Compile(['nuitka_setuptools'])
    )
