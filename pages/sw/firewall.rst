.. title: Enforce internet access through Tor
.. slug: sw/firewall
.. date: 2017-12-26
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

-------------
Android 7.1.1
-------------

AFWall+

* Preferences > Rules/Connectivitey > LAN control [check]
* Preferences > Rules/Connectivitey > VPN control [check]
* Mode: Allow selected
* Applications rules:
  * Orbot:       Allow LAN, WiFi, Mobile
  * (tethering): Allow LAN, VPN
  * (Any app):   Allow VPN
  * [bypass]:    Allow LAN, WiFi, Mobile [i.e. same as Orbot]

Orbot

* Menu > Apps VPN mode [toggle on]
* Apps > select the apps you want to force through Tor
