#!/bin/bash
set -x
source /cvmfs/cms.cern.ch/cmsset_default.sh
git clone https://github.com/cms-sw/genproductions.git genproductions
#git clone --branch mg265UL https://github.com/cms-sw/genproductions.git genproductions
cd genproductions/bin/MadGraph5_aMCatNLO

model=$1

mv ../../../${model} cards/

./gridpack_generation.sh ${model} cards/${model}

cp *.xz ../../../

tar -xavf *.xz
./runcmsgrid.sh 10 12345 1
