find tests/data/xrdml_918-16_10  -type f ! -name '*.nxs' | xargs dataconverter --nxdl NXxrd_pan --reader xrd --output XRD-918-16_10.nxs
find tests/data/xrdml_918-16_10 -type f -name '*.nxs' | xargs mv XRD-918-16_10.nxs
