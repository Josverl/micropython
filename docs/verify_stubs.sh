#!/usr/bin/env bash


if [ -n $1 ]; then
    echo "### $1"
    python -c "import sys; sys.path.insert(0, 'stubs'); import stubs.$1"
else
    cd stubs

    for i in */__init__.py; do
        d=`dirname $i`
        echo "### $d"

        cd ..
        python -c "import sys; sys.path.insert(0, 'stubs'); import stubs.$d"
        cd stubs
    done
fi
