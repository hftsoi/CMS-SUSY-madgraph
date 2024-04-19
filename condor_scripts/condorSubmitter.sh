proc=$1
model=$2

submitDir="submit/${proc}/${model}"
mkdir -p "${submitDir}"

#inputDir=inputfiles/${proc}/jobs/${model}
inputDir=13p6TeV/${proc}/jobs/${model}

cat > "job_${model}.sub" << EOF
executable = do.sh
arguments = ${model}
log = ${submitDir}/log.log
output = ${submitDir}/output.txt
error = ${submitDir}/error.txt
transfer_input_files = ${inputDir}
requestdisk = 16G
requestmemory = 16G
requirements = TARGET.OpSysAndVer == "CentOS7"
queue
EOF

condor_submit job_${model}.sub
rm job_${model}.sub
