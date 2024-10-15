.PHONY: build clean release

build:
	python -m build

clean:
	rm -rf dist *.egg-info

release: clean build
	twine upload dist/*
