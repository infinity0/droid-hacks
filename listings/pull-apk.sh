#!/bin/sh
# Pull APKs of installed applications from an Android device.
#
# Reads package names on STDIN, then pulls these using adb(1).
# You can see the package name of an app by going to Settings > Apps
#
# $ ./pull-apk.sh <<EOF
# com.android.vending
# com.google.android.apps.maps
# com.google.android.gms
# com.google.android.youtube
# de.srlabs.snoopsnitch
# edu.cmu.cylab.starslinger
# info.guardianproject.otr.app.im
# org.thoughtcrime.redphone
# org.thoughtcrime.securesms
# EOF
#
# You can then install these on another device with:
#
# $ adb install $local_apk_file # install new
# $ adb install -r $local_apk_file # upgrade existing
#
while read x; do
	path="$(adb shell pm path "$x" | sed -e 's/\r//g')"
	path="${path#package:}"
	echo >&2 "pull $path"
	adb pull "$path"
done
