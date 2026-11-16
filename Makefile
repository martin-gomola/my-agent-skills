PORT ?= 8983

.PHONY: plugins site dev check test
plugins:
	python3 scripts/sync_plugins.py
site:
	cp -R pets site/
dev: site
	python3 -m http.server $(PORT) --bind 127.0.0.1 --directory site
check:
	uv run --with-requirements requirements-dev.txt python scripts/validate.py
test: check
	uv run --with-requirements requirements-dev.txt python -m unittest discover -s tests -v
	node --test tests/installer.test.mjs
