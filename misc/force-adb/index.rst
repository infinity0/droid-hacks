.. title: Enable ADB in highly-constrained situations
.. slug: misc/force-adb
.. date: 2016-01-20
.. tags:
.. category:
.. link:
.. description:
.. type: text

"Highly-constrained" means that, for whatever reason, you can't go into the
"Developer options" menu to enable "Android debugging" yourself. For example,
your screen is cracked, or you forgot your screen unlock password.

However, you still need some physical way of communicating with your phone's
ADB service *after* enabling it. These instructions won't work if your USB port
is broken.

--------------------------------
Nexus 4, CM 12.1 / Android 5.1.1
--------------------------------

The instructions below assume that your device is encrypted, and that you need
an ``adb shell`` both before and after decryption. If your requirements are
less than this, you should be able to adapt the instructions accordingly.

They also assume that you've used your computer to debug your phone before -
i.e. that it is already authorized to debug your phone. If you haven't done
this before, don't worry - you can adapt the instructions below to authorize
your computer, but I've forgotten how exactly. TODO: dig this information out
again from the depths of the internet, and add it.

Prepare
=======

0. On your computer, install :doc:`adb and fastboot<android-overview>`,
   ``sqlite3`` and ``abootimg``.
1. On your phone, install :doc:`TWRP <setup-enc-cm>`.

TODO: link to specific sections rather than entire page.

Enable after decrypt
====================

This enables ADB after you decrypt your data partition.

Boot into TWRP recovery, then from your computer::

  $ adb shell
   # twrp decrypt $YOUR_PASSWORD
   # mount /system
   # echo "persist.service.adb.enable=1" >> /system/build.prop
   # echo "persist.service.debuggable=1" >> /system/build.prop
   # echo "persist.sys.usb.config=mtp,adb" >> /system/build.prop
   # exit
  $ echo -n 'mtp,adb' > /data/property/persist.sys.usb.config
  $ adb pull "/data/data/com.android.providers.settings/databases/settings.db"
  $ sqlite3 settings.db 'update "global" set value=1 where name == "adb_enabled";'
  $ sqlite3 settings.db 'update "global" set value=1 where name == "development_settings_enabled";'
  $ adb push settings.db "/data/data/com.android.providers.settings/databases/settings.db"
  $ adb shell chown system: "/data/data/com.android.providers.settings/databases/settings.db"
  $ adb shell chmod 660 "/data/data/com.android.providers.settings/databases/settings.db"

See also https://android.stackexchange.com/questions/112040/ which gives
details for other android versions.

Enable before decrypt
=====================

This enables ADB while Android is still booting up, *before* you decrypt your
data partition.

Boot into TWRP recovery, then from your computer::

  $ adb shell twrp decrypt
  $ adb shell twrp backup B
  $ adb pull /sdcard/TWRP/BACKUPS/*/*/boot.emmc.win boot.img
  $ mkdir boot && cd boot
  boot$ abootimg -x ../boot.img
  boot$ mkdir initrd && cd initrd
  boot/initrd$ cat ../initrd.img | gunzip | cpio -vid
  boot/initrd$ sed -e 's/\(ro.*\.secure\)=1/\1=0/g' -i default.prop
  boot/initrd$ find . | cpio --create --format='newc' | gzip > ../initrd-adb.img
  boot/initrd$ cd ..
  boot$ abootimg --create boot-adb.img -f bootimg.cfg -k zImage -r initrd-adb.img
  boot$ adb reboot bootloader
  boot$ fastboot boot boot-adb.img

Or to install this permanently so you don't need to keep running the last
``fastboot boot`` command::

  boot$ fastboot flash boot boot-adb.img

Note that any attacker with physical access to the phone can do the equivalent
of above - even though ``twrp backup`` command requires a decrypted ``/data``
to dump the backup into, an attacker could execute the same functionality and
dump it to an unencrypted location.

This is an inherent danger of rooting your device. But the proper solution to
defend against this, is to develop better security architectures that place
authority (to execute bootstrap code) in the user's hands, instead of in the
hands of a third party then claim it's "for security" (as "locked" phones do).
