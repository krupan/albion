#!/bin/bash

if [ ! -e "albion.py" ]; then
    echo "FAIL: albion.py not found"
elif [ ! -x "albion.py" ]; then
    echo "FAIL: albion.py not executable"
fi

output=`./albion.py list_envs`

if [ "$output" = "ALBION_ENV_PATH is not set" ]; then
    echo "WIN: ALBION_ENV_PATH not set"
    export ALBION_ENV_PATH=/opt/albion-stuff/envs/
else
    echo "FAIL: missing error about missing ALBION_ENV_PATH"
fi

output=`./albion.py list_envs`

if [ "$output" = "default" ]; then
    echo "WIN: listed with one dir in path"
    export ALBION_ENV_PATH=$ALBION_ENV_PATH:$HOME/.local_albion/envs
else
    echo "FAIL: failed with one dir in path"
fi

output=`./albion.py list_envs`

if [ "$(echo $output)" = "default my-default" ]; then
    echo "WIN: listed with two dirs in path"
else
    echo "FAIL: failed with two dirs in path"
fi

