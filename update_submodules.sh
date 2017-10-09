# Script to update each of the 4 submodules in the IATI-SSOT repository
# 

timestamp=$(date +%s)

for version in 1.04 1.05 2.01 2.02; do
	# Checkout to the specified version for the SSOT directory
	git checkout version-$version

	# Pull the latest code from origin for this version (i.e. Git branch) of the SSOT directory
	git pull origin version-$version

	# Check out a new branch to get around branch protection
	git checkout -b update-submodules-$timestamp-$version

	# Loop over each subfolder, pull the latest version and add to staging
	for folder in IATI-Codelists IATI-Extra-Documentation IATI-Schemas IATI-Rulesets; do
		# Enter the specified folder (which contains the submodule)
		cd $folder
		
		# Ensure that we are on the correct branch (i.e. Git branch)
		git checkout version-$version

		# Pull the latest code from origin for this version (i.e. Git branch)
		git pull origin version-$version

		# Go back to the SSOT folder
		cd ..

		# Add the specified folder (which contains the submodule) to staging
		git add $folder
	done
	
	# Commit updated submodules
	git commit -m "Updated submodules (using script) "$version
	
	# Push to the server
	git push origin update-submodules-$timestamp-$version
done
