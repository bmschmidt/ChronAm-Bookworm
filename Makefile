targets=$(addprefix downloads/,$(shell curl http://chroniclingamerica.loc.gov/ocr.json | perl -ne 'if (m/"name": ?"(.*)"/) {print "$$1\n"}'))

all: bookworm/bookworm.cnf $(targets)

downloads/%.tar.bz2:
	curl -o $@ $(subst downloads/,http://chroniclingamerica.loc.gov/data/ocr/,$@)

bookworm/files/texts/input.txt:
	mkdir -p bookworm/files/texts
	mkfifo bookworm/files/texts/input.txt
	python parseBZ2.py downloads &

jsoncatalog.txt:
	python parseBZ2.py downloads titles | python makePageMetadata.py > $@

bookworm:
	git clone git@github.com:bmschmidt/Presidio bookworm
	cd bookworm; git checkout lessDiskSpace

bookworm/bookworm.cnf: bookworm
	python bookworm/scripts/makeConfiguration.py
	mv bookworm.cnf bookworm/bookworm.cnf

metadata:
	curl -o newspapers.rdf http://chroniclingamerica.loc.gov/newspapers.rdf


