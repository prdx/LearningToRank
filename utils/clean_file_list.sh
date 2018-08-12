#!/bin/bash

cd /home/prdx/Documents/CS6200-Summer/A6/AP_DATA/ 
tail -n+3 doclist_new_0609.txt | sed -e 's/^[0-9]\+\s\s//g' > processed_doclist.txt

