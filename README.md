# abbreviations

A tool to find and expand abbreviations within a string. Designed for scientific writing.

This tool uses regular expressions to identify and expand abbreviations found in a string. This can be useful for counting terms within a scientific article when the relationship between full term and abbreviation is not known ahead of time.

We will also be using this to create dictionaries of abbreviations across a domain (cognitive neuroscience, in our case).

Abbreviations are expected to be presented using parentheses, as is standard in APA format.

Currently supported:
- Initialisms/Acronyms in parentheses: E.g., full term (FT)
  - This includes acronyms using non-initial letters: E.g., full term (fuTE)
  - All letters within the abbreviation must occur in the words preceding the abbreviation's first use.
- The above, with citations after the abbreviation: E.g., full term (FT; Example et al., 2016)

Next steps
--
Ultimately, we would like to shift away from regular expressions toward NLP and ML, but we have no immediate plans to do so.

Disclaimer
--
We've developed this project primarily in order to learn about building small scientific projects in Python, continuous integration, and test-driven development. We still plan to provide support as needed. PRs and issues welcome.

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
