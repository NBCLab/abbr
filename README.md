# abbreviations
A tool to find and expand abbreviations within a string. Designed for scientific writing.

This tool uses regular expressions to identify and expand abbreviations found in a string. This can be useful for counting terms within a scientific article when the relationship between full term and abbreviation is not known ahead of time.

We will also be using this to create dictionaries of abbreviations across a domain (cognitive neuroscience, in our case).

Abbreviations are expected to be presented using parentheses, as is standard in APA format.

Currently supported:
- full term (FT): Simple acronym.
- full term (FT; citation): Acronym followed by citation(s).
- full term (fT): Mixed-case acronym.
- full term (fT; citation): Mixed-case acronym followed by citation(s).

Currently unsupported:
- FT (full term): Acronym followed by term.
- Non-acronymic abbreviations.

Once we've made some improvements and estimated the tool's accuracy, we will convert it to a Python package for mass consumption!

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
