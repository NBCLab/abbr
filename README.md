# abbreviations 

A tool to find and expand abbreviations within a string. Designed for scientific writing.

This tool uses regular expressions to identify and expand abbreviations found in a string. This can be useful for counting terms within a scientific article when the relationship between full term and abbreviation is not known ahead of time.

We will also be using this to create dictionaries of abbreviations across a domain (cognitive neuroscience, in our case).

Abbreviations are expected to be presented using parentheses, as is standard in APA format.

Currently supported:
- Acronyms in parentheses: full term (FT)
- Abbreviations in parentheses: full term (fuTE)
  - All letters within the abbreviation must occur in the words preceding the abbreviation's first use.
- The above, with citations after the abbreviation: full term (FT; Salo et al., 2016)

Currently unsupported:
- FT (full term): Acronym followed by term.
- Probably many other kinds of abbreviations.

Once we've made some improvements and estimated the tool's accuracy, we will convert it to a Python package for mass consumption!

Status
--
[![Build Status](https://travis-ci.com/emdupre/abbreviations.svg?token=DqydGcufv4xDUqpFRaEx&branch=master)](https://travis-ci.com/emdupre/abbreviations)

Installation
--
```shell
cd /desired/location/of/package/
git clone git@github.com:NBCLab/abbreviations.git
cd abbreviations/

# for users:
python setup.py install

# for developers:
python setup.py develop
```

Usage
--

```python
from abbreviations import expandall

text = expandall(text)
```
