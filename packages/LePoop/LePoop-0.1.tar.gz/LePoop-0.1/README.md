# Le Poop
An undo for your pip commands, inspired by [nvbn](http://github.com/nvbn/)'s [The Fuck](http://github.com/nvbn/thefuck) (no affiliation). Why use `Le Poop`? Take an `install`, for example. It can come with a slew of dependencies, and `pip uninstall` graciously allows you to remove your new package, and all its friends, one by one. `Le Poop` cleans up *all* the mess, in one go.



`Le Poop` supports undos for the only three `pip` commands it makes sense to undo:

- `pip install`: Uninstall packages that were *just* installed. Leaves older packages intact, unless `poop` is run successively.
- `pip download`: Removes tarballs and wheels for the just-downloaded package and all its dependencies.
- `pip uninstall`: Reinstall the package in question.

## Installation

To get started, install using pip.

```
pip install lepoop
```

Then, run `poop` after any `pip` command you regret.
