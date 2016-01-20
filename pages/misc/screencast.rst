.. title: Control your phone via keyboard and mouse
.. slug: misc/screencast
.. date: 2016-01-20
.. tags:
.. category:
.. link:
.. description:
.. type: text

These instructions let you control your phone via a computer keyboard and
mouse, for example if your touchscreen is cracked.

This is only necessary on older phones. With more recent phones, you can just
plug in a mouse via a USB OTG cable, or a USB C cable (that entails OTG) for
the newest phones such as the Nexus 5X. (Supposedly you can also do this with
the Nexus 4 after some extra convoluted hacks, but I never managed to get that
working myself.)

Prepare
=======

0. On your computer, install :doc:`adb <android-overview>` and ``maven``.
1. On your phone, enable ADB. :doc:`Do this <misc/force-adb>` if necessary.

TODO: link to specific sections rather than entire page.

Run screencast
==============

These are the basic core instructions, which may need to be adapted depending
on your system::

  $ git clone https://github.com/xSAVIKx/AndroidScreencast && cd AndroidScreencast
  AndroidScreencast$ mvn package
  AndroidScreencast$ java -jar target/androidscreencast*.jar

If you're on Debian, you need to integrate the following:

- Before ``mvn package``::

    AndroidScreencast$ patch -p1 <<EOF
    diff --git a/pom.xml b/pom.xml
    index 1dc8e0a..40012d8 100644
    --- a/pom.xml
    +++ b/pom.xml
    @@ -89,7 +89,15 @@
      <pluginRepositories>
        <pluginRepository>
    +			<id>local</id>
    +			<url>file:///usr/share/maven-repo</url>
    +		</pluginRepository>
    +		<pluginRepository>
    +			<id>maven-apache</id>
    +			<url>https://repo.maven.apache.org/maven2/</url>
    +		</pluginRepository>
    +		<pluginRepository>
          <id>onejar-maven-plugin.googlecode.com</id>
    -			<url>http://onejar-maven-plugin.googlecode.com/svn/mavenrepo</url>
    +			<url>https://onejar-maven-plugin.googlecode.com/svn/mavenrepo</url>
        </pluginRepository>
      </pluginRepositories>
      <url>http://xsavikx.github.io/AndroidScreencast</url>
    EOF

- Before ``java -jar [..]``::

    AndroidScreencast$ socat TCP-LISTEN:5037,fork UNIX-CONNECT:/tmp/5037 &

  This is because Debian disables TCP-listen for the adb server by default, for
  security. If your non-Debian system does this, you'll need to run this too.
