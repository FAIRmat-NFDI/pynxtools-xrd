# #!/bin/sh

# # Update nexus file in tests/data directory

# set -e
# scpt_dir=$(dirname $0)
# root_dir=$(dirname $scpt_dir)

# # # STS Nanonis 5e
# echo " !!! Converting Nanonis STS data !!! "

# sts_5e_default_config=${root_dir}/tests/data/nanonis/sts/version_gen_5e_default_config
# find $sts_5e_default_config -type f ! \( -name '*.log -o -name *.nxs' \) | xargs dataconverter --nxdl NXsts --reader spm --output ${sts_5e_default_config}/sts_5e_default_config.nxs #--skip-verify
# read_nexus -f $sts_5e_default_config/sts_5e_default_config.nxs > ${sts_5e_default_config}/ref_nexus.log 2>&1
# rm ${sts_5e_default_config}/sts_5e_default_config.nxs

# sts_5e_with_described_nxdata=${root_dir}/tests/data/nanonis/sts/version_gen_5e_with_described_nxdata
# find ${sts_5e_with_described_nxdata} -type f ! \( -name '*.nxs' -o -name '*.log' \) | xargs dataconverter --nxdl NXsts --reader spm --output ${sts_5e_with_described_nxdata}/sts_5e_with_described_nxdata.nxs #--skip-verify
# read_nexus -f ${sts_5e_with_described_nxdata}/sts_5e_with_described_nxdata.nxs > ${sts_5e_with_described_nxdata}/ref_nexus.log 2>&1
# rm ${sts_5e_with_described_nxdata}/sts_5e_with_described_nxdata.nxs

# sts_5_with_described_nxdata=${root_dir}/tests/data/nanonis/sts/version_gen_5_with_described_nxdata
# find ${sts_5_with_described_nxdata} -type f ! \( -name '*.nxs' -o -name '*.log' \) | xargs dataconverter --nxdl NXsts --reader spm --output ${sts_5_with_described_nxdata}/sts_5_with_described_nxdata.nxs #--skip-verify
# read_nexus -f ${sts_5_with_described_nxdata}/sts_5_with_described_nxdata.nxs > ${sts_5_with_described_nxdata}/ref_nexus.log 2>&1
# rm ${sts_5_with_described_nxdata}/sts_5_with_described_nxdata.nxs

# # STM Nanonis 5e and 5
# echo " !!! Converting Nanonis STM data !!! "

# stm_5e_with_described_nxdata=${root_dir}/tests/data/nanonis/stm/version_gen_5e_with_described_nxdata
# find ${stm_5e_with_described_nxdata} -type f ! \( -name '*.nxs' -o -name '*.log' \) | xargs dataconverter --nxdl NXstm --reader spm --output ${stm_5e_with_described_nxdata}/stm_5e_with_described_nxdata.nxs
# read_nexus -f ${stm_5e_with_described_nxdata}/stm_5e_with_described_nxdata.nxs > ${stm_5e_with_described_nxdata}/ref_nexus.log 2>&1
# rm ${stm_5e_with_described_nxdata}/stm_5e_with_described_nxdata.nxs

# stm_5_with_described_nxdata=${root_dir}/tests/data/nanonis/stm/version_gen_5_with_described_nxdata
# find ${stm_5_with_described_nxdata} -type f ! \( -name '*.nxs' -o -name '*.log' \) | xargs dataconverter --nxdl NXstm --reader spm --output ${stm_5_with_described_nxdata}/stm_5_with_described_nxdata.nxs
# read_nexus -f ${stm_5_with_described_nxdata}/stm_5_with_described_nxdata.nxs > ${stm_5_with_described_nxdata}/ref_nexus.log 2>&1
# rm ${stm_5_with_described_nxdata}/stm_5_with_described_nxdata.nxs

# stm_5_with_default_config=${root_dir}/tests/data/nanonis/stm/version_gen_5_with_default_config
# find ${stm_5_with_default_config} -type f ! \( -name '*.nxs' -o -name '*.log' \) | xargs dataconverter --nxdl NXstm --reader spm --output ${stm_5_with_default_config}/stm_5_with_default_config.nxs
# read_nexus -f ${stm_5_with_default_config}/stm_5_with_default_config.nxs > ${stm_5_with_default_config}/ref_nexus.log 2>&1
# rm ${stm_5_with_default_config}/stm_5_with_default_config.nxs


# # STM Omicron
# echo " !!! Converting Omicron STM data !!! "

# afm_default_config=${root_dir}/tests/data/omicron/stm/default_config

# find ${afm_default_config} -type f ! \( -name '*.nxs' -o -name '*.log' \) | xargs dataconverter --nxdl NXstm --reader spm --output ${afm_default_config}/afm_omicron_default_config.nxs
# read_nexus -f ${afm_default_config}/afm_omicron_default_config.nxs > ${afm_default_config}/ref_nexus.log 2>&1
# rm ${afm_default_config}/afm_omicron_default_config.nxs


# # # # # AFM Nanonis 4
# echo " !!! Converting Nanonis AFM data !!! "

# afm_4_with_default_config=${root_dir}/tests/data/nanonis/afm/version_gen_4_default_config
# find ${afm_4_with_default_config} -type f ! \( -name '*.nxs' -o -name '*.log' \) | xargs dataconverter --nxdl NXafm --reader spm --output ${afm_4_with_default_config}/afm_4_with_default_config.nxs
# read_nexus -f ${afm_4_with_default_config}/afm_4_with_default_config.nxs > ${afm_4_with_default_config}/ref_nexus.log 2>&1
# rm ${afm_4_with_default_config}/afm_4_with_default_config.nxs

# afm_4_with_described_nxdata=${root_dir}/tests/data/nanonis/afm/version_gen_4_with_described_nxdata
# find ${afm_4_with_described_nxdata} -type f ! \( -name '*.nxs' -o -name '*.log' \) | xargs dataconverter --nxdl NXafm --reader spm --output ${afm_4_with_described_nxdata}/afm_4_with_described_nxdata.nxs
# read_nexus -f ${afm_4_with_described_nxdata}/afm_4_with_described_nxdata.nxs > ${afm_4_with_described_nxdata}/ref_nexus.log 2>&1
# rm ${afm_4_with_described_nxdata}/afm_4_with_described_nxdata.nxs


#!/bin/bash
READER=xrd

# Function to update log
function update_log {
  local FOLDER=$1
  local NXDL=$2
  local lowercase_NXDL=$(echo "$NXDL" | tr '[:upper:]' '[:lower:]')
  local ref_file="ref_nexus.log"
  log_filename="${FOLDER}/${ref_file}"
  echo "Generating log file at $log_filename..."
  python -c "
import os
from pynxtools.testing.nexus_conversion import get_log_file
folder = os.path.join(os.getcwd(), 'tests', 'data', '$FOLDER')
nxs_filepath = os.path.join(folder,'output.nxs')
log_filepath = os.path.join(folder,'$log_filename')
get_log_file(nxs_filepath, log_filepath, './')
"
  echo "Done!"
  echo
}

function update_log_file {
  local FOLDER=$1
  local NXDL=$2
  cd $FOLDER || exit
  echo "Update $FOLDER reference log for $NXDL"
  files=$(find . -type f \( ! -name "*.log" -a ! -name "*.nxs" \))
  dataconverter ${files[@]} --reader $READER --nxdl $NXDL --ignore-undocumented
  cd ../../.. || exit
  update_log "$FOLDER" "$NXDL"
  find $FOLDER -type f -name "output.nxs" | xargs rm 
}

project_dir=$(dirname $(dirname $(realpath $0)))

folders=(
  "${project_dir}/tests/data/xrdml_918-16_10"
)

nxdls=(
  "NXxrd_pan"
)

for folder in "${folders[@]}"; do
  for nxdl in "${nxdls[@]}"; do
    cd $folder
    update_log_file "$folder" "$nxdl"
  done
done