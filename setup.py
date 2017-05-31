import errno
from   os.path      import dirname, join
from   setuptools   import setup
from   literal_exec import literal_execfile

metadata = literal_execfile(join(dirname(__file__), 'literal_exec.py'))

try:
    with open(join(dirname(__file__), 'README.rst')) as fp:
        long_desc = fp.read()
except EnvironmentError as e:
    if e.errno == errno.ENOENT:
        long_desc = None
    else:
        raise

setup(
    name='literal_exec',
    version=metadata["__version__"],
    py_modules=['literal_exec'],
    license=metadata["__license__"],
    author=metadata["__author__"],
    author_email=metadata["__author_email__"],
    keywords='parsing eval exec constants literals configfile ast variables',
    description=metadata["__doc__"].strip().splitlines()[0].strip(),
    long_description=long_desc,
    url=metadata["__url__"],

    python_requires='>=2.6, !=3.0.*, !=3.1.*, !=3.2.*, <4',

    install_requires=[],

    classifiers=[
        'Development Status :: 3 - Alpha',
        #'Development Status :: 4 - Beta',
        #'Development Status :: 5 - Production/Stable',

        'Programming Language :: Python :: 2',
        'Programming Language :: Python :: 2.6',
        'Programming Language :: Python :: 2.7',
        'Programming Language :: Python :: 3',
        'Programming Language :: Python :: 3.3',
        'Programming Language :: Python :: 3.4',
        'Programming Language :: Python :: 3.5',
        'Programming Language :: Python :: 3.6',
        'Programming Language :: Python :: Implementation :: CPython',
        'Programming Language :: Python :: Implementation :: PyPy',

        'License :: OSI Approved :: MIT License',
        'Intended Audience :: Developers',
        'Intended Audience :: Information Technology',
        'Topic :: Software Development :: Interpreters',
        'Topic :: Text Processing :: Filters',
    ],
)
