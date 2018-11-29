# Usage:
#
#     make [command]
#

setup:
	virtualenv pyenv; \
	. pyenv/bin/activate; \
	pip install -r requirements.txt

clone_components:
	bash scripts/main/clone_components.sh

clean_virtualenv:
	rm -rf pyenv

clean: clean_virtualenv; \
	rm -rf IATI-*; \
	rm -rf docs docs-copy

reinstall_dependencies: clean_virtualenv setup

dev_install: clean setup clone_components

live_install: dev_install

run:
	cd docs-copy/en/_build/dirhtml; \
	python -m SimpleHTTPServer 8000; \
	cd -

switch_version:
	. pyenv/bin/activate; \
	bash scripts/main/clone_components.sh -s true -ver $(VERSION)

build_rst:
	. pyenv/bin/activate; \
	bash scripts/main/gen_rst.sh

build_html:
	. pyenv/bin/activate; \
	bash scripts/main/gen_html.sh

build_dev:
	. pyenv/bin/activate; \
	bash scripts/main/combined_gen.sh

build_docs: build_rst build_html

build_live: build_dev

deploy_dev:
	echo "Not yet implemented"

deploy_live:
	echo "Not yet implemented"
