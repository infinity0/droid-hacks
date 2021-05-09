.. title: Enforce internet access through Tor
.. slug: sw/firewall
.. date: 2018-12-05
.. tags:
.. category:
.. link:
.. description:
.. type: text

Block unwanted internet access system-wide, and force other traffic through
Tor. Of course, one can add exceptions to allow specific applications to access
the internet directly.

Previously I achieved this through Orwall, but that is no longer maintained and
has several open bugs that need awkward manual work-arounds. The following
approach seems to work better for me, pending clarification of `this issue`_.

.. _this issue: https://github.com/ukanth/afwall/issues/789

----------
Android 10
----------

AFWall+

* Preferences > Rules/Connectivitey > LAN control [check]
* Preferences > Rules/Connectivitey > VPN control [check]
* Mode: Allow selected
* Applications rules:

  ==== ==== ==== ==== ============================== ======================================
  LAN  WiFi Data VPN  Application                    Reason why it shouldn't go through Tor
  ==== ==== ==== ==== ============================== ======================================
  .    .    .    Y    Any app
  Y    Y    Y    Y    Orbot                          Ofc Orbot itself can't go through Tor
  Y    Y    Y    Y    (any other apps you want to bypass Tor)
  ---- ---- ---- ---- ---------------------------------------------------------------------
  .    .    Y    Y    (root)                         Mobile internet, need it before Orbot can even access internet
  .    .    Y    Y    Phone Services, (..)           Mobile internet, need it before Orbot can even access internet
  .    Y    Y    Y    NetworkPermissionConfig, (..)  Internet connectivity detection
  .    Y    Y    Y    (gps)                          AGPS, Orbot can't intercept this
  .    Y    Y    Y    (ntp)                          AGPS, Orbot can't intercept this
  Y    Y    Y    Y    (tethering)                    Tethering, Orbot can't intercept this
  Y    .    .    Y    VLC                            Chromecast, don't want to put this through Tor
  ==== ==== ==== ==== ============================== ======================================

Orbot

* Menu > Apps VPN mode [toggle on]
* Apps > select the apps you want to force through Tor, which should at the
  very least include:

  * microG Services Core
  * Mozilla UnifiedNlp Backend
  * Mozilla Stumbler
  * Nominatim Geocoder Backend
  * GSM Location Service
  * SatStat
  * Updater -- i.e. LineageOS Updater
