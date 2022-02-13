all: README.md
README.md: make_readme hatching.py sphere.py
	./make_readme
