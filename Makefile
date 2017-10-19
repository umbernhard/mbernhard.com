all:
	source venv/bin/activate
	python3 freeze.py
	deactivate
	mkdir build/css
	mkdir build/images
	mkdir build/keys
	mkdir build/papers
	cp css/*.css build/css/
	cp images/*.jpg build/images
	cp keys/*.pub build/keys/
	cp papers/*.pdf build/papers/

init:
	python3 -m venv venv
	source venv/bin/activate
	pip3 freeze -r requirements.txt
	deactivate
