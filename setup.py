import errno
from   os.path    import dirname, join
import re
from   setuptools import setup

with open(join(dirname(__file__), 'literal_exec.py')) as fp:
    for line in fp:
        m = re.search(r'^\s*__version__\s*=\s*([\'"])([^\'"]+)\1\s*$', line)
        if m:
            version = m.group(2)
            break
    else:
        raise RuntimeError('Unable to find own __version__ string')

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
    version=version,
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
