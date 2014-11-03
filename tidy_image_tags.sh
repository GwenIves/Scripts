#!/bin/env bash

# Strip personal information from image files passed as a command line parameter list

for f in "$@"
do
	[ ! -f "$f" ] && continue

	exiv2 -M "del Exif.Image.DocumentName" "$f"
	exiv2 -M "del Exif.Image.Artist" "$f"
	exiv2 -M "del Xmp.digiKam.ImageHistory" "$f"

	echo "Cleaned up $f"
done
