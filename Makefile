
all: build test

test:
	pytest -s

build:
	python3 -m build

publish:
	python3 -m twine upload dist/*

publish-test:
	python3 -m twine upload --repository testpypi dist/*

clean:
	rm -rf ./build
	rm -rf ./datetime_matcher.egg-info
	rm -rf ./dist
	rm -rf ./.pytest_cache

.PHONY: all build publish publish-test clean test