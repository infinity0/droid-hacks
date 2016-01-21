.. title: Basic setup: CyanogenMod with device encryption
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

3. Boot into system, then encrypt your phone (Android 6+ don't need this).

4. For future upgrades: Boot into recovery, decrypt the phone via ``adb shell
   twrp decrypt``, then install via ADB sideload as in (2).

None of our recommendations require you to install GAPPS. If you are content to
only use our recommendations, you can ignore other online instructions that
tell you to install it.

Recommended apps
================

All FOSS and available from F-Droid.

Core

* Barcode Scanner
* ConnectBot
* Cryptfs Password
* Hash Droid
* SnoopSnitch / AIMSICD

Comms

* ChatSecure, Conversations
* Orbot + Orwall
* Orfox
* SMSSecure

Data

* DAVDroid, see :doc:`sw/owndata`

Location

* µg UnifiedNlp + LocalGSMNlpBackend, :doc:`sw/location`
* OsmAnd~
* Transportr

Suggested apps
==============

FOSS and available from F-Droid:

* aLogcat ROOT
* AndIodine
* Open Camera
* Plumble

Non-free, or uses non-free or centralised services:

* Signal - ``org.thoughtcrime.securesms``

  * Despite the package name, it does not (any more) support "secure SMS", it
    is "secure XOR SMS". Use SMSSecure for "secure AND SMS". You should then
    use CM Privacy Guard to block this app from accidentally receiving SMS.
  * It **does** work without Google Play Services, it just won't have push
    notifications, so you will need to periodically check it manually - like
    checking your email.

* Google Keyboard - ``com.google.android.inputmethod.latin``
* Google Translate - ``com.google.android.apps.translate``

Ask a friend to download these from Google Play, then use `pull-apk.sh
<../../listings/pull-apk.sh.html>`_ to grab the APKs from their device, then
install them on your device.

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
