# put this in your ~/.profile:
#
# export PROFILE_SOURCED_YO=1
#
# and this in your ~/.bashrc:
#
# export BASHRC_SOURCED_YO=1
#
# log out, and log back in, and then source this script and make sure
# not FAILs print out, should be able to be sourced over and over with
# no fails

fail(){
    echo "FAIL: $1 is incorrect"
}

if [ "$PROFILE_SOURCED_YO" = "1" ]; then
    echo "PROFILE_READ_YO is correct"
else
    fail PROFILE_READ_YO
    return
fi

if [ "$BASHRC_SOURCED_YO" = "1" ]; then
    echo "BASHRC_SOURCED_YO is correct"
else
    fail BASHRC_SOURCED_YO
    return
fi

if [ "$PURGEENV_TEST" = "" ]; then
    echo "PURGEENV_TEST is not set"
else
    fail "PURGEENV_TEST"
    return
fi
export PURGEENV_TEST=purgeenv_test

if [ "$PURGEENV_TEST" = "" ]; then
    fail "PURGEENV_TEST"
    return
else
    echo "PURGEENV_TEST is set"
fi

echo "purging environment, check that PURGEENV_TEST is not set when done"

if [ ! -e "albion.py" ]; then
    echo "FAIL: albion.py not found"
elif [ -x "albion.py" ]; then
    eval `./albion.py unload`
else
    echo "FAIL: purgenenv.py not executable"
fi
