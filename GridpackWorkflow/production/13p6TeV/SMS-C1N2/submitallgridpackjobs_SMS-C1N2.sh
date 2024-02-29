#!/bin/sh
SCRIPT="../../test/scripts/submitGridpackCondorJob.py"
MODEL="SMS-C1N2_mC1-"
JOBS="/afs/cern.ch/work/d/dspitzba/SUSYsignalProduction/GenLHEfiles/GridpackWorkflow/production/SMS-C1N2/jobs"
genprodir="/afs/cern.ch/work/d/dspitzba/SUSYsignalProduction/genproductions/"

#for MNLSP in {100..200..10} {250..500..50} {600..1000..100} 125; do
#for MNLSP in {225..475..50} {625..1300..25}; do
for MNLSP in 175; do
    python ${SCRIPT} ${MODEL}${MNLSP} --cards-dir ${JOBS}/${MODEL}${MNLSP}  --genproductions-dir ${genprodir}
done
