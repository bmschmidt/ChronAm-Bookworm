targets = $(addprefix downloads/,$(shell curl http://chroniclingamerica.loc.gov/ocr.json | perl -ne 'if (m/"name": ?"(.*)"/) {print "$$1\n"}'))

all: bookworm/bookworm.cnf $(targets)

downloads/%.tar.bz2:
	mkdir -p downloads
	-curl -f -o $@ $(subst downloads/,http://chroniclingamerica.loc.gov/data/ocr/,$@)

bookworm/files/texts/input.txt:
	mkdir -p bookworm/files/texts
	ln -s ../../../input.txt  bookworm/files/texts/input.txt

bookworm/files/metadata/jsoncatalog.txt:	
	mkdir -p bookworm/files/texts
	ln -s ../../../jsoncatalog.txt $@

jsoncatalog.txt:
#The page metadata is spit out from the raw files.
	python parseBZ2.py downloads | tee input.txt | python makePageMetadata.py > jsoncatalog.txt

input.txt: jsoncatalog.txt

bookworm:
	git clone git@github.com:bmschmidt/Presidio bookworm
	cd bookworm; git checkout lessDiskSpace

bookworm/bookworm.cnf: bookworm
	python bookworm/scripts/makeConfiguration.py
	mv bookworm.cnf bookworm/bookworm.cnf

newspapers.rdf:
	curl -o newspapers.rdf http://chroniclingamerica.loc.gov/newspapers.rdf


