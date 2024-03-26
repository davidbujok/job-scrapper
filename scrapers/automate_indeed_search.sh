#!/bin/bash

swaymsg workspace 10
job1='Junior Software Developer'
job2='Edinburgh'

echo -e "$job1\n$job2" | python indeed-scrape.py
swaymsg workspace 10
echo pgrep firefox-bin | xargs kill

job1='Graduate Software Developer'
job2='Edinburgh'

echo -e "$job1\n$job2" | python indeed-scrape.py
swaymsg workspace 10
echo pgrep firefox-bin | xargs kill

job1='Graduate Software Developer'
job2='Glasgow'

echo -e "$job1\n$job2" | python indeed-scrape.py
swaymsg workspace 10
echo pgrep firefox-bin | xargs kill

job1='Junior Software Developer'
job2='Glasgow'

echo -e "$job1\n$job2" | python indeed-scrape.py
swaymsg workspace 10
echo pgrep firefox-bin | xargs kill

job1='Junior Software Developer'
job2='Dunfermline'

echo -e "$job1\n$job2" | python indeed-scrape.py
swaymsg workspace 10
echo pgrep firefox-bin | xargs kill

job1='Graduate Software Developer'
job2='Dunfermline'

echo -e "$job1\n$job2" | python indeed-scrape.py
swaymsg workspace 10
echo pgrep firefox-bin | xargs kill

job1='Apprenticeship software developer'
job2='Edinburgh'

echo -e "$job1\n$job2" | python indeed-scrape.py
swaymsg workspace 10
echo pgrep firefox-bin | xargs kill

job1='Apprenticeship network administrator' 
job2='Edinburgh'

echo -e "$job1\n$job2" | python indeed-scrape.py
swaymsg workspace 10
echo pgrep firefox-bin | xargs kill
