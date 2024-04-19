#!/bin/sh
PROC="SMS-StopStop"
PARTSq="_mStop-"

for MSq in {167..1317..25} {183..1333..25}; do
    MSqSTR=${MSq/./p}
    MODEL=${PROC}${PARTSq}${MSqSTR}
    if [ -f "${MODEL}_slc7_amd64_gcc10_CMSSW_12_4_8_tarball.tar.xz" ]; then
        if ! grep -Fq 'All checks passed' "submit/${PROC}/${MODEL}/output.txt"; then
            echo "gridpack not validated: ${MODEL}"
        fi
    else
        echo "gridpack not existed: ${MODEL}"
    fi
done
