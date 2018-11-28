# Script to update each of the 4 main components + 2 optional ones in the IATI-SSOT repository
#
source scripts/main/CONFIG.FILE

timestamp=$(date +%s)


while getopts ver:s: option; do
	case "${option}" in
		ver) VERSION=${OPTARG};;
		s) SSOT=${OPTARG};;
	esac
done


if [ -z "$VERSION" ]; then
    VERSION=$DEFAULT_SSOT_BRANCH; echo "No version specified, building version $DEFAULT_SSOT_BRANCH";
else
	echo "Building version $VERSION"
fi

if [ -z "$SSOT" ]; then
    SSOT="false"; echo "Building all components";
else
	echo "Building SSOT only components"
fi


# fetches the main ssot components
for COMPONENT in "${SSOT_COMPONENTS[@]}"; do
	if [ -d $COMPONENT ]; then
		echo "Found $COMPONENT folder, deleting and cloning again"
		rm -rf $COMPONENT
	fi

	git clone "$IATI_GIT_BASE$COMPONENT.git"
	cd $COMPONENT
	git fetch
	git checkout "version-$VERSION"
	git pull
	cd ..
done


# fetches the optional ssot components
if [ $SSOT = "false" ]; then
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
	done;
fi
