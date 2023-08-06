# Conditional Blocks for Foliant

This preprocessors lets you exclude parts of the source based on flags defined in the project config and environment variables.


## Installation

```shell
$ pip install foliantcontrib.flags
```


## Config

Enabled project flags are listed in `preprocessors.flags`:

```yaml
preprocessors:
  flags:
    - foo
    - bar
```

To set flags for the current session, define `FOLIANT_FLAGS` environment variable:

```shell
$ FOLIANT_FLAGS="spam, eggs"
```

You can use commas, semicolons, or spaces to separate flags.


## Usage

Conditional blocks are enclosed between `<<if>...</if>` tags:

```markdown
This paragraph is for everyone.

<<if flags="management">
This parapraph is for management only.
</if>
```

A block can depend on multiple flags. You can pick whether all tags must be present for the block to appear, or any of them (by default, `kind="all"` is assumed):

```markdown
<<if flags="spam, eggs" kind="all">
This is included only if both `spam` and `eggs` are set.
</if>

<<if flags="spam, eggs" kind="any">
This is included if both `spam` or `eggs` is set.
</if>
```

You can also list flags that must *not* be set for the block to be included:

```markdown
<<if flags="spam, eggs" kind="none">
This is included only if neither `spam` nor `eggs` are set.
</if>
```
