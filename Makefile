
all: build

test:
	pytest -s

build:
	python3 setup.py sdist bdist_wheel

publish:
	python3 -m twine upload dist/*

publish-test:
	python3 -m twine upload --repository testpypi dist/*

clean:
	rm -rf ./build ./datetime_matcher.egg-info ./dist

.PHONY: all build publish publish-test clean test