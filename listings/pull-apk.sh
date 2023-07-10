#!/bin/sh
# Pull APKs of installed applications from an Android device.
#
# Reads package names on STDIN, then pulls these using adb(1).
# You can see the package name of an app by going to Settings > Apps
#
# $ ./pull-apk.sh <<EOF
# com.google.android.gms
# EOF
#
# You can then install these on another device with:
#
# $ adb install com.aurora.store_45-0.apk                   # install new
# $ adb install -r com.aurora.store_45-0.apk                # upgrade existing
# $ adb install-multiple com.twitter.android_VERSION-*.apk  # install multi-apk package
#
set -e
ANDROID_USER="${ANDROID_USER:-0}"

while read pkg; do
  ver="$(adb shell -n pm list packages --show-versioncode "$pkg" | sed -nre 's/.* versionCode://p' || true)"
  if [ -z "$ver" ]; then
    echo >&2 "no version found for: $pkg"
    continue
  fi
  echo "-- $pkg $ver"
  i=0
  adb shell -n pm path --user "$ANDROID_USER" "$pkg" | sed -nre 's/^package://p' | while read path; do
    adb pull "$path" "${pkg}_${ver}-${i}.apk"
    echo "${pkg}_${ver}-${i}.apk"
    i=$((i + 1))
  done
done
