
all: build test

PY_EXE_PATH ?= $(shell which python3.9 || which python3.8 || which python3.7 || which python3.6 || which python3)
PY_EXE := $(shell basename $(PY_EXE_PATH))

VENV_DIR := .venv
ACTIVATE_VENV_EXE := . $(VENV_DIR)/bin/activate
PY_IN_VENV_EXE := $(ACTIVATE_VENV_EXE); python

PIP_IN_VENV_EXE := $(PY_IN_VENV_EXE) -m pip
PIP_COMPILE_IN_VENV_EXE := $(PY_IN_VENV_EXE) -m piptools compile
PIP_SYNC_IN_VENV_EXE := $(PY_IN_VENV_EXE) -m piptools sync

MARKER_VENV := $(VENV_DIR)/bin/.m_venv
MARKER_PIPTOOLS := $(VENV_DIR)/bin/.m_piptools
MARKER_REQUIREMENTS_RESOLVED := $(VENV_DIR)/bin/.m_requirements-resolved

REQUIREMENTS_DEVTIME_FILENAME := requirements-devtime.txt
REQUIREMENTS_RUNTIME_FILENAME := requirements.txt

package := datetime_matcher
package_dir := src/datetime_matcher
test_dir := test


# ==================== Virtual Environment Management ====================

.PHONY: init-venv
init-venv:
	$(PY_EXE) -m venv $(VENV_DIR)
	@touch $(MARKER_VENV)
	
.PHONY: reinit-venv
reinit-venv:
	rm -rf $(VENV_DIR)
	make init-venv

$(MARKER_VENV):
	make init-venv

.PHONY: init-piptools
init-piptools:
	test -f $(MARKER_VENV) || make init-venv
	$(PIP_IN_VENV_EXE) install -U setuptools pip pip-tools wheel
	@touch $(MARKER_PIPTOOLS)

$(MARKER_PIPTOOLS):
	make init-piptools


# ==================== Requirements Management ====================

# Requirements input files
INPUT_RUNTIME_REQUIREMENTS_FILENAME := requirements.in
INPUT_DEVTIME_REQUIREMENTS_FILENAMES := $(wildcard requirements-devtime.d/*.in)
ALL_INPUT_REQUIREMENTS_FILENAMES := $(INPUT_RUNTIME_REQUIREMENTS_FILENAME) $(INPUT_DEVTIME_REQUIREMENTS_FILENAMES)

# Resolve and then Sync requirements

.PHONY: install-requirements
install-requirements: # Installs all requirements
install-requirements: $(MARKER_PIPTOOLS)
	make resolve-requirements
	make sync-requirements

.PHONY: upgrade-requirements
upgrade-requirements: # Upgrades all requirements
upgrade-requirements: $(MARKER_PIPTOOLS)
	make update-requirements
	make sync-requirements

# Syncing of Actual Requirements

.PHONY: sync-devtime-requirements
sync-devtime-requirements: # Syncs (installs/upgrades) the actual requirements by downloading the exact versions of the requirements specified in the pinned .txt for devtime requirements
sync-devtime-requirements: $(MARKER_PIPTOOLS) $(MARKER_REQUIREMENTS_RESOLVED)
	test -f $(REQUIREMENTS_DEVTIME_FILENAME) || make resolve-requirements
	$(PIP_SYNC_IN_VENV_EXE) $(REQUIREMENTS_DEVTIME_FILENAME)
	@echo "Installed devtime requirements as specified in $(REQUIREMENTS_DEVTIME_FILENAME)."

.PHONY: sync-runtime-requirements
sync-runtime-requirements: # Syncs (installs/upgrades) the actual requirements by downloading the exact versions of the requirements specified in the pinned .txt for devtime requirements
sync-runtime-requirements: $(MARKER_PIPTOOLS) $(MARKER_REQUIREMENTS_RESOLVED)
	test -f $(REQUIREMENTS_RUNTIME_FILENAME) || make resolve-requirements
	$(PIP_SYNC_IN_VENV_EXE) $(REQUIREMENTS_RUNTIME_FILENAME)
	@echo "Installed runtime requirements as specified in $(REQUIREMENTS_RUNTIME_FILENAME)."

.PHONY: sync-requirements
sync-requirements: # Syncs (installs/upgrades) the actual requirements by downloading the exact versions of the requirements specified in the pinned .txt for both devtime and runtime requirements
sync-requirements: $(MARKER_PIPTOOLS) $(MARKER_REQUIREMENTS_RESOLVED)
	make sync-devtime-requirements
	make sync-runtime-requirements

# Resolving of Requirements

.PHONY: resolve-requirements
resolve-requirements: # Resolves requirements from input files to generate pinned .txt, WITHOUT upgrading the versions
resolve-requirements: # - then marks requirements as having been resolved
resolve-requirements: $(MARKER_PIPTOOLS)
	$(PIP_COMPILE_IN_VENV_EXE) --output-file=$(REQUIREMENTS_DEVTIME_FILENAME) $(ALL_INPUT_REQUIREMENTS_FILENAMES)
	@echo "Updated $(REQUIREMENTS_DEVTIME_FILENAME) with devtime and runtime requirements."
	$(PIP_COMPILE_IN_VENV_EXE) --output-file=$(REQUIREMENTS_RUNTIME_FILENAME) $(INPUT_RUNTIME_REQUIREMENTS_FILENAME)
	@echo "Updated $(REQUIREMENTS_RUNTIME_FILENAME) with runtime requirements."
	@touch $(MARKER_REQUIREMENTS_RESOLVED)

.PHONY: update-requirements
update-requirements: # Resolves requirements from input files to generate pinned .txt, upgrading the versions as necessary
update-requirements: # - then marks requirements as having been resolved
update-requirements: $(MARKER_PIPTOOLS)
	$(PIP_COMPILE_IN_VENV_EXE) --upgrade --output-file=$(REQUIREMENTS_DEVTIME_FILENAME) $(ALL_INPUT_REQUIREMENTS_FILENAMES)
	@echo "Updated $(REQUIREMENTS_DEVTIME_FILENAME) with latest/upgraded devtime and runtime requirements."
	$(PIP_COMPILE_IN_VENV_EXE) --upgrade --output-file=$(REQUIREMENTS_RUNTIME_FILENAME) $(INPUT_RUNTIME_REQUIREMENTS_FILENAME)
	@echo "Updated $(REQUIREMENTS_RUNTIME_FILENAME) with latest/upgraded runtime requirements."
	@touch $(MARKER_REQUIREMENTS_RESOLVED)

$(MARKER_REQUIREMENTS_RESOLVED): # If any of the requirements input files have been updated, the requirements are NOT considered resolved
$(MARKER_REQUIREMENTS_RESOLVED): $(ALL_INPUT_REQUIREMENTS_FILENAMES)
	make resolve-requirements

$(ALL_INPUT_REQUIREMENTS_FILENAMES) &:
	@touch $(ALL_INPUT_REQUIREMENTS_FILENAMES)


# ==================== Linting ====================

.PHONY: lint
lint: # Run all linters in check mode
lint: isort mypy

.PHONY: fix-lint
fix-lint: # Run all auto-fix linters
fix-lint: isort-fix

.PHONY: isort
isort: # Run isort to check sorting of imports
isort: sync-devtime-requirements
	$(PY_IN_VENV_EXE) -m isort --check-only $(package_dir)
	$(PY_IN_VENV_EXE) -m isort --check-only $(test_dir)

.PHONY: isort-fix
isort-fix: # Run isort to fix sorting of imports
isort-fix: sync-devtime-requirements
	$(PY_IN_VENV_EXE) -m isort $(package_dir)
	$(PY_IN_VENV_EXE) -m isort $(test_dir)

.PHONY: mypy
mypy: # Run mypy type-checker
mypy: sync-devtime-requirements
	$(PY_IN_VENV_EXE) -m mypy --config-file setup.cfg $(package_dir)

# ==================== Testing ====================

.PHONY: test
test: sync-devtime-requirements
	$(PY_IN_VENV_EXE) -m pytest $(test_dir)


# ==================== Building ====================

.PHONY: build
build:
	$(PY_IN_VENV_EXE) -m build

.PHONY: publish
publish:
	python3 -m twine upload dist/*

.PHONY: publish-test
publish-test:
	python3 -m twine upload --repository testpypi dist/*

# ==================== Cleaning Up ====================

RM_RECURSIVE := $(RM) -r

.PHONY: clean
clean:
	$(RM_RECURSIVE) ./build
	$(RM_RECURSIVE) ./dist
	$(RM_RECURSIVE) ./.mypy_cache
	find . -type d -name '__pycache__' -exec rm -r {} +
	find . -type d -name '.pytest_cache' -exec rm -r {} +
	find . -type f -name '*.pyc' -exec rm -r {} +
