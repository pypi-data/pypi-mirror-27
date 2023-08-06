# pip-upgrade-all

Author: [Michael Kim](http://michaelkim0407.com) <mkim0407@gmail.com>

***IMPORTANT*** This package has been merged into [mklibpy-bin](https://github.com/MichaelKim0407/mklibpy/tree/master/mklibpy-bin) (v0.8) and is now inactive. Please install that package instead.

## Compatibility

This script only runs on Python 3, however it supports upgrading `pip2` packages.

`pip` version must be at least 9.

## Installation

```
pip3 install mkpipU
```

## Usage

```
pip-upgrade-all PATH_TO_PIP [...]
```

e.g.

```
pip-upgrade-all pip2 pip3
```

will upgrade all packages for `pip2` and `pip3`.

## License

MIT
