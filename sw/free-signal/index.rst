.. title: Libre secure messaging with no-Google Signal
.. slug: sw/free-signal
.. date: 2016-02-06
.. tags:
.. category:
.. link:
.. description:
.. type: text

Signal is a free asynchronous messaging app with some very strong security
properties. It is far from perfect, but at the time of writing is probably the
best such app available for Android. Unfortunately, official builds depend on
Google Play Services (GMS) because it requires Google Cloud Messaging (GCM) as
a core part of the protocol. This page discusses how to have Signal *without*
GMS on your phone.

-----------------------------
You have an old trusted phone
-----------------------------

Use an old phone with GMS to do the Signal registration process on, using your
current SIM card. When you're done, you can move your SIM card back to your new
phone, then `migrate your keys over <#migrate-signal-to-a-new-phone>`_.

On the new phone, Signal will occasionally complain about the lack of GMS but
**it runs fine** - as opposed to auto-exiting if you haven't registered and
have no GMS to do that with. However, you won't have push notifications, so you
will need to periodically check it manually - just like your email. :)

--------------------------
You like to try new things
--------------------------

Add `Eutopia.cz F-Droid Experimental Repository`_ as an F-Droid repo. (If
you're reading this on your phone, you can copy the link and add it into
F-Droid directly.)

Refresh your repositories, then install **LibreSignal (Websocket)**. This will
replace any existing Signal app, but keep your keys and data. You will likely
need to perform another registration, but this one doesn't require GMS.

Push notifications do work here. This is because the Signal servers do support
the underlying push technology (WebSocket) for some non-Android clients, but
they just haven't made this work in their Android client yet due to resource
constraints and a negative attitude.

.. _Eutopia.cz F-Droid Experimental Repository: https://eutopia.cz/experimental/fdroid/repo?fingerprint=A0E4D1D912D8B81809AB18F5B7CF562CD1A10533ED4F7B25E595ABC8D862AD87

-----------------------------
Migrate Signal to a new phone
-----------------------------

1. On both phones, enable ADB. If you can't, then :doc:`try this <misc/force-adb>`.

2. On your new phone, install Signal (or `LibreSignal <#new-way>`_), start it once, then go
   to Settings / Apps / Signal then press "Force Stop".

3. Connect your old phone to your computer, then on the latter::

    $ adb root
    $ adb shell tar -C /data/user/0 -czf /data/user/0/signal.tar.gz org.thoughtcrime.securesms
    $ adb pull /data/user/0/signal.tar.gz
    $ adb shell rm /data/user/0/signal.tar.gz

4. Disconnect your old phone, and **put it in Airplane Mode**.

5. Connect your new phone to your computer, then on the latter::

    $ adb root
    $ adb push signal.tar.gz /data/user/0/  # the slash is important
    $ adb shell
      # cd /data/user/0
      # mv org.thoughtcrime.securesms _old_signal
      # tar -xzf signal.tar.gz
      # chmod 771 org.thoughtcrime.securesms
      # chown -R "$(stat -c %u:%g _old_signal)" org.thoughtcrime.securesms
      # chcon -R "$(ls -Zd _old_signal | cut '-d ' -f1)" org.thoughtcrime.securesms
      # chmod 751 org.thoughtcrime.securesms

6. Start Signal on your new phone, and check that everything still works. If it
   does, you can run::

    $ adb shell rm -rf /data/user/0/_old_signal
    $ adb shell rm /data/user/0/signal.tar.gz

   Or you can leave this until later, as a backup.

7. Disconnect your new phone. Uninstall Signal from your old phone **before**
   disabling Airplane Mode. If you don't do this, *both* of your installations
   will start to break as the cryptographic ratchet gets forked.
