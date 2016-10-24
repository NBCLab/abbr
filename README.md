# abbreviation-expansion
A tool to expand abbreviations detected within a string. Designed for scientific writing.

This tool uses regular expressions to identify and expand abbreviations found in a string. This can be useful for counting terms within a scientific article when the relationship between full term and abbreviation is not known ahead of time.

Abbreviations are expected to be presented using parentheses, as is standard in APA format. We will attempt to support similar likely scenarios, such as:
- full term (ABBV) <-- Standard
- full term (ABBV; citation) <-- Likely
- ABBV (full term) <-- Rarer
- full term (aBBV) <-- Mixed-case abbreviations; fairly common with brain regions

Once we've made some improvements and estimated the tool's accuracy, we will convert it to a Python package for mass consumption.
