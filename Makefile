install:
	rm -rf ./bin
	mkdir bin
	cp TurCrypt.py ./bin/turcrypt
	chmod 777 ./bin/turcrypt
	sudo cp `pwd`/bin/turcrypt /usr/local/bin/turcrypt
	echo "Done. You can now run turcrypt from the command line."

all: install
