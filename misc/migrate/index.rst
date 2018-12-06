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
      # package=org.thoughtcrime.securesms
      # mv "$package" _old_signal
      # tar -xzf signal.tar.gz
      # chmod 771 "$package"
      # chown -R "$(stat -c %u:%g _old_signal                    )" "$package"
      # chcon -R "$(ls -Zd        _old_signal     | cut '-d ' -f1)" "$package"
      # ln -snf  "$(readlink      _old_signal/lib                )" "$package"/lib
      # chown -h "$(stat -c %u:%g _old_signal/lib                )" "$package"/lib
      # chcon -h "$(ls -Zd        _old_signal/lib | cut '-d ' -f1)" "$package"/lib
      # chmod 751 "$package"

6. Start Signal on your new phone, and check that everything still works. If it
   does, you can run::

    $ adb shell rm -rf /data/user/0/_old_signal
    $ adb shell rm /data/user/0/signal.tar.gz

   Or you can leave this until later, as a backup.

7. Disconnect your new phone. Uninstall Signal from your old phone **before**
   disabling Airplane Mode. If you don't do this, *both* of your installations
   will start to break as the cryptographic ratchet gets forked.
