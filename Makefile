# Usage:
#
#     make [command]


setup:
	virtualenv pyenv; \
	source pyenv/bin/activate; \
	pip install -r requirements.txt

clone_components:
	sh scripts/main/clone_components.sh

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
	echo "Not yet implemented"

build_rst:
	sh scripts/main/gen_rst.sh

build_html:
	sh scripts/main/gen_html.sh

build_dev:
	sh scripts/main/combined_gen.sh

build_dev_light: build_rst build_html

build_live:
	sh scripts/main/combined_gen.sh

deploy_dev:
	echo "Not yet implemented"

deploy_live:
	echo "Not yet implemented"
