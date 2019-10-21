#!/bin/sh
# Go through a Google Takeout "Saved" data dump and retrieve JSON data for all
# Places URLs listed in all of the CSV files.

set -e
sdir="$(dirname "$(readlink -f "$0")")"

mkdir -p json
for i in *.csv; do
	mkdir -p "${i%.csv}"
	sed -nEe 's,.*(https://.*),\1,gp' "$i" | while read url; do
		out="$( cd json && "$sdir/gmaps_get_cid.sh" "$url" )"
		if [ -n "$out" ]; then ln -sf "../json/$out" "${i%.csv}/$out"; fi
	done
done
