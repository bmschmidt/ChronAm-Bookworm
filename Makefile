locFiles = $(shell curl http://chroniclingamerica.loc.gov/ocr.json | perl -ne 'if (m/"name": ?"(.*)"/) {print "$$1\n"}')
targets = $(addprefix downloads/,$(locFiles))
baseNames = $(basename $(basename $(locFiles)))
catalogs = $(addsuffix .txt.gz, $(addprefix jsoncatalogs/,$(baseNames)))
txts = $(addsuffix .txt.gz, $(addprefix inputfiles/,$(baseNames)))

####################
# First: downloading.
####################

downloads: $(targets)

parsedness: $(catalogs)

jsoncatalogs/%.txt.gz: downloads/%.tar.bz2
	mkdir -p jsoncatalogs inputfiles
	python parseBZ2.py $<

inputfiles/%.txt.gz: jsoncatalogs/%.txt.gz

################
# Then: Building
################

bookworm.cnf:
	bookworm init

.bookworm:
	bookworm init

input.sh:
	echo 'find ../inputfiles -name "*.gz" | xargs gunzip -c' > $@

bookwormdatabase: input.sh jsoncatalog.txt field_descriptions.json
	bookworm build all

downloads/%.tar.bz2:
	mkdir -p downloads
	-curl -f -o $@ $(subst downloads/,http://chroniclingamerica.loc.gov/data/ocr/,$@)

jsoncatalog.txt: jsoncatalogs
#The page metadata is spit out from the raw files.
	find jsoncatalogs | parallel -P 8 gunzip -c {} > $@

#######################
#Then: better metadata
#######################

newspapers.rdf:
	curl -o newspapers.rdf http://chroniclingamerica.loc.gov/newspapers.rdf

newspaperdata.json: newspapers.rdf
#Should require newspapers.rdf, but I'm skipping.
	python parseRDF.py > $@

