#!/bin/sh
PROC="Higgsino-N2C1"
PARTN2="_mN2-"
PARTC1="_mC1-"

for MN2 in 100 125 150 175 200 225 250 275 300 325 350 375 400 425 450 475 500 525 550 575 600; do
    for DM in 0.6 0.8 1 1.5 2 3 5 7.5 10 15 20 30 40 50; do
        MN1=`awk "BEGIN {printf \"%.2f\n\", (${MN2}-${DM})}"`	
	MC1=`awk "BEGIN {printf \"%.2f\n\", ((${MN1}+${MN2})/2)}"`
	MN2STR=${MN2/./p}
	MN1STR=${MN1/./p}
	MC1STR=${MC1/./p}
        MODEL=${PROC}${PARTN2}${MN2STR}${PARTC1}${MC1STR}
        if [[ ! -f "${MODEL}_slc7_amd64_gcc700_CMSSW_10_6_19_tarball.tar.xz" ]]; then
            rm -rf submit/${PROC}/${MODEL}
            sh condorSubmitter.sh ${PROC} ${MODEL}
        fi
    done
done
