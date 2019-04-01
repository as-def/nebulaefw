DIST:=neb_update.zip

all: $(DIST)

$(DIST):
	tar cfz $(DIST) QB_Nebulae_V2

clean:
	rm -f $(DIST)
	find . -iname '*.pyc' -exec rm {} \;
	find . -name __pycache__ -exec rmdir {} \;