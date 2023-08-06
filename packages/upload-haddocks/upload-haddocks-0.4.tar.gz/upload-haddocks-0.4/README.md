# upload-haddocks by Richard Cook

[![View on PyPI](https://img.shields.io/pypi/v/upload-haddocks.svg)](https://pypi.python.org/pypi/upload-haddocks)
[![Licence](https://img.shields.io/badge/license-MIT-blue.svg)](https://raw.githubusercontent.com/rcook/upload-haddocks/master/LICENSE)

Simple script that fixes hyperlinks in Haskell documentation generated using
`stack haddock` and then uploads it to the appropriate location on [Hackage][hackage]

## Clone repository

```
git clone https://github.com/rcook/upload-haddocks.git
```

## Developer notes

Various package properties are defined in `upload-haddocks/__init__py`:

* `__project_name__`
* `__version__`
* `__description__`

When publishing a new build of the package, ensure that `__version__` is incremented as appropriate.

## Licence

[MIT License][licence]

Released under [MIT License][licence]

[licence]: LICENSE
[hackage]: http://hackage.haskell.org/
