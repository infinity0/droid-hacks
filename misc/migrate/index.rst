.. title: Migrating app data to a new phone
.. slug: misc/migrate
.. date: 2018-12-05
.. tags:
.. category:
.. link:
.. description:
.. type: text

The below guide was originally written for the Signal Messenger app, and I
haven't had time to generalise it to other apps yet. However I have personally
adapted them to successfully migrate my own data across phones.

In newer versions of Signal (4.16+) they decided to put user private keys in a
special place in the system (Android KeyStore) that "keeps it safe from
hackers" but unfortunately is totally untransparent to end-users, and can't be
easily backed-up even when you figure out what's going on. So the instructions
below won't actually work for Signal today. However, they can be adapted to
e.g. Silence, or pretty much any other app that doesn't use the KeyStore.

0. Download `<../../listings/restore-apk-data.sh.html>`_, have a read through
   it and understand what it does. Then push it to your new phone::

    $ adb root
    $ adb shell mkdir -p /data/user/0/restore
    $ adb push restore-apk-data.sh /data/user/0/restore/ # the slash is important

1. On both phones, enable ADB. If you can't, then :doc:`try this <misc/force-adb>`.

2. On your new phone, install Signal (or `LibreSignal <#new-way>`_), start it
   once, then go to Settings / Apps / Signal then press "Force Stop".

3. On your old phone, go to Settings / Apps / Signal then press "Force Stop".
   Then, **put your old phone in Airplane Mode**.

4. Connect your old phone to your computer, then on the latter::

    $ adb root
    $ adb shell tar -C /data/user/0 -czf /data/user/0/signal.tar.gz org.thoughtcrime.securesms
    $ adb pull /data/user/0/signal.tar.gz
    $ adb shell rm /data/user/0/signal.tar.gz

5. Disconnect your old phone from your computer.

6. Connect your new phone to your computer, then on the latter::

    $ adb root
    $ adb push signal.tar.gz /data/user/0/restore/ # the slash is important
    $ adb shell "cd /data/user/0/restore/ && tar -xzf signal.tar.gz"
    $ adb shell "cd /data/user/0/restore/ && ./restore-apk-data.sh org.thoughtcrime.securesms"

7. Start Signal on your new phone, and check that everything still works. If it
   does, you can run::

    $ adb shell rm -rf /data/user/0/_old_signal
    $ adb shell rm /data/user/0/signal.tar.gz

   Or you can leave this until later, as a backup.

8. Disconnect your new phone from your computer.

9. On your old phone, uninstall Signal **before** disabling Airplane Mode. If
   you don't do this, *both* of your installations will start to break as the
   cryptographic ratchet gets forked.
