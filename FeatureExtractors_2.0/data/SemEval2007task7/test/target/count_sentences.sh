#!/bin/bash
cat $1 | grep instance | grep "d00$2" | cut -d'.' -f2 | uniq |wc -l