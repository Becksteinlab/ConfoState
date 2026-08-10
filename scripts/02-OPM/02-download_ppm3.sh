#!/usr/bin/env bash
# https://docs.aws.amazon.com/boto3/latest/

export PATH=$PATH:build/google-cloud-sdk/bin

mkdir build/ppm3_code/
gsutil cp "gs://opm-assets/ppm3_code/*" ./build/ppm3_code/
