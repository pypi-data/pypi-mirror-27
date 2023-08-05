PWD=`pwd`
export CPKG=`basename $PWD`
echo "NAME $CPKG ..."
pip uninstall --yes $CPKG
pip install .
