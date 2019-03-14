# pandoc-linguex

Preprocess Pandoc-flavored Markdown,
replace numbered example lists (`example_lists` extension) with `linguex.sty` LaTeX code.

Output can be piped into pandoc to convert into LaTeX code.

## Usage

Call `linguex.py` with Markdown file as argument and pipe output into `pandoc`.
If no input file is provided, `linguex.py` reads from `stdin`.

Sample calls for example files:
```bash
> python linguex.py example.md | pandoc -f markdown+example_lists+raw_tex -o example.tex
> python linguex.py example.md | pandoc -f markdown+example_lists+raw_tex -o example.pdf
```

## Supported Markdown syntax and `linguex` LaTeX replacement
See also [example.md](example.md) for an illustration of most of the supported syntax.
### Example items
Markdown numbered example items correspond to `linguex` example items:
```markdown
(@1) Lorem ipsum.
@11. Ipsum lorem.
```
```latex
\ex. Lorem ipsum. \label{ex:[filename:]1}

\ex. Ipsum lorem. \label{ex:[filename:]11}

```

### Subexamples:
Regular alphanumeric lists are translated into `linguex` subexamples if they are second-level of an example list,
i.e. they are indented and immediately follow an item containing @:
```
@1. Lorem ipsum dolor.
    a. Lorem?
    b. Ipsum?
```

```latex
\ex. Lorem ipsum dolor.
\a. Lorem?
\b. Ipsum?

```

### Labels and references
Only labels that are actually used in references are inserted,
all unused labels are deleted.
If `linguex.py` is called with an input file as argument, the filename will become part of the label:
```
    {ex:filename:label}
```
Otherwise (i.e. if input is `stdin`) the label contains just the prefix `ex`:
```
    {ex:label}
```

## FAQ

### Why is this not a filter?
Pandoc inserts example numbers as raw text during Markdown parsing, so the labels are lost and a filter cannot determine if a reference to an example is actually a reference or just a number looking like a reference.
