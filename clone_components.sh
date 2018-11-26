# Script to update each of the 4 main components + 2 optional ones in the IATI-SSOT repository
#

timestamp=$(date +%s)

# main git url
IATI_GIT_BASE="git@github.com:IATI/"

# main ssot components
SSOT_COMPONENTS=(
	"IATI-Codelists"
	"IATI-Schemas"
	"IATI-Rulesets"
	"IATI-Extra-Documentation"
)

# optional components
OPTIONAL_COMPONENTS=(
	"IATI-Websites"
	"IATI-Guidance"
	"IATI-Developer-Documentation"
)

# main branch is 2.03 (latest) for SSOT, live for other repos
DEFAULT_SSOT_BRANCH="2.03"

ALL_SSOT_BRANCHES=("1.04" "1.05" "2.01" "2.02" "2.03")

DEFAULT_NON_SSOT_BRANCH="live"

# fetches the main ssot components
for COMPONENT in "${SSOT_COMPONENTS[@]}"; do
	if [ -d $COMPONENT ]; then
		echo "Found $COMPONENT folder, deleting and cloning again"
		rm -rf $COMPONENT
	fi

	git clone "$IATI_GIT_BASE$COMPONENT.git"
	cd $COMPONENT
	git fetch
	git checkout "version-$DEFAULT_SSOT_BRANCH"
	git pull
	cd ..
done

# fetches the optional ssot components
for COMPONENT in "${OPTIONAL_COMPONENTS[@]}"; do
	if [ -d $COMPONENT ]; then
		echo "Found $COMPONENT folder, deleting and cloning again"
		rm -rf $COMPONENT
	fi

	git clone "$IATI_GIT_BASE$COMPONENT.git"
	cd $COMPONENT
	git fetch
	git checkout $DEFAULT_NON_SSOT_BRANCH
	git pull
	cd ..
done
