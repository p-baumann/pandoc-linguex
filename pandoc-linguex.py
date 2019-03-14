#!/usr/bin/env python3
"""
Preprocess Pandoc-flavored Markdown, 
replace numbered example lists (example_lists extension) with linguex.sty LaTeX code.

Output can be piped into pandoc to convert into LaTeX code
Sample pipe:
> python linguex.py document.md | pandoc -f markdown+example_lists+raw_tex -t latex

# Supported Markdown syntax and linguex LaTeX replacement:
## Main examples:
(@1) Lorem.        --> \ex. Lorem. \label{ex:[filename:]1}
@11. Ipsum.        --> \ex. Ipsum. \label{ex:[filename:]11}
(@example) Lorem.  --> \ex. Lorem. \label{ex:[filename:]example}

## Subexamples: 
Regular alphanumeric lists are translated into linguex subexamples if they are second-level of an example list, 
i.e. they are indented and immediately follow an item containing @:
@1. Main sentence
    a. Lorem
    b. Ipsum
-->
\ex. Main sentence 
\a. Lorem
\b. Ipsum

## Labels and references
Only labels that are actually used in references are inserted, 
all unused labels are deleted.
If the filename is known labels have the form
    {ex:filename:label}
otherwise
    {ex:label}
"""

# last edit: 2019-03-13
# Copyright 2019 by Peter Baumann
# This program can be redistributed and/or modified under the MIT license.


import argparse, re, sys

def replace_labels(lines, labels=None, prefix=None):
    """Replace dummy labels with actual labels if used. Othewise remove dummy"""
    newlines = []
    dummy_pattern = re.compile('####LABEL####([A-Za-z0-9-_]+)####')
    for line in lines:
        dummy_match = re.search(dummy_pattern, line)
        if dummy_match:
            label = dummy_match.groups()[0]
            if label in labels:
                if prefix:
                    full_label = f"ex:{prefix}:{label}"
                else:
                    full_label = f"ex:{label}"
                new_line = dummy_pattern.sub('\\\\label{' + full_label + '}', line)
            else:
                new_line = dummy_pattern.sub('', line)
            newlines.append(new_line)
        else:
            newlines.append(line)
    return newlines

def pandoc_to_linguex(lines, prefix=None):
    """Replace Pandoc example lists (and nested alphanumeric lists) with linguex LaTeX syntax, and insert dummy labels """
    ex_pattern = re.compile('\s*\(?@([A-Za-z0-9-_]*)[.)]\s+')
    ab_pattern = re.compile('\s+\(?([a-z]+)[.)]\s+')
    empty_pattern = re.compile('^\s*$')
    label_pattern = re.compile('\(@([A-Za-z0-9-_]+)\)')
    labels = set()
    within_ex = False
    newlines = []
    for line in lines:
        ex_match = re.match(ex_pattern, line)
        ab_match = re.match(ab_pattern, line)
        empty_match = re.search(empty_pattern, line)
        if ex_match:
            if within_ex:
                newlines.append('\n')
            else:
                within_ex = True
            label = ex_match.groups()[0]
            example_words = line.strip().split()[1:]
            new_line = '\\ex. ' + ' '.join(example_words)
            if label != '':
                dummy_label = f"####LABEL####{label}####"
                new_line += f"{dummy_label}\n"
            else:
                new_line += '\n'
            newlines.append(new_line)
        elif within_ex and ab_match:
            index = ab_match.groups()[0]
            example_words = line.strip().split()[1:]
            new_line = f"\\{index}. " + ' '.join(example_words) + '\n'
            newlines.append(new_line)
        elif within_ex and empty_match:
            within_ex = False
            newlines.append(line)
        else:
            label_match = re.search(label_pattern, line)
            if label_match:    
                label_iter = re.finditer(label_pattern, line)
                for l in label_iter:
                    labels.add(l.groups()[0])
                if prefix:
                    ref_label = f"ex:{prefix}:\\1"
                else:
                    ref_label = f"ex:\\1"
                subs = label_pattern.subn('\\\\ref{' + ref_label + '}', line)
                new_line = subs[0]
                newlines.append(new_line)
            else:
                newlines.append(line)
    return replace_labels(newlines, labels = labels, prefix=prefix)

if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="Turn Pandoc-style numbered examples (example_lists extension) into linguex LaTeX examples")
    parser.add_argument('input', nargs='?', type=argparse.FileType('r'), default=sys.stdin)
    parser.add_argument('output', nargs='?', type=argparse.FileType('w'), default=sys.stdout)
    args = parser.parse_args()

    lines = args.input.readlines()
    filename = args.input.name
    if filename != "<stdin>":
        prefix = filename.split('.')[0]
    else:
        prefix = None

    outlines = pandoc_to_linguex(lines, prefix=prefix)
    args.output.write(''.join(outlines))
    