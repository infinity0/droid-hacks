#!/bin/bash
# Get raw JSON data for a given client Id in Google Places.
# Very hacky, last tested 2019-10-22

set -e
arg="$1"

get_gmaps_cid() {
	local cid="$1"
	local out="${cid}.json"
	if [ -s "$out" -a "$OVERWRITE_GMAPS_JSON" != "1" ]; then return; fi
	curl -s "https://www.google.com/maps?cid=$((16#$cid))" | \
	sed -ne '/^;window.APP_INITIALIZATION_STATE=/,/^;/p' | \
	head -n-1 | tail -c+34 | jq > "$out"
	echo "$out"
}

if [ "${#arg}" = 16 ]; then
	get_gmaps_cid "$arg"
elif [ "${arg#https://}" != "${arg}" ]; then
	get_gmaps_cid "$(echo "$arg" | sed -Ee 's/.*0x\w+:0x(\w+).*/\1/g')"
else
	echo >&2 "not recognised: $arg"
	exit 1
fi
