PY_EXE_PATH ?= $(shell which python3.10 || which python3.9 || which python3.8 || which python3.7 || which python3.6 || which python3)
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
MARKER_REQUIREMENTS_SYNCED_DEVTIME := $(VENV_DIR)/bin/.m_requirements-synced--devtime
MARKER_REQUIREMENTS_SYNCED_DISTTIME := $(VENV_DIR)/bin/.m_requirements-synced--disttime
MARKER_INSTALLED_EDITABLE := $(VENV_DIR)/bin/.m_installed-editable

REQUIREMENTS_DEVTIME_FILENAME := requirements-devtime.txt
REQUIREMENTS_DISTTIME_FILENAME := requirements.txt

package := datetime_matcher
package_dir := src/datetime_matcher
test_dir := test
coverage_percent = 80

# ==================== Virtual Environment Management ====================

all: fix-lint build lint test build

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

$(MARKER_PIPTOOLS): # If venv marker is newer, then re-init piptools
$(MARKER_PIPTOOLS): $(MARKER_VENV)
	make init-piptools


# ==================== Requirements Management ====================

# Requirements input files
INPUT_DISTTIME_REQUIREMENTS_FILENAME := requirements.in
INPUT_DEVTIME_REQUIREMENTS_FILENAME := requirements-devtime.in
ALL_INPUT_REQUIREMENTS_FILENAMES := $(INPUT_DISTTIME_REQUIREMENTS_FILENAME) $(INPUT_DEVTIME_REQUIREMENTS_FILENAME)

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
sync-devtime-requirements: # Syncs (installs/upgrades) the actual requirements by downloading the exact versions of the requirements specified in the pinned .txt for dev-time requirements
sync-devtime-requirements: $(MARKER_PIPTOOLS) $(MARKER_REQUIREMENTS_RESOLVED)
	test -f $(REQUIREMENTS_DEVTIME_FILENAME) || make resolve-requirements
	$(PIP_SYNC_IN_VENV_EXE) $(REQUIREMENTS_DEVTIME_FILENAME)
	@echo "Installed devtime requirements as specified in $(REQUIREMENTS_DEVTIME_FILENAME)."
	@touch $(MARKER_REQUIREMENTS_SYNCED_DEVTIME)

.PHONY: sync-disttime-requirements
sync-disttime-requirements: # Syncs (installs/upgrades) the actual requirements by downloading the exact versions of the requirements specified in the pinned .txt for dist-time requirements
sync-disttime-requirements: $(MARKER_PIPTOOLS) $(MARKER_REQUIREMENTS_RESOLVED)
	test -f $(REQUIREMENTS_DISTTIME_FILENAME) || make resolve-requirements
	$(PIP_SYNC_IN_VENV_EXE) $(REQUIREMENTS_DISTTIME_FILENAME)
	@echo "Installed disttime requirements as specified in $(REQUIREMENTS_DISTTIME_FILENAME)."
	@touch $(MARKER_REQUIREMENTS_SYNCED_DISTTIME)

.PHONY: sync-requirements
sync-requirements: # Syncs (installs/upgrades) the actual requirements by downloading the exact versions of the requirements specified in the pinned .txt for both dev-time and dist-time requirements
sync-requirements: $(MARKER_PIPTOOLS)
	make sync-devtime-requirements
# make sync-disttime-requirements

$(MARKER_REQUIREMENTS_SYNCED_DEVTIME): # If the requirements resolved marker has been updated, then the requirements are considered NOT synced
$(MARKER_REQUIREMENTS_SYNCED_DEVTIME): $(MARKER_REQUIREMENTS_RESOLVED)
	make sync-devtime-requirements

$(MARKER_REQUIREMENTS_SYNCED_DISTTIME): # If the requirements resolved marker has been updated, then the requirements are considered NOT synced
$(MARKER_REQUIREMENTS_SYNCED_DISTTIME): $(MARKER_REQUIREMENTS_RESOLVED)
	make sync-disttime-requirements

# Resolving of Requirements

.PHONY: resolve-requirements
resolve-requirements: # Resolves requirements from input files to generate pinned .txt, WITHOUT upgrading the versions
resolve-requirements: # - then marks requirements as having been resolved
resolve-requirements: $(MARKER_PIPTOOLS)
	$(PIP_COMPILE_IN_VENV_EXE) --output-file=$(REQUIREMENTS_DEVTIME_FILENAME) $(ALL_INPUT_REQUIREMENTS_FILENAMES)
	@echo "Updated $(REQUIREMENTS_DEVTIME_FILENAME) with devtime and disttime requirements."
	$(PIP_COMPILE_IN_VENV_EXE) --output-file=$(REQUIREMENTS_DISTTIME_FILENAME) $(INPUT_DISTTIME_REQUIREMENTS_FILENAME)
	@echo "Updated $(REQUIREMENTS_DISTTIME_FILENAME) with disttime requirements."
	@touch $(MARKER_REQUIREMENTS_RESOLVED)

.PHONY: update-requirements
update-requirements: # Resolves requirements from input files to generate pinned .txt, upgrading the versions as necessary
update-requirements: # - then marks requirements as having been resolved
update-requirements: $(MARKER_PIPTOOLS)
	$(PIP_COMPILE_IN_VENV_EXE) --upgrade --output-file=$(REQUIREMENTS_DEVTIME_FILENAME) $(ALL_INPUT_REQUIREMENTS_FILENAMES)
	@echo "Updated $(REQUIREMENTS_DEVTIME_FILENAME) with latest/upgraded devtime and disttime requirements."
	$(PIP_COMPILE_IN_VENV_EXE) --upgrade --output-file=$(REQUIREMENTS_DISTTIME_FILENAME) $(INPUT_DISTTIME_REQUIREMENTS_FILENAME)
	@echo "Updated $(REQUIREMENTS_DISTTIME_FILENAME) with latest/upgraded disttime requirements."
	@touch $(MARKER_REQUIREMENTS_RESOLVED)

$(MARKER_REQUIREMENTS_RESOLVED): # If any of the requirements input files have been updated, the requirements are NOT considered resolved
$(MARKER_REQUIREMENTS_RESOLVED): $(ALL_INPUT_REQUIREMENTS_FILENAMES)
	make resolve-requirements

$(ALL_INPUT_REQUIREMENTS_FILENAMES) &:
	@touch $(ALL_INPUT_REQUIREMENTS_FILENAMES)


# ==================== Linting ====================

.PHONY: lint
lint: # Run all linters in check mode
lint: isort flake8 mypy black

.PHONY: fix-lint
fix-lint: # Run all auto-fix linters
fix-lint: isort-fix black-fix

.PHONY: isort
isort: # Run isort to check sorting of imports
isort: $(MARKER_REQUIREMENTS_SYNCED_DEVTIME)
	$(PY_IN_VENV_EXE) -m isort --check-only $(package_dir)
	$(PY_IN_VENV_EXE) -m isort --check-only $(test_dir)

.PHONY: isort-fix
isort-fix: # Run isort to fix sorting of imports
isort-fix: $(MARKER_REQUIREMENTS_SYNCED_DEVTIME)
	$(PY_IN_VENV_EXE) -m isort $(package_dir)
	$(PY_IN_VENV_EXE) -m isort $(test_dir)

.PHONY: flake8
flake8: # Run flake8 to check PEP style violations
flake8: $(MARKER_REQUIREMENTS_SYNCED_DEVTIME)
	$(PY_IN_VENV_EXE) -m flake8 --config=setup.cfg $(package_dir)

.PHONY: black
black: # Run black to check PEP style violations
black: $(MARKER_REQUIREMENTS_SYNCED_DEVTIME)
	$(PY_IN_VENV_EXE) -m black --diff --check -q --color $(package_dir)
	$(PY_IN_VENV_EXE) -m black --diff --check -q --color $(tests_dir)

.PHONY: black-fix
black-fix: # Run black to fix PEP style violations
black-fix: $(MARKER_REQUIREMENTS_SYNCED_DEVTIME)
	$(PY_IN_VENV_EXE) -m black -q --color $(package_dir)
	$(PY_IN_VENV_EXE) -m black -q --color $(tests_dir)

.PHONY: mypy
mypy: # Run mypy type-checker
mypy: $(MARKER_REQUIREMENTS_SYNCED_DEVTIME)
	$(PY_IN_VENV_EXE) -m mypy --config-file setup.cfg --namespace-packages -p $(package)


# ==================== Building ====================

.PHONY: build
build: $(MARKER_REQUIREMENTS_SYNCED_DEVTIME)
	$(PY_IN_VENV_EXE) -m build


# ==================== Testing ====================

.PHONY: test
test: $(MARKER_REQUIREMENTS_SYNCED_DEVTIME)
	$(PY_IN_VENV_EXE) -m pytest --cov=src --cov-fail-under=$(coverage_percent) --cov-config=setup.cfg --cov-report=xml:coverage.xml --cov-report=term-missing --cov-branch $(package_dir) $(test_dir)


# ==================== Publishing ====================

.PHONY: pre-publish
pre-publish:
	$(PY_IN_VENV_EXE) -m twine check dist/*

.PHONY: publish
publish: pre-publish
	$(PY_IN_VENV_EXE) -m twine upload dist/*

.PHONY: publish-test
publish-test: pre-publish
	$(PY_IN_VENV_EXE) -m twine upload --repository testpypi dist/*


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
