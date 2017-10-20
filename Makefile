all: venv
	venv/bin/python3 freeze.py
	mkdir build/css
	mkdir build/images
	mkdir build/keys
	mkdir build/papers
	cp css/*.css build/css/
	cp images/*.jpg build/images
	cp keys/*.pub build/keys/
	cp papers/*.pdf build/papers/
	cp images/favicon.ico ./build/

venv: requirements.txt
	python3 -m venv venv
	venv/bin/pip3 install -r requirements.txt

clean:
	rm -rf venv/ build/
