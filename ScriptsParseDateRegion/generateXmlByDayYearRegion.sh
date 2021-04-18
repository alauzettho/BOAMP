#!/bin/bash

cd resultsTest

for d in 40 64 33 47;
do
	for y in {2007..2021};
	do
		for m in 01 02 03 04 05 06 07 08 09 10 11 12;
		do
			(curl -X GET --header 'Accept: application/xml' "http://api.dila.fr/opendata/api-boamp/annonces/search?criterion=(numerodepartement:$d%20AND%20dateparution:$y/$m)") > file_${d}_${y}_${m}.xml
		done;
	done;
done;
	
cd ..
