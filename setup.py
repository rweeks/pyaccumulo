#!/usr/bin/env python
# -*- coding: utf-8 -*-
#

import os

try:
    import subprocess
    has_subprocess = True
except:
    has_subprocess = False

try:
    from ez_setup import use_setuptools
    use_setuptools()
except ImportError:
    pass

try:
    from setuptools import setup
except ImportError:
    from distutils.core import setup

from distutils.cmd import Command

import version

long_description = """pyaccumulo is a python client library for Apache Accumulo that uses the Accumulo Thrift Proxy"""


class rpm(Command):
    description = "builds a RPM package"
    user_options = []

    def initialize_options(self):
        pass

    def finalize_options(self):
        pass

    def run(self):
        if has_subprocess:
            status = subprocess.call(["python", "setup.py", "bdist_rpm", "--install-script", "rpm-install-script.sh"])

            if status:
                raise RuntimeError("RPM build failed")

            print ""
            print "RPM built"
        else:
            print """
`setup.py rpm` is not supported for this version of Python.

Please ask in the user forums for help.
"""

class doc(Command):
    description = "generate or test documentation"
    user_options = [("test", "t",
                     "run doctests instead of generating documentation")]
    boolean_options = ["test"]

    def initialize_options(self):
        self.test = False

    def finalize_options(self):
        pass

    def run(self):
        if self.test:
            path = "doc/_build/doctest"
            mode = "doctest"
        else:
            path = "doc/_build/%s" % __version__
            mode = "html"

            try:
                os.makedirs(path)
            except:
                pass

        if has_subprocess:
            status = subprocess.call(["sphinx-build", "-b", mode, "doc", path])

            if status:
                raise RuntimeError("documentation step '%s' failed" % mode)

            print ""
            print "Documentation step '%s' performed, results here:" % mode
            print "   %s/" % path
        else:
            print """
`setup.py doc` is not supported for this version of Python.

Please ask in the user forums for help.
"""


setup(
      name = 'pyaccumulo',
      version = version.get_git_version(),
      author = 'Jason Trost',
      author_email = 'jason.trost AT gmail.com',
      maintainer = 'Jason Trost',
      maintainer_email = 'jason.trost AT gmail.com',
      description = 'Python client library for Apache Accumulo',
      long_description = long_description,
      url = 'https://github.com/accumulo/pyaccumulo',
      keywords = 'accumulo client db distributed thrift',
      packages = ['pyaccumulo',
                  'pyaccumulo.iterators',
                  'pyaccumulo.proxy'
                  ],
      install_requires = ['thrift'],
      py_modules=['ez_setup'],
      cmdclass={"doc": doc, "rpm": rpm},
      classifiers=[
          'Development Status :: 3 - Alpha',
          'Intended Audience :: Developers',
          'License :: OSI Approved :: Apache Software License',
          'Natural Language :: English',
          'Operating System :: OS Independent',
          'Programming Language :: Python',
          'Programming Language :: Python :: 2',
          'Programming Language :: Python :: 2.6',
          'Programming Language :: Python :: 2.7',
          'Programming Language :: Python :: 2 :: Only',
          'Topic :: Software Development :: Libraries :: Python Modules'
          ]
      )
