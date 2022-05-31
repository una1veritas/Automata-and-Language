#!/bin/sh

echo "starting tests..."


for t in 1 2 3
do 
    echo $t
    unzip -c words.txt.zip | gshuf > words_shuf.txt
    for wc in 10000 15000 25000 40000 65000 100000 150000 250000 400000 
    do 
    	for adc in 2000
	   	do
			for rep in 1 2 3
			do 
			    echo "file $t, $wc words, add $adc words, iteration $rep, \c"
		    	cat words_shuf.txt | ./acm.exe -n $wc -x $adc -p - 
			done
		done
    done
done
echo "done."