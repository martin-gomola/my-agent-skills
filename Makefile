PORT ?= 8983

.PHONY: site dev check test
site:
	cp -R pets site/
dev: site
	python3 -m http.server $(PORT) --bind 127.0.0.1 --directory site
check:
	uv run --with-requirements requirements-dev.txt python scripts/validate.py
test: check
	uv run --with-requirements requirements-dev.txt python -m unittest discover -s tests -v
	node --test tests/installer.test.mjs
