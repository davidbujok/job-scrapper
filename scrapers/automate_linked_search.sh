#!/bin/bash

# pairs=()
# for i in {1..10}; do
#     read -p "Enter first variable for pair $i: " var1
#     read -p "Enter second variable for pair $i: " var2
#     pairs+=("$var1 $var2")
# done
#
# for pair in "${pairs[@]}"; do
#     var1=$(echo $pair | cut -d ' ' -f 1)
#     var2=$(echo $pair | cut -d ' ' -f 2)
#     echo "First variable: $var1, Second variable: $var2"
#     echo -e "$var1\n$var2" | python /home/arch/repos/job-scrapper/scrapers/linkedin-scrape.py
#     echo pgrep firefox-bin | xargs kill
# done


job1='Junior Software Developer'
job2='Edinburgh'

echo -e "$job1\n$job2" | python /home/arch/repos/job-scrapper/scrapers/linkedin-scrape.py
echo pgrep firefox-bin | xargs kill

job1='Graduate Software Developer'
job2='Edinburgh'

echo -e "$job1\n$job2" | python /home/arch/repos/job-scrapper/scrapers/linkedin-scrape.py
echo pgrep firefox-bin | xargs kill

job1='Graduate Software Developer'
job2='Glasgow'

echo -e "$job1\n$job2" | python /home/arch/repos/job-scrapper/scrapers/linkedin-scrape.py
echo pgrep firefox-bin | xargs kill

job1='Junior Software Developer'
job2='Glasgow'

echo -e "$job1\n$job2" | python /home/arch/repos/job-scrapper/scrapers/linkedin-scrape.py
echo pgrep firefox-bin | xargs kill

job1='Junior Software Developer'
job2='Dunfermline'

echo -e "$job1\n$job2" | python /home/arch/repos/job-scrapper/scrapers/linkedin-scrape.py
echo pgrep firefox-bin | xargs kill

job1='Graduate Software Developer'
job2='Dunfermline'

echo -e "$job1\n$job2" | python /home/arch/repos/job-scrapper/scrapers/linkedin-scrape.py
echo pgrep firefox-bin | xargs kill

job1='Apprenticeship software developer'
job2='Edinburgh'

echo -e "$job1\n$job2" | python /home/arch/repos/job-scrapper/scrapers/linkedin-scrape.py
echo pgrep firefox-bin | xargs kill

job1='Apprenticeship network administrator' 
job2='Edinburgh'

echo -e "$job1\n$job2" | python /home/arch/repos/job-scrapper/scrapers/linkedin-scrape.py
echo pgrep firefox-bin | xargs kill
