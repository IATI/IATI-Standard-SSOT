# Script to update each of the 4 submodules in the IATI-SSOT repository
#

timestamp=$(date +%s)

for version in 2.01 2.02 2.03; do
	# fetch the latest version from the remote
	git fetch origin version-$version

	# Checkout to the specified version for the SSOT directory
	git checkout --force origin/version-$version

	# Discard local changes to submodules
	# See: https://stackoverflow.com/a/27415757/2323348
	git submodule deinit -f .
	git submodule update --init

	# Check out a new branch to get around branch protection
	git checkout -b update-submodules-$timestamp-$version

	# Pull the latest versions of submodules
	git submodule update --remote

	# Git add submodules
	git add IATI-Codelists IATI-Extra-Documentation IATI-Schemas IATI-Rulesets

	# Commit updated submodules
	git commit -m "Updated submodules (using script) "$version

	# Push to the server
	git push origin update-submodules-$timestamp-$version
done
