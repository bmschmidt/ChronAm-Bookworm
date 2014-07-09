#locFiles = $(shell curl http://chroniclingamerica.loc.gov/ocr.json | perl -ne 'if (m/"name": ?"(.*)"/) {print "$$1\n"}')
locFiles = $(shell cat ocr.json | perl -ne 'if (m/"name": ?"(.*)"/) {print "$$1\n"}')
targets = $(addprefix downloads/,$(locFiles))

baseNames = $(basename $(basename $(locFiles)))
catalogs = $(addsuffix .txt.gz, $(addprefix jsoncatalogs/,$(baseNames)))
txts = $(addsuffix .txt.gz, $(addprefix inputfiles/,$(baseNames)))



parsedness: $(catalogs)


jsoncatalogs/%.txt.gz: downloads/%.tar.bz2
	mkdir -p jsoncatalogs inputfiles
	python parseBZ2.py $<

inputfiles/%.txt.gz: jsoncatalogs/%.txt.gz


all: bookworm/bookworm.cnf $(targets)

bookwormdatabase: bookworm/bookworm.cnf bookworm/files/metadata/jsoncatalog.txt bookworm/files/texts/input.txt bookworm/files/metadata/field_descriptions.json
	cd bookworm; make;

downloads/%.tar.bz2:
	mkdir -p downloads
	-curl -f -o $@ $(subst downloads/,http://chroniclingamerica.loc.gov/data/ocr/,$@)

bookworm/files/texts/input.txt: input.txt
	mkdir -p bookworm/files/texts
	ln -s ../../../input.txt  bookworm/files/texts/input.txt

bookworm/files/metadata/jsoncatalog.txt:	
	mkdir -p bookworm/files/metadata
	ln -s ../../../jsoncatalog.txt $@

bookworm/files/metadata/field_descriptions.json:	
	mkdir -p bookworm/files/metadata
	ln -s ../../../field_descriptions.json $@

jsoncatalog.txt:
#The page metadata is spit out from the raw files.
	python parseBZ2.py downloads | tee input.txt | python makePageMetadata.py > jsoncatalog.txt

input.txt: jsoncatalog.txt

bookworm:
	git clone git@github.com:bmschmidt/Presidio bookworm
	cd bookworm; git checkout master

bookworm/bookworm.cnf: bookworm
	python bookworm/scripts/makeConfiguration.py
	mv bookworm.cnf bookworm/bookworm.cnf

newspapers.rdf:
	curl -o newspapers.rdf http://chroniclingamerica.loc.gov/newspapers.rdf


