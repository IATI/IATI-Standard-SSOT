# Script to update each of the 4 submodules in the IATI-SSOT repository
#

timestamp=$(date +%s)

for version in 1.04 1.05 2.01 2.02 2.03; do
	# Checkout to the specified version for the SSOT directory
	git checkout version-$version

	# Pull the latest code from origin for this version (i.e. Git branch) of the SSOT directory
	git pull origin version-$version

	# Check out a new branch to get around branch protection
	git checkout -b update-submodules-$timestamp-$version

	# Discard local changes to submodules
	# See: https://stackoverflow.com/a/27415757/2323348
	git submodule deinit -f .
	git submodule update --init

	# Pull the latest versions of submodules
	git submodule update --remote

	# Git add submodules
	git add IATI-Codelists IATI-Extra-Documentation IATI-Schemas IATI-Rulesets

	# Commit updated submodules
	git commit -m "Updated submodules (using script) "$version

	# Push to the server
	git push origin update-submodules-$timestamp-$version
done
