#!/bin/bash

which -s osc || { echo "osc must be installed"; exit 1; }

VERSION=`python setup.py --version`

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
    sed -i '' -E "s/(\%define (unmangled_)?version).*/\1 $VERSION/;" colab.spec
}


push_to_obs () {
    echo
}

update_sdist
update_spec_versions

pull_obs
add_to_obs
push_to_obs
