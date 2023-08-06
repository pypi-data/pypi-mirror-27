# Makaron

A simple way to handle your version number.

Look at the homepage: [makaron.gitlab.io](http://makaron.gitlab.io/)

## Config

Makaron expect a `.makaron.yml` file in the current working directory.
This file list the files where Makaron has to update the version number.

You have to give Makaron two information. First the file where is supposed to search.
Second a regex that will let him find the line where is the version number.

You can update version number with this format `major.minor.patch` with the following `.makaron.yml` file.

```
setup.py: "__version__ = .*"
```

You can also choose to store your version number in different line with the following `.makaron.yml` file.

```
setup.py:
    major: "major = .*\n"
    minor: "minor = .*\n"
    patch: "patch = .*\n"
```

You can also add several files to update using different method, like so:

```
setup.py: "__version__ = .*"
lib/version.py:
    major: "major = .*\n"
    minor: "minor = .*\n"
    patch: "patch = .*\n"
```

You can also update different versions in the same file, doing this:

```
setup.py:
  - "__version__ = .*"
  - major: "major = .*\n"
    minor: "minor = .*\n"
    patch: "patch = .*\n"
```

## Update version

Just type the name of the number you want to increase:

```bash
$ makaron major
```
or

```bash
$ makaron minor
```

or

```bash
$ makaron patch
```

## Print the current version

Just type `makaron` in your prompt.
