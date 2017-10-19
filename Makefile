all:
	python3 freeze.py
	mkdir build/css
	mkdir build/images
	mkdir build/keys
	mkdir build/papers
	cp css/*.css build/css/
	cp images/*.jpg build/images
	cp keys/*.pub build/keys/
	cp papers/*.pdf build/papers/

