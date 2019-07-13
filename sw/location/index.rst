.. title: Free and privacy-respecting location providers
.. slug: sw/location
.. date: 2018-12-05
.. tags:
.. category:
.. link:
.. description:
.. type: text

----------
Background
----------

Currently, Android phones determine location by using GPS, as well as from
nearby cell tower and WiFi stations. GPS is accurate and privacy-preserving,
but takes a while to lock onto your position. The other two methods can give
you a rough idea of your location more quickly. However, they involve querying
remote proprietary databases that tell you which cell towers and WiFi stations
are near which locations. This reveals your location to the database provider,
as well as anyone that can read or break this communication.

In Android, that is handled by **Google Play Services** (GMS). In our
:doc:`basic setup <setup-enc-cm>`, we mentioned that we don't need this. It is
proprietary software and makes you economically dependent on a centralized
third party, and getting rid of such software is the aim of our game.

Instead, we use alternative FOSS to provide the equivalent service. However,
here you download the entire database periodically and do the lookups locally,
so that no remote parties to find out your location. As an added bonus, your
GPS will also be able to get a lock much more quickly, based on this data.

Yes, your mobile carrier can still determine your location, since they know
which cell towers you're connecting to. Given enough data, this will eventually
de-anonymise you even if you got a burner SIM card. However, the other benefits
mentioned above still remain. Also, it prepares the way (and is a necessary
pre-requisite) for eventually having fully location-private mobile networks in
the future. (More generally, if one needs to do A and B to achieve T, and doing
A is not feasible right now, it does not mean that doing B is pointless.)

------------
Instructions
------------

The steps are very simple but it makes your phone GPS so much more usable that
it deserves its own page:

- Follow (1) the installation instructions at `LineagoOS for microG`_ including
  (2) install SU for root access and (3) add the `microG Fdroid repo`_. If you
  choose to enable the MozillaNlpBackend and NominatimNlpBackend, you should
  probably also follow the instructions in :doc:`sw/firewall`.

- Install `LocalGsmNlpBackend`_, which lets you download global databases for
  cell tower locations, and query them later when your phone asks for location.
  We also encourage you to install other programs that let you contribute back
  to these public and open databases. (TODO: add some specific suggestions)

- At the time of writing, there are no downloadable global databases for WiFi
  station locations, but there is `LocalWifiNlpBackend`_. This remembers the
  location of nearby WiFi stations (using GPS) so that it will lock quicker the
  next time you're nearby. This can be useful if you go to a new place for a
  few days - after the first day or so, your GPS should lock quickly again. But
  you should switch it off when you are in a familiar place, to save battery.

After installing these, restart your phone, then follow further instructions
for *µg UnifiedNlp* which will take you through configuration steps for the
other programs as well.

Make sure it works
------------------

Install "GPSTest", "SatStat", and "HereGPS". Currently it's a bit stupid but
you do need to install all of them for the following functionality:

- GPSTest has a "clear AGPS" option
- SatStat has a "reload APGS" option
- HereGPS shows you *when* each source (Network, GPS) was last updated.

Annoyingly, I haven't found an app that contains all three features. >:[

``gps.conf`` is the important thing. This file is located in different paths
depending on your phone, use ``adb shell`` and ``find(1)`` to find it yourself.
We are now going to edit it, since the stock one provided by LineageOS is not
very suitable for many phones. You may need to run something like ``mount -o
remount,rw /vendor`` as root in adb if the partition containing ``gps.conf`` is
mounted read-only.

There is some good information about the file contents here:

https://rootzwiki.com/topic/28989-the-end-all-be-all-guide-to-your-gps/

Read the whole thread. Then to get you started, download one of these `custom
gps.conf`_ files. These are pretty good but still contain some mistakes, so
edit it further after downloading it, based on the above thread. For example, I
had to remove extraneous NTP servers and placeholder "FQDN" entries for
``SUPL_HOST`` and ``SUPL_TLS_HOST``. I also had to download the correct root
cert for the ``SUPL_TLS_HOST``::

  $ openssl s_client -connect $SUPL_TLS_HOST:$SUPL_SECURE_PORT -prexit -showcerts

It will output a bunch of stuff. Only proceed if near the bottom you see
"Verify return code: 0 (ok)". Then, find the root certificate (probably the
last one that was output), paste it into a new file ``SuplRootCert.pem``, then
run::

  $ openssl x509 -in SuplRootCert.pem -outform DER -out SuplRootCert

You can then copy ``SuplRootCert`` into your phone. Put it next to ``gps.conf``
and then set the entry for ``SUPL_TLS_CERT`` to point to it.

When you're all done, restart your phone and go somewhere with good GPS signal
(i.e. outside or near a window) and good cell signal. Then, use the apps I
mentioned above to make sure everything's working correctly. You might have to
dick around a bit, but hopefully the ``gps.conf`` tips helped a lot.

Next steps
----------

To replace **Google Maps**, use `OsmAnd+`_. It has completely offline vector
maps, that are incredibly detailed, with public transport and address data, as
well as offline navigation. The main downside is that redrawing the map when
you move or resize takes about 2-3 seconds, but you get used to it quickly.

Finally, don't forget to update your data every once in a while. Of the apps
mentioned on this page, that is *LocalGsmNlpBackend* which you access *via* the
*microG Services Core* app, and *OsmAnd~*. At present, neither of these apps
will alert you about out-of-date data, but in practice this hasn't been a
problem for me. Just remember to do it every month, or longer is probably fine
too - and you can even set a :doc:`calendar event <sw/owndata>` for that. :)

.. _LineagoOS for microG: https://lineage.microg.org/
.. _microG Fdroid repo: https://microg.org/fdroid.html
.. _LocalGsmNlpBackend: https://f-droid.org/repository/browse/?fdid=org.fitchfamily.android.gmslocation
.. _LocalWifiNlpBackend: https://f-droid.org/repository/browse/?fdid=org.fitchfamily.android.wifi_backend
.. _OsmAnd+: https://f-droid.org/repository/browse/?fdid=net.osmand.plus
.. _custom gps.conf: https://app.box.com/s/w57s1v1n3hie7l5lk28i
