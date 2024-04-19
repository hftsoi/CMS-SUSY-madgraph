#!/bin/sh
PROC="SMS-N2N3"
PARTSq="_mN-"

for MSq in {150..1800..25}; do
    MSqSTR=${MSq/./p}
    MODEL=${PROC}${PARTSq}${MSqSTR}
    if [[ ! -f "${MODEL}_slc7_amd64_gcc10_CMSSW_12_4_8_tarball.tar.xz" ]]; then
        rm -rf submit/${PROC}/${MODEL}
        sh condorSubmitter.sh ${PROC} ${MODEL}
    fi
done
