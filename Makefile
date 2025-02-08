.PHONY: files/cv.pdf
all: files/cv.pdf
	jekyll build

files/cv.pdf: cv/template.tex 
	cd cv; rake;
	cp cv/cv.pdf files/bernhard-cv.pdf

show: all
	jekyll serve
	
clean:
	rm -rf build
	rm files/bernhard-cv.pdf
	rm cv/cv.*

