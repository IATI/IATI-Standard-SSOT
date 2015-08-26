# Script to update each of the 4 submodules in the IAST-SSOT repository
# 

for version in 1.04 1.05 2.01; do
	# Checkout to teh specified version
	git checkout version-$version

	# Pull each submodule for this versino
	git submodule foreach git pull origin version-$version
	
	# Add each folder to staging
	git add IATI-Codelists/
	git add IATI-Extra-Documentation/
	git add IATI-Schemas
	git add IATI-Rulesets

	# Commit updated submodules
	git commit -m "Updated submodules"
	
	# Push to the server
	git push
done
