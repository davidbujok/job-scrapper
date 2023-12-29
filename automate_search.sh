#!/bin/bash

job1='Junior Software Developer'
job2='Edinburgh'

echo -e "$job1\n$job2" | python linkedin-scrape.py
echo pgrep firefox-bin | xargs kill

job1='Graduate Software Developer'
job2='Edinburgh'

echo -e "$job1\n$job2" | python linkedin-scrape.py
echo pgrep firefox-bin | xargs kill

job1='Graduate Software Developer'
job2='Glasgow'

echo -e "$job1\n$job2" | python linkedin-scrape.py
echo pgrep firefox-bin | xargs kill

job1='Junior Software Developer'
job2='Glasgow'

echo -e "$job1\n$job2" | python linkedin-scrape.py
echo pgrep firefox-bin | xargs kill

job1='Junior Software Developer'
job2='Dunfermline'

echo -e "$job1\n$job2" | python linkedin-scrape.py
echo pgrep firefox-bin | xargs kill

job1='Graduate Software Developer'
job2='Dunfermline'

echo -e "$job1\n$job2" | python linkedin-scrape.py
echo pgrep firefox-bin | xargs kill
