.PHONY: files/cv.pdf
all: files/cv.pdf
	jekyll build

files/cv.pdf: cv/template.tex 
	cd cv; rake;
	cp cv/cv.pdf files/bernhard-cv.pdf
	
clean:
	rm -rf build
	rm files/cv.pdf
	rm cv/cv.*

