#!/bin/sh

# Update nexus file in tests/data directory

set -e
scpt_dir=$(dirname $(realpath $0))
root_dir=$(dirname $scpt_dir)


echo " !!! Converting xrd data !!! "
echo " Root directory: ${scpt_dir} "
echo " Updating XRD-918-16_10 data file... ${root_dir}"

xrdml=${root_dir}/tests/data/xrdml_918-16_10
find ${xrdml} -type f ! \( -name '*.log -o -name *.nxs' \) | xargs  dataconverter --nxdl NXxrd_pan --reader xrd --output ${xrdml}/XRD-918-16_10.nxs
read_nexus -f ${xrdml}/XRD-918-16_10.nxs > ${xrdml}/ref_nexus.log 2>&1
rm ${xrdml}/XRD-918-16_10.nxs

