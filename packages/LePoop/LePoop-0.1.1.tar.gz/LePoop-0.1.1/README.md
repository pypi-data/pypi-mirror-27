# Le Poop 💩
An undo for your pip commands. Why use `Le Poop` instead of `uninstall`? Take any `install`. It can come with a slew of dependencies, and `pip uninstall` graciously allows you to remove your new package, and all its friends, one by one. `Le Poop` cleans up *all* the mess with a single command, `poop`. To get started, install using pip.

```
pip install lepoop
```

Then, run `poop` after any `pip` command you regret.

![lepoop-3](https://user-images.githubusercontent.com/2068077/34505328-70ad999a-efd9-11e7-8300-06c57ecc2927.gif)

More examples:

```
→ $ poop md2py tex2py  # auto-remove, no matter installed how long ago
Packages md2py are not installed. I'm ignoring them.
pip uninstall -y pptree tex2py texsoup [enter/ctrl+c]
Uninstalling pptree-2.0:
  Successfully uninstalled pptree-2.0
Uninstalling tex2py-0.0.4:
  Successfully uninstalled tex2py-0.0.4
Uninstalling TexSoup-0.1:
  Successfully uninstalled TexSoup-0.1
```

```
→ $ pip install datascience
Collecting datascience
...
Successfully installed coveralls-0.5 datascience-0.10.3 folium-0.1.5 sphinx-1.6.5

→ $ pip install tex2py
Collecting tex2py
...
Successfully installed TexSoup-0.1 coveralls-1.1 pptree-2.0 tex2py-0.0.4

→ $ poop --skip 1
pip uninstall -y sphinx folium datascience [enter/ctrl+c]
Uninstalling Sphinx-1.6.5:
  Successfully uninstalled Sphinx-1.6.5
Uninstalling folium-0.1.5:
  Successfully uninstalled folium-0.1.5
Uninstalling datascience-0.10.3:
  Successfully uninstalled datascience-0.10.3

→ $ poop
pip uninstall -y tex2py pptree texsoup [enter/ctrl+c]
Uninstalling TexSoup-0.1:
  Successfully uninstalled TexSoup-0.1
Uninstalling tex2py-0.0.4:
  Successfully uninstalled tex2py-0.0.4
Uninstalling pptree-2.0:
  Successfully uninstalled pptree-2.0
```

```
→ $ pip download md2py
Collecting md2py
  Using cached md2py-0.0.1.tar.gz
  Saved ./md2py-0.0.1.tar.gz
Collecting markdown (from md2py)
  Using cached Markdown-2.6.10.zip
  Saved ./Markdown-2.6.10.zip
Collecting beautifulsoup4 (from md2py)
  Using cached beautifulsoup4-4.6.0-py3-none-any.whl
  Saved ./beautifulsoup4-4.6.0-py3-none-any.whl
Successfully downloaded md2py markdown beautifulsoup4

...a day passes...

→ $ ls
Markdown-2.6.10.zip			donttouchme.tar.gz
beautifulsoup4-4.6.0-py3-none-any.whl	md2py-0.0.1.tar.gz

→ $ poop
Already pooped. (No undoable pip commands.)

→ $ poop --harder
rm md2py-0.0.1.tar.gz Markdown-2.6.10.zip beautifulsoup4-4.6.0-py3-none-any.whl [enter/ctrl+c]

→ $ ls
donttouchme.tar.gz
```

`Le Poop` supports undos for the only three `pip` commands it makes sense to undo:

- `pip install`: Uninstall packages that were *just* installed. Leaves older packages intact, unless `poop` is run successively.
- `pip download`: Removes tarballs and wheels for the just-downloaded package and all its dependencies.
- `pip uninstall`: Reinstall the package in question.

```
usage: poop [-h] [-a] [--harder] [--stronger] [--skip SKIP]
            [package [package ...]]

positional arguments:
  package      packages to uninstall

optional arguments:
  -h, --help   show this help message and exit
  -a, --alias  Alias to `poop`
  --harder     Look through bash history as far as possible.
  --stronger   Look through bash history and module source files for modules
               to uninstall.
  --skip SKIP  Number of pip commands to skip.
```

### Inspiration (Rated R) 🤭

Inspired by [nvbn](http://github.com/nvbn/)'s [The Fuck](http://github.com/nvbn/thefuck) (no affiliation). I initially wanted to name this repository `The Shit`. The command-line utility would be `shit`, and if the app had no suggestions, it'd respond `no shit`. Ultimately decided to keep it PG. `Poop` is closer to `pip` in edit distance any how.
