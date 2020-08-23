.. title: Basic setup: microG LineageOS with device encryption
.. slug: setup-enc-cm
.. date: 2016-01-21
.. tags:
.. category:
.. link:
.. description:
.. type: text

TODO: write this up properly, including reasons (e.g. tradeoffs vs AOSP, vs
stock Google, vs Replicant, etc)

Rough steps
===========

0. Unlock your bootloader.

1. Boot into bootloader, then install TWRP recovery. (Ignore official CM
   instructions that tell you to install ClockworkMod - TWRP is better.)

2. Boot into recovery, then install via ADB sideload.

3. Boot into system, then encrypt your phone (Android > 6 doesn't need this,
   it's all encrypted by default).

   TODO: how to set a more complex password for the initial bootup decryption?
   Previously could be achieved with "Cryptfs Password" but it's no longer
   compatible with Android 7+.

4. For future upgrades: Boot into recovery, decrypt the phone via ``adb shell
   twrp decrypt``, then install via ADB sideload as in (2).

None of our recommendations require you to install GAPPS. If you are content to
only use our recommendations, you can ignore other online instructions that
tell you to install it.

Recommended apps
================

All F-Droid FOSS

System, should be already installed as part of microG LineageOS

* F-Droid, F-Droid Privileged Extension
* microG Services Core, (MozillaNlpBackend), (NominatimNlpBackend)

Comms and security

* AFWall+, Orbot
* andOTP, ConnectBot
* Conversations, Silence, Signal
* Orfox
* SnoopSnitch / AIMSICD
* WifiAnalyzer

Personal data

* DAVx5, Tasks, see :doc:`sw/owndata`

Location

* LocalGSMNlpBackend, LocalWifiNlpBackend, see :doc:`sw/location`
* GPSTest, SatStat
* Mozilla Stumbler
* OsmAnd~
* Sky Map (FOSS by Google)
* Transportr

Utilities

* Barcode Scanner
* Equate
* Fennec F-Droid
* Giggity
* Hash Droid
* NewPipe

Suggested apps
==============

F-Droid FOSS
------------

* aLogcat ROOT
* AndIodine
* ApkTrack
* Auto Updater for Chromium
* Open Camera
* Plumble

Not from F-Droid, but microG-compatible
---------------------------------------

* Google Gboard (keyboard with swipe)
* Google Maps
* Google Translate
* Revolut
* Songkick
* Soundcloud
* Spotify
* VLC

Ask a friend to download these from Google Play, then use `pull-apk.sh
<../../listings/pull-apk.sh.html>`_ to grab the APKs from their device, then
install them on your device. Later, most of them are updateable from ApkTrack
so you only have to do this process once.

Disable stock apps
==================

Optionally, disable these stock apps (perhaps after setting the relevant ones
from above to perform the action that they're responsible for):

* Browser
* Camera
* Email
* Messenger
* Telephone

If you can't disable them, either leave them as-is or install "/system/app
mover" from F-Droid to forcibly remove them. TODO: test this personally.
