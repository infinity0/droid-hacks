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

For now, we discuss Radicale with DAVx5. There are other solutions that are
similarly good, which we may cover in the future or accept contributions to
include. (The previous version of this guide used Apple CalendarServer, but
that has been discontinued. Radicale is much simpler to set up anyway.)

You need to do the following steps:

* On your server, configure `Radicale <#configure-radicale>`_ and a
  `Tor stealth service <#configure-tor-stealth-service>`_.
* On each client device, configure `tor <#tor-on-a-client>`_ and `DAVx5
  <#configure-a-client-device>`_.
* `Sanitise and import your data <#sanitise-and-import-your-old-data>`_.

Along the way, you'll also configure some other desktop clients to access your
server. This is useful for heavy editing tasks.

Configure Radicale
==================

The Radicale website has `excellent highly-detailed documentation
<https://radicale.org/3.0.html#tutorials/basic-configuration/storage>`_
already. OTOH our instructions below are more concise and fine-tuned for Debian
and Tor Stealth Hidden Services.

For a Debian server, install::

  # aptitude install radicale python3-passlib

Configure users::

  $ sudo htpasswd -B -c /etc/radicale/users $USER

Edit ``/etc/radicale/config`` to contain the following::

  [auth]
  type = htpasswd
  htpasswd_filename = /etc/radicale/users
  htpasswd_encryption = bcrypt

Use something like ``rsnapshot(1)`` to back up ``/var/lib/radicale/collections``.
This **not optional** - if you don't do this, then none of the rest of the
stuff mentioned on this page will work, and the world will explode. Even worse,
Google SREs will start showing up at your house every day to laugh at you.

We're ready to start::

  # systemctl enable radicale
  # systemctl start radicale

In your web browser, go to ``localhost:5232``, log in, then create an
"addressbook" and a "calendar, journal and tasks". You will end up with 2
collections each with a URL with the collection UUID at the end, like
``http://localhost:5232/$YOU/$COLLECTION/``. Note these for later.

Configure Tor stealth service
=============================

This allows your client devices to access your server, without exposing it to
the rest of the internet, and without needing complex rules/mechanism to bypass
any NAT/firewall policies.

Add to ``/etc/tor/torrc``::

  HiddenServiceDir /var/lib/tor/hidden_service/
  HiddenServicePort 5232 127.0.0.1:5232
  HiddenServiceAuthorizeClient stealth $client_names

Here, ``$client_names`` is a comma-separated list of arbitrary names (i.e. you
make them up yourself), one for each device that will access your server. You
should make up at least two names - one for your phone, one for the desktop
machine you will use to sanitise and import your data from.

Restart tor, then find out your client addresses/authcookies::

  # service tor restart
  # cat /var/lib/tor/hidden_service/hostname

Note this information for later - your client devices will need it.

Configure a client device
=========================

Tor on a client
---------------

Add to ``/etc/tor/torrc``::

  MapAddress $SERVER_HOSTNAME $client_hs_address
  HidServAuth $client_hs_address $client_hs_authcookie

Here, ``$client_hs_address`` is one of the addresses (you pick which one) that
your Tor stealth service generated. ``$SERVER_HOSTNAME`` is something you make
up for your own reference, but it must end in `.onion`; this is a restriction
enforced for non-technical reasons by tor, which might be lifted in the future.

This also works on Orbot - go into Settings and look for "Torrc Custom Config"
near the bottom. With Android 10+ you also need to disable "Private DNS" in
your system settings, see `guardianproject/orbot#262
<https://github.com/guardianproject/orbot/issues/262>`_ for discussion.

Test web UI
-----------

Test that you can actually access Radicale via your stealth service by going to
``http://$SERVER_HOSTNAME:5232`` from a Tor-enabled web browser. For Mozilla
programs such as Firefox or Fennec on Android, you'll need to set
``network.dns.blockDotOnion`` to false in ``about:config`` (effectively only
after a restart). If you're using Torbirdy, it unfortunately resets the proxy
exception on every restart, so you need to set it manually every time.

DAVx5
-----

DAVx5 may be installed from F-Droid. It is not itself a client; rather it is
an accounts provider and data synchronizer. Configure your account:

* Settings > Accounts > DAVx5 > Login with URL and user name
* Base URL = ``http://$SERVER_HOSTNAME:5232``

Then, other client programs may access and act on the data in these accounts -
for example, the stock Android Contacts app and the stock Android Calendar app
(*not* Google Calendar).

For "Contact group method", either choice is fine and totally up to you. I
personally prefer "Groups are per-contact categories" as mine are more fluid
and informal. Since Android 10+ the stock Contacts app can edit these fine.

If account sync fails, check that your Tor connection is stable by downloading
some large things. Failing that, try to debug via ``adb logcat``.

Since this is going over Tor, the first sync may take a few minutes. Be patient
and try again several times, if the sync only appears to get part of your data.

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
* Type = CardDAV
* URL = ``http://$SERVER_HOSTNAME:5232/$YOU/$COLLECTION/``

Go to Edit > Preferences > Network Preferences, add a new proxy by clicking the
"+" button near the bottom, call it "Tor", and configure its address. Have your
address book use this proxy, in "Apply custom proxy settings to these accounts".

To import your contacts: File / Import

Import calendar data using Lightning / Iceowl
---------------------------------------------

* File / New / Calendar > On the Network
* Format = CalDAV
* Location = ``http://$SERVER_HOSTNAME:5232/$YOU/$COLLECTION/``
* Check "Offline Support" (optional)

To import your calendar: Events and Tasks / Import
