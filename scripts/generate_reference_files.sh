#!/bin/bash
function update_ref_file {
  local FOLDER=$1
  local NXDL=$2
  cd "$FOLDER"
  if [[ "$FOLDER" == "." ]]; then
    FOLDER="test"
  fi
  echo "Update $FOLDER reference file for $NXDL"
  files=$(find . -type f \( ! -name "*.log" -a ! -name "*.nxs" \))
  dataconverter ${files[@]} --reader $READER --nxdl $NXDL --ignore-undocumented --output "${FOLDER}_ref.nxs" # &> ref_output.txt
  cd ..
}

folders=(
  "xrdml_918-16_10"
)

READER="xrd"
nxdls=(
  "NXxrd_pan"
)

project_dir=$(dirname $(dirname $(realpath $0)))
cd $project_dir/tests/data

for folder in "${folders[@]}"; do
  for nxdl in "${nxdls[@]}"; do
    update_ref_file "$folder" "$nxdl"
  done
done