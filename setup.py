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
    license='MIT',
    author='John Thorvald Wodder II',
    author_email='literal-exec@varonathe.org',
    ###keywords='',
    ###description='',
    long_description=long_desc,
    url='https://github.com/jwodder/literal_exec',

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

        ###
    ],
)
