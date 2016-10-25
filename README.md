# abbreviations
A tool to find and expand abbreviations within a string. Designed for scientific writing.

This tool uses regular expressions to identify and expand abbreviations found in a string. This can be useful for counting terms within a scientific article when the relationship between full term and abbreviation is not known ahead of time.

We will also be using this to create dictionaries of abbreviations across a domain (cognitive neuroscience, in our case).

Abbreviations are expected to be presented using parentheses, as is standard in APA format. We will attempt to support similar likely scenarios, such as:
- full term (ABB) 
- full term (ABB; citation) 
- ~~ABB (full term)~~: Not currently supported.
- full term (aBB): Mixed-case abbreviations; fairly common with brain regions.

Once we've made some improvements and estimated the tool's accuracy, we will convert it to a Python package for mass consumption.

Usage
--

```python
from abbreviations import expandall

text = expandall(text)
```
