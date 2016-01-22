.. title: Free and privacy-respecting location providers
.. slug: sw/location
.. date: 2016-01-21
.. tags:
.. category:
.. link:
.. description:
.. type: text

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

The steps are very simple but it makes your phone GPS so much more usable that
it deserves its own page:

- Install `µg UnifiedNlp for GAPPS-free devices`_. This assumes your phone is
  based on Android 4.4 or above, and doesn't have GMS. If this doesn't apply to
  you, see the `other editions of µg UnifiedNlp`_. It is FOSS and a modular
  replacement for GMS, that delegates to external programs such as the ones
  below to perform the actual location lookups.

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

To replace **Google Maps**, use `OsmAnd+`_. It has completely offline vector
maps, that are incredibly detailed, with public transport and address data, as
well as offline navigation. The main downside is that redrawing the map when
you move or resize takes about 2-3 seconds, but you get used to it quickly.

Finally, don't forget to update your data every once in a while. Of the apps
mentioned on this page, that is *LocalGsmNlpBackend* which you access *via* the
*UnifiedNlp* app, and *OsmAnd~*. At present, neither of these apps will alert
you about out-of-date data, but in practice this hasn't been a problem for me.
Just remember to do it every month, or longer is probably fine too - and you
can even set a :doc:`calendar event <sw/owndata>` for that. :)

.. _µg UnifiedNlp for GAPPS-free devices: https://f-droid.org/repository/browse/?fdid=com.google.android.gms
.. _other editions of µg UnifiedNlp: https://f-droid.org/repository/browse/?fdfilter=%C2%B5g+UnifiedNlp
.. _LocalGsmNlpBackend: https://f-droid.org/repository/browse/?fdid=org.fitchfamily.android.gmslocation
.. _LocalWifiNlpBackend: https://f-droid.org/repository/browse/?fdid=org.fitchfamily.android.wifi_backend
.. _OsmAnd+: https://f-droid.org/repository/browse/?fdid=net.osmand.plus
