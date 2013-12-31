#/usr/bin/env sh
bmn-mgrast.py -t scan "*phage" -so starphage.tsv
bmn-mgrast.py -t scan "*viral" -so starviral.tsv
bmn-mgrast.py -t scan "*virome" -so starvirome.tsv
bmn-mgrast.py -t scan "*virus" -so starvirus.tsv
bmn-mgrast.py -t scan "virome" -so virome.tsv
bmn-mgrast.py -t scan "vir*" -so virstar.tsv
bmn-mgrast.py -t scan "virio*" -so viriostar.tsv

cat *.tsv | sed '/^status/d' | sort -u > all.tsv

cut -f18 all.tsv | sort -u > allProjects

# make a per project folder and download data

wd=`pwd`
for p in `cat allProjects`;
do
	cd $wd
	mkdir -p $p; cd $p
	bmn-mgrast.py -t details $p > $p.txt
	grep $p ../all.tsv | cut -f19 > $p.metagenomes
	for m in `cat $p.metagenomes`;
	do
		bmn-mgrast.py -t download -s all $m
	done
done

	
