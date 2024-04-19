#!/bin/sh
PROC="SMS-GlGl"
PARTGl="_mGl-"

for MGl in {600..2850..25}; do
    MGlSTR=${MGl/./p}
    MODEL=${PROC}${PARTGl}${MGlSTR}
    if [ -f "${MODEL}_slc7_amd64_gcc10_CMSSW_12_4_8_tarball.tar.xz" ]; then
        if ! grep -Fq 'All checks passed' "submit/${PROC}/${MODEL}/output.txt"; then
            echo "gridpack not validated: ${MODEL}"
        fi
    else
        echo "gridpack not existed: ${MODEL}"
    fi
done
