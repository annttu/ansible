#!/bin/bash


THERE_PATH="$1"
cd "$THERE_PATH"

make wrapper > ../make.log 2>&1
#make test >> make.log 2>&1

# Fix installation path
sed -i.bak -e 's#/data00/there#/opt/there#' ${THERE_PATH}/src/perllib/There/Conf.pm
rm ${THERE_PATH}/src/perllib/There/Conf.pm.bak

make install >> ../make.log 2>&1
