#!/bin/bash

which osc || { echo "osc must be installed"; exit 1; }

VERSION=`python setup.py --version`
PLATFORM=`uname`

pull_obs () {
    if [ -d .obs ]
    then
        osc update .obs/
    else
        osc checkout isv:spb:colab/colab --output-dir=".obs/"
    fi
}

update_sdist () {
    rm -fR dist/
    python setup.py sdist
}


add_to_obs () {
    osc revert .obs/
    osc rm -f .obs/colab-*.tar.gz

    cp dist/colab-*.tar.gz .obs/
    cp colab.spec .obs/

    osc add .obs/colab-$VERSION.tar.gz
}


update_spec_versions () {
    regex="s/(\%define (unmangled_)?version).*/\1 $VERSION/;"
    if [[ "$PLATFORM" == 'Darwin' ]]; then
        sed -i '' -E "$regex" colab.spec
    else
        sed -i -E "$regex" colab.spec
    fi
}


push_to_obs () {
    osc checkin .obs/ -m "Updated version $VERSION"
}

update_sdist
update_spec_versions

pull_obs
add_to_obs
push_to_obs
