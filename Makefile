
.PHONY: all build publish publish-test clean test bump-version install-uv

all: build

# URL for the uv installer script.
# This is defined as a variable so it can be pinned or overridden if needed.
UV_INSTALL_URL ?= https://astral.sh/uv/install.sh

# Helper target for local development only.
# Downloads and runs the uv installer script from $(UV_INSTALL_URL).
# Review the installer script before running and do not use this target in production automation.
install-uv:
	@echo "Installing uv if not already available (local/dev helper only)..."
	@command -v uv >/dev/null 2>&1 || { \
		echo "Downloading uv installer from $(UV_INSTALL_URL)"; \
		tmpfile=$$(mktemp); \
		curl -LsSf "$(UV_INSTALL_URL)" -o "$$tmpfile"; \
		sh "$$tmpfile"; \
		rm -f "$$tmpfile"; \
	}

test:
	uv run pytest -s

build:
	uv build

publish:
	uv publish

publish-test:
	uv publish --repository testpypi

clean:
	rm -rf ./build ./*.egg-info ./dist

bump-version:
	uv run --frozen bump-my-version bump $(PART)