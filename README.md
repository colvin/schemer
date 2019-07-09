# NAME

`schemer` -- compose SQL schema definitions from component files

# SYNOPSIS

```
schemer [-p PATH] [-o FILE] [-m JSON] [-f FILE]
schemer -h
```

# DESCRIPTION

`schemer` composes a single stream of SQL from multiple SQL file sources using
ordering rules and performs macro replacement.

A directory structure like the following is expected:

```
  prefix/
  |-- ORDER
  |-- PROLOGUE.sql
  |-- EPILOGUE.sql
  |-- one/
  |   |-- ORDER
  |   |-- PROLOGUE.sql
  |   |-- EPILOGUE.sql
  |   |-- A.sql
  |   |-- B.sql
  |   `-- ...
  `-- two/
      |-- ORDER
      |-- PROLOGUE.sql
      |-- EPILOGUE.sql
      |-- X.sql
      |-- Y.sql
      `-- ...
```

The top-level _prefix_ directory must contain a file named `ORDER`. This file
contains an ordered list of one or more directory names, one per line,
corresponding to child directories of the prefix. This defines the order in
which directories are processed. Each child directory generally corresponds to
a schema.

Each child directory must also contain a file named `ORDER`. This file contains
an ordered list of one or more file patterns, one per line. Each pattern should
match one or more file names within that child directory, using explicit paths
rooted in that directory and/or globs. This `ORDER` file defines the order in
which files are concatenated within this directory.

If files match multiple patterns within the child directory `ORDER` file, each
file will only be processed once, and will be processed at its earliest
appearance in the order.

If a file named `PROLOGUE.sql` exists within the prefix directory, it is
processed as the first file in the sequence. If a file named `EPILOGUE.sql`
exists, it is processed as the very last file in the sequence. Similarly, each
child directory may also contain a `PROLOGUE.sql` and/or `EPILOGUE.sql` file,
which are placed at the very beginning and very end of the sequence for that
child directory.

Once the order has been determined, each file is processed for macros and
emitted to standard output (or a file if `-o FILE` is used).

Macros are identified by the pattern `MACRO{KEY}`, where `KEY` is the name of a
macro key. Macros are replaced using key/value definitions taken from a macro
file (using `-f FILE`), JSON data (using `-m JSON`), or the environment.

Macro files use a simple line-wise `key = value` syntax. No quote interpolation
is used, so any quotes in the value is considered part of the value.

Macro JSON is converted directly into a dictionary. The following will define
the macro `FOO` (which appears as `MACRO{FOO}` in the SQL files) as the value
`1`, while the macro `BAR` (`MACRO{BAR}`) will be defined as the value `bar`.

```
{"FOO":1,"BAR":"bar"}
```

If a macro is present in a SQL file and the macro key cannot be resolved, a
`KeyError` is raised and the process fails. Note that because output is
produced as files are processed an error can result in incomplete output.

# OPTIONS

- `-p PATH, --path PATH` path to the prefix directory
- `-o FILE, --output FILE` write output to the given file
- `-m JSON, --macro JSON` define macros in a JSON string
- `-f FILE, --macro-file FILE` read the given file for macro definitions

# DEVELOPER SETUP

This project uses a git filter to place CVS-style ID tags into certain source
files when they are checked out. The tags are replaced with their placeholder,
(the `$Id$` comment that appears near the beginning of the file) when commits
are pushed to Github. This is useful for determining the exact version of the
program that is installed.

In order for this to work, the git configuration needs to be updated to
reference this project's embedded `.gitconfig`. Once the repository has been
cloned, run the `make config` command to set this up, and then run `make
rcs-tag` to ensure the tags are properly set.

# LICENSE

This program is provide under the terms of the BSD 2-clause License.
