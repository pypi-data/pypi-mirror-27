[![travis build](https://img.shields.io/travis/jvrana/magicdir.svg)](https://travis-ci.org/jvrana/magicdir)
[![Coverage Status](https://coveralls.io/repos/github/jvrana/magicdir/badge.svg?branch=master)](https://coveralls.io/github/jvrana/magicdir?branch=master)
[![PyPI version](https://badge.fury.io/py/REPO.svg)](https://badge.fury.io/py/REPO)
[![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg)](https://opensource.org/licenses/MIT)


#### Build/Coverage Status
Branch | Build | Coverage
:---: | :---: | :---:
**master** | [![travis build](https://img.shields.io/travis/jvrana/magicdir/master.svg)](https://travis-ci.org/jvrana/magicdir/master) | [![Coverage Status](https://coveralls.io/repos/github/jvrana/magicdir/badge.svg?branch=master)](https://coveralls.io/github/jvrana/magicdir?branch=master)
**development** | [![travis build](https://img.shields.io/travis/jvrana/magicdir/development.svg)](https://travis-ci.org/jvrana/magicdir/development) | [![Coverage Status](https://coveralls.io/repos/github/jvrana/magicdir/badge.svg?branch=development)](https://coveralls.io/github/jvrana/magicdir?branch=development)

# 📁 MagicDir 📁

Dealing with paths and directories isn't rocket science, but it can be a pain. **MagicDir** allows you to build directory trees by treating
your directory tree as a first-class object.


Stop writing your directory trees like this:
```python
# define paths
top = os.path.abspath('top')
middle = os.path.join(str(top), 'middle')
bottom = os.path.join(str(middle), 'bottom')
os.makedirs(bottom)
with open(os.path.join(bottom, 'bottomlog.txt', 'w') as f:
    f.write("some log information")
```

And start writing them like this:
```python
# define paths
env = MagicDir('top').add('middle').add('bottom').root
env.bottom.write('log.txt', 'w', 'some log information')
```

Live usage:

![live_example](images/magicdir_example.gif?raw=true)

Its very easy to create, move, or delete directory trees. For example, the following builds the directory
skeleton for this repo.

![demo](images/directory_example.png?raw=true)

```python
from magicdir import *

# create folder structure
env = MagicDir('magicdir')
env.add('magicdir', alias='core')
env.core.add('tests')
env.tests.add('env')
env.tests.add('env2')

# make the directory
env.set_dir(Path(__file__).absolute().parent)
env.mkdirs()

# write some files
env.write('README.md', 'w', '# Magic Dir\nThis is a test readme file')
env.core.write("__init__.py", "w", "__version__ = \"1.0\"")
```

Other things you can do:

Abstracting the directory structure lets your create, remove, copy, move directory trees easily.

![rmdirs_example](images/rmdirs_example.gif?raw=true)

All paths are easily accessible.

```python
print(env.test.abspath) # absolute path
print(env.test.path) # relative path
```

You can even read and write files intuitively.

```python
# writes file to 'test' folder
env.test.write('test.txt', 'w', 'some data')

# reads test file
env.test.read('test.txt', 'r')

 # open file and read lines
env.test.open('test.txt', 'r').readlines()
```

All iterables are magically chainable making it easy to do complex things. Pretty cool!

```python
# recurseively write a log file to all subfolders of 'core'
env.core.descendents.write('log.txt', 'w', 'some log file')

# read all files named 'log.txt' for subfolders in 'test'
env.test.children.read('log.txt', 'r')

# readlines files named 'log.txt' for subfolders in 'test'
env.test.children.open('log.txt', 'r').readlines()

# recursively get stats on folders
d = env.descendents()
zip(d, d.stat().st_mtime)
```

Better documentation about chaining methods is soon to come along with recipes.

# Installation

Installation via pip is the easiest way...

```bash
pip install magicdir
```

# Basic usage

Use `add` to create folders.

```python
from magicdir import *

env = MagicDir('bin')
env.add('subfolder1')
env.add('subfolder2')
env.print()

>>>
*bin
|   *subfolder1
|   *subfolder2
```

Functions return MagicDir objects and so can be chained together.
```python
env = MagicDir('bin')
env.add('subfolder1').add('subsubfolder')
env.print()

>>>
*bin
|   *subfolder1
|   |   *subsubfolder
```

Add can be chained together
```python
env = MagicDir('bin')
env.add('subfolder1').add('subsubfolder')
env.print()

>>>
*bin
|   *subfolder1
|   |   *subsubfolder
```

Folders create accesible MagicDir attributes automatically. Alternative attribute names can be set using
'alias='

```python
env = MagicDir('bin')
env.add('subfolder1')
env.subfolder1.add('misc')
env.subfolder1.misc.add('.hidden', alias='hidden')
env.subfolder1.misc.hidden.add('hiddenbin')
env.print()

*bin
|   *subfolder1
|   |   *misc
|   |   |   *.hidden ("hidden")
|   |   |   |   *hiddenbin

```

By default, attributes are *pushed* back the the root directory. The following is equivalent to above.

```python
env = MagicDir('bin')
env.add('subfolder1')
env.subfolder1.add('misc')
env.misc.add('.hidden', alias='hidden')
env.hidden.add('hiddenbin')
env.print()

*bin
|   *subfolder1
|   |   *misc
|   |   |   *.hidden ("hidden")
|   |   |   |   *hiddenbin

```

# Making, moving, copying, and deleting directories

The location of the root folder can be set by `set_bin`

```python
env.set_bin('../bin')
```

Directories can be created, deleted, copied or moved using `mkdirs`, `cpdirs`, `mvdirs`, `rmdirs`

```python
env.mkdirs()
env_copy = env.cpdirs()
# you can do stuff with env_copy independently
env.mvdirs('~/Document')
env_copy.rmdirs()
```

# Advanced usage

All iterables return special list-like objects that can be chained in one-liners.

```python
env.descendents() # returns a MagicList object

# find all txt files
env.descendents(include_self=True).glob("*.txt")

# recursively change permissions for directories
env.abspaths.chmod(0o444)
```
