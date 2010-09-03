#! /bin/bash

echo 'WARNING: this test is still under construction'

if [ ! -e "albion.py" ]; then
    echo "FAIL: albion.py not found"
elif [ ! -x "albion.py" ]; then
    echo "FAIL: albion.py not executable"
fi

output = `./albion.py load my-stuff 1.1`

if [ "$output" = "ALBION_CONFIGS_PATH is not set" ]; then
    echo "WIN: ALBION_CONFIGS_PATH not set"
    export ALBION_CONFIGS_PATH="$HOME/.local_albion/configs"
else
    echo "FAIL: missing error about missing ALBION_CONFIGS_PATH"
fi

output = `./albion.py load my-stuff 1.0`

if [ "$output" = "" ]; then
    echo "WIN: found config, but not version"
else
    echo "FAIL: missing error about wrong version"
fi