#!/bin/bash

rm -rf doc/build
rm dist/*
python3 setup.py clean
python3 setup.py build
python3 setup.py bdist_wheel
pip3 uninstall -y pytiled_parser
for file in dist/*
do
  pip3 install $file
done
# sphinx-build -b html doc doc/build/html
coverage run --source pytiled_parser setup.py test
coverage report -m
