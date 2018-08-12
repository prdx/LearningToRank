#!/bin/bash

# This script is intended to append a root tag in our dataset
# We are using BeautifulSoup to parse the data
# If we don't add the root tag, then BeautifulSoup simply read the first tag
# For example, in:
# <Node></Node><Node></Node><Node></Node>
# Only one node will be parsed by the BeautifulSoup

cd /home/prdx/Documents/CS6200-Summer/A1/AP_DATA/ap89_collection/ 

for d in ap*; do
  echo '<DOCS>' | cat - ${d} > temp && mv temp ${d}
  echo '</DOCS>' >> ${d}
done
