#!/usr/bin/env bash
VERSION=`perl -ne 'm/<addon.*?version="(.*?)"/ && print "$1\n"' addon.xml`
ADDON_ID=`perl -ne 'm/<addon.*?id="(.*?)"/ && print "$1\n"' addon.xml`
OUTPUT_FILE="$ADDON_ID.$VERSION.zip"
ADDON_CODE_DIR=`basename "$PWD"`
BUILD_DIR="$ADDON_CODE_DIR/build/"

cd ..
rm $OUTPUT_FILE
zip -r $OUTPUT_FILE $ADDON_CODE_DIR -x "*.sh" -x "*.git*" -x ".DS_Store"
mkdir -p $BUILD_DIR
mv $OUTPUT_FILE $BUILD_DIR
