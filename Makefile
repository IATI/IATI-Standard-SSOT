#
# Makefile for IATI's Standard SSOT reference site
# 

clone_components:
	sh scripts/main/clone_components.sh

install:
	sh scripts/main/setup.sh
	clone_components

clean:
	sh scripts/main/clean.sh

run:
	sh scripts/main/runserver.sh

switch_version:
	echo "Not yet implemented"

build_rst:
	sh scripts/main/gen_rst.sh

build_html:
	sh scripts/main/gen_html.sh

build_dev:
	sh scripts/main/combined_gen.sh

build_live:
	sh scripts/main/combined_gen.sh

deploy_dev:
	echo "Not yet implemented"

deploy_live:
	echo "Not yet implemented"
