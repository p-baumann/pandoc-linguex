---
title: "Pandoc to linguex examples"
header-includes:
- \usepackage{linguex}
---

# Numbered examples in Markdown

Numbered examples can look like this:

(@1) Example one
(@2) Example two

We can also embed alphanumeric lists within example lists

(@A) Let's embed.
    a. Embedded example one
    b. Embedded example two.

The period syntax works as well:

@four. Example four.

We can reference (@four) and (@2), and also forward (@last).
Even with some intervening text.

(@last) Is two.

Regular numbered lists keep their own numbering.

1. First list item
2. Second list item

But maybe this is confusing.
Anyway, we can refer back to (@1).
