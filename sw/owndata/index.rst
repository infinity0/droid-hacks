.. title: Self-hosting your personal data
.. slug: sw/owndata
.. date: 2016-01-21
.. tags:
.. category:
.. link:
.. description:
.. type: text

Move your data onto infrastructure that you control, then access and work with
it from your phone later.

---------------------
Contacts and Calendar
---------------------

For now, we discuss Apple CalendarServer with DAVDroid. There are other
solutions that are similarly good, which we may cover in the future or accept
contributions to include.

You need to do the following steps:

* On your server, configure `CalendarServer <#configure-calendarserver>`_ and a
  `Tor stealth service <#configure-tor-stealth-service>`_.
* `Sanitise and import your data <#sanitise-and-import-your-old-data>`_.
* On each client device, configure `tor <#tor-on-a-client>`_ and `DAVDroid
  <#configure-a-client-device>`_.

Along the way, you'll also configure some other desktop clients to access your
server. This is useful for heavy editing tasks.

Configure CalendarServer
========================

For a Debian server, install::

  # aptitude install calendarserver postgresql

Read ``/usr/share/doc/calendarserver/README.Debian.gz`` on how to configure
postgresql for calendarserver. If you have calendarserver 7.0, this would be::

  $ sudo -u postgres createuser caldavd --no-createdb --no-createrole --no-superuser
  $ sudo -u postgres createdb --owner=caldavd caldav
  $ sudo -u caldavd psql -f /usr/lib/python2.7/dist-packages/txdav/common/datastore/sql_schema/current.sql caldav

Configure calendarserver::

  # SERVER_HOSTNAME="set-this-yourself.onion" # e.g. "caldavd.alice.stealth.onion"
  # cd /etc/caldavd && patch -p0 <<EOF
  --- caldavd.plist
  +++ caldavd.plist
  @@ -34,2 +34,2 @@
       <key>ServerHostName</key>
  -    <string></string> <!-- The hostname clients use when connecting -->
  +    <string>$SERVER_HOSTNAME</string> <!-- The hostname clients use when connecting -->
  @@ -63,3 +63,4 @@
       <key>BindAddresses</key>
       <array>
  +    <string>localhost</string>
       </array>
  EOF

For our purposes, we set an explicit server hostname and bind only to local
addresses. The former is necessary due to (a) our use of stealth onion services
and (b) calendarserver not being as smart as it could be. [#sn]_ The hostname
must end in ``.onion``; this is a restriction enforced for non-technical
reasons by tor, which might be lifted in the future.

.. [#sn] For a stealth service, each client has a *different* onion address
  (and authcookie) that it uses to access the service with. To make this work
  with calendarserver we use ``MapAddress``, which is like ``/etc/hosts`` for
  tor, and have every client use the same hostname alias for the server.

Add crontab entry to backup your data::

  # BACKUP_FILE="set-this-yourself.in-a-dir-where-caldavd-can-write"
  # { crontab -l; cat <<EOF; } | crontab -
  50  1  *  *  *  /usr/bin/sudo -u caldavd -g staff /usr/bin/pg_dump pg_dump -f "$BACKUP_FILE.$(date +%F)" caldav
  EOF

This **not optional** - if you don't do this, then none of the rest of the
stuff mentioned on this page will work, and the world will explode. Even worse,
Google SREs will start showing up at your house every day to laugh at you.

Configure ``/etc/caldavd/accounts.xml``. You can generate uuids with
``uuidgen``.

We're ready to start::

  # sed -i -e 's,#\?\(start_calendarserver="\?yes"\?\),\1,' /etc/default/calendarserver
  # service calendarserver restart

Configure Tor stealth service
=============================

This allows your client devices to access your calendarserver, without exposing
it to the rest of the internet, and without needing complex rules/mechanism to
bypass any NAT/firewall policies.

Add to ``/etc/tor/torrc``::

  HiddenServiceDir /var/lib/tor/hidden_service/
  HiddenServicePort 8008 127.0.0.1:8008
  HiddenServiceAuthorizeClient stealth $client_names

Here, ``$client_names`` is a comma-separated list of arbitrary names (i.e. you
make them up yourself), one for each device that will access your server. You
should make up at least two names - one for your phone, one for the desktop
machine you will use to sanitise and import your data from.

Restart tor, then find out your client addresses/authcookies::

  # service tor restart
  # cat /var/lib/tor/hidden_service/hostname

Note this information for later - your client devices will need it.

Sanitise and import your old data
=================================

To begin with, export your data from the Google web interface. This is more
accurate than doing it from client applications - since Google themselves know
what data they hold about you, whereas application authors may have missed some
things. Google offers several formats for export. Do them all, since certain
types of data are present in some formats but not others. For example (during
2014-11), Google loses event categories and contact groups when exporting VCF
and ICS respectively. You should export to CSV (contacts) and XML (calendar) as
well, and whatever else they've added in the meantime.

Make sure you sanitise your data - merge duplicate contacts, etc. This is quite
important; Google adds a lot of cruft and non-standard extensions to the data,
which can waste your time if imported as-is into another application. Here are
some sample scripts to help you:

* `Sanitise Google Contacts exported data <../../listings/sanitise-google-contacts.py.html>`_
* `Sanitise Google Calendar exported data <../../listings/sanitise-google-calendar.py.html>`_

Note though, that I wrote these quickly for myself - they might not cover all
the features of Google that *you* used, and Google may have changed the export
format since I wrote them. You should manually review the output.

When you are satisfied with the sanitised data, you can import it into your
server using one of the following clients. (You should first `configure tor
<#tor-on-a-client>`_).

You can also use these clients to further clean up your data, now or in the
future. I certainly find it much easier to perform mass edits from a desktop
machine than from a phone.

Import contacts data using Evolution
------------------------------------

* File / New / Address Book
* Type = WebDAV
* URL = ``http://$SERVER_HOSTNAME:8008/addressbooks/users/$YOU/addressbook/``

To import your contacts: File / Import

Import calendar data using Lightning / Iceowl
---------------------------------------------

* File / New / Calendar > On the Network
* Format = CalDAV
* Location = ``http://$SERVER_HOSTNAME:8008/calendars/users/$YOU/calendar/``
* Check "Offline Support" (optional)

To import your calendar: Events and Tasks / Import

Configure a client device
=========================

Tor on a client
---------------

Add to ``/etc/tor/torrc``::

  MapAddress $SERVER_HOSTNAME $client_hs_address
  HidServAuth $client_hs_address $client_hs_authcookie

Here, ``$client_hs_address`` is one of the addresses (you pick which one) that
your Tor stealth service generated.

This also works on Orbot - go into Settings and look for "Torrc Custom Config"
near the bottom.

Bypass Tor on a localhost client
````````````````````````````````

If you want to use a client *on the same machine as the server*, the above will
work, but it's better to avoid going through Tor completely. This is a bit more
fiddly: you can't just point the client at localhost because CalendarServer
only accepts requests to $SERVER_HOSTNAME and will get confused when getting
requests to other hosts. Instead, add this to ``/etc/hosts``::

  127.0.0.1 $SERVER_HOSTNAME

Then, when configuring your client programs, set a proxy exception for
``$SERVER_HOSTNAME``, so that it bypasses Tor. Of course, this only works if
your client supports proxy exceptions, which Mozilla applications do. (If you
can't use such a client, then I don't know of a good simple solution here.)

For Mozilla programs, you also need to set network.dns.blockDotOnion to false
(effectively only after a restart). If you're using Torbirdy, it resets the
proxy exception on every restart, so you'd need to set it manually again.

DAVDroid
--------

DAVDroid may be installed from F-Droid. It is not itself a client; rather it is
an accounts provider and data synchronizer. Configure your account:

* Settings > Accounts > DAVDroid > Login with URL and user name
* Base URL = ``http://$SERVER_HOSTNAME:8008/principals``
* Uncheck "Preemptive authentication"

Then, other client programs may access and act on the data in these accounts -
for example, the stock Android Contacts app and the stock Android Calendar app
(*not* Google Calendar).

If account sync fails, check that your Tor connection is stable by downloading
some things. Failing that, you can try to debug the issue via ``adb logcat``.

Random tip: the stock Contacts app does not support editing the groups of a
contact, but it can read and display this data if the server has it. You may
use Evolution (mentioned above, used to import old contacts data) to edit that.
