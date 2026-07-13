#!/usr/bin/env bash

export PATH=$PATH:build/google-cloud-sdk/bin

mkdir build/ppm3_code/
gsutil cp "gs://opm-assets/ppm3_code/*" ./build/ppm3_code/
