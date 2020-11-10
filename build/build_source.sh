ZPATH=build/src/

cd $ZPATH
#python setup.py build_ext --inplace
#python setup.py build_ext --build-dir c
python setup.py build_ext -b out/so -t out/o
#cython scheduler --embed
