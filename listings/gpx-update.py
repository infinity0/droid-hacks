#!/usr/bin/python
"""
Export KDE Marble KML bookmarks to OsmAnd GPX favourites.
Requires: python-lxml, gpsbabel

Usage: $0 <EXPORT_FOLDER> ... < bookmarks.kml > favourites.gpx
       $0 -i favourites.gpx

EXPORT_FOLDER are the bookmark folders (in Marble) to export. The argument can
also be in the following extended syntax:

  EXPORT_FOLDER ::= (folder | gpx_file) "|" colour

gpx_file    is the path to an actual file to splice into the favourites as-is.
colour      is what colour to display those places in, in OsmAnd.

Use the -i option to install the output file into Android.

TODO: write this up in the main droid-hacks doc. Roughly:
- add this script to a crontab
- expose $(dirname favourites.gpx) via a stealth hidden service
- periodically download it to your phone
- su -c 'ln -sf ../Downloads/favourites.gpx /data/media/0/osmand/'

"""

from __future__ import print_function

from lxml import etree

import copy
import os.path
import subprocess
import sys

path = os.path.expanduser

NS = {
    "k":"http://www.opengis.net/kml/2.2",
    "g":"http://www.topografix.com/GPX/1/0",
}

def export(*args):
    kml_in = etree.parse(sys.stdin)
    fav = None
    fav_time = None
    fav_bounds = None

    for export in args:
        parts = export.split("|")
        if len(parts) == 2:
            folder, colour = parts
        elif len(parts) == 1:
            folder, colour = parts[0], None
        else:
            raise ValueError(export)

        if folder.endswith(".gpx"):
            fp = open(path(folder))
            folder = os.path.basename(folder)
        else:
            p = subprocess.Popen(["/usr/bin/gpsbabel", "-i", "kml", "-o", "gpx", "-f", "-", "-F", "-"],
                stdin=subprocess.PIPE,
                stdout=subprocess.PIPE)

            # filter only this folder
            r = copy.deepcopy(kml_in)
            for e in r.findall("//k:Document/k:Folder", namespaces=NS):
                if e.getchildren()[0].text != folder:
                    r.getroot().getchildren()[0].remove(e)
            r.write(p.stdin, encoding="utf-8", xml_declaration=True)
            p.stdin.close()
            fp = p.stdout

        # write the folder name into the GPX output of gpsbabel, otherwise it's lost
        g = etree.parse(fp)
        for e in g.findall("//g:wpt", namespaces=NS):
            t = e.makeelement('type')
            t.tail = e.text                                                     # i'm OCD, maintain indentation
            t.text = folder
            e.insert(0, t)
            i2, i1 = e.getchildren()[-2:]
            if colour:
                x = e.makeelement("extensions")
                c = e.makeelement("color")
                c.text = colour
                x.append(c)
                e.append(x)
                x.tail = i1.tail                                                # i'm OCD, maintain indentation
                i1.tail = i2.tail

        # merge the output into "fav"
        if fav is None:
            fav = g
            fav_time = fav.findall("//g:time", namespaces=NS)[0]
            fav_bounds = fav.findall("//g:bounds", namespaces=NS)[0]
        else:
            g_time = g.findall("//g:time", namespaces=NS)
            if g_time:
                g_time = g_time[0]
                if g_time.text > fav_time.text:
                    fav_time.text = g_time.text

            g_bounds = g.findall("//g:bounds", namespaces=NS)
            if g_bounds:
                g_bounds = g_bounds[0]
                if float(g_bounds.get("minlon")) < float(fav_bounds.get("minlon")):
                    fav_bounds.set("minlon", g_bounds.get("minlon"))
                if float(g_bounds.get("minlat")) < float(fav_bounds.get("minlat")):
                    fav_bounds.set("minlat", g_bounds.get("minlat"))
                if float(g_bounds.get("maxlon")) > float(fav_bounds.get("maxlon")):
                    fav_bounds.set("maxlon", g_bounds.get("maxlon"))
                if float(g_bounds.get("maxlat")) > float(fav_bounds.get("maxlat")):
                    fav_bounds.set("maxlat", g_bounds.get("maxlat"))

            for e in g.findall("//g:wpt", namespaces=NS):
                fav.getroot().getchildren()[-1].tail = g.getroot().text         # i'm OCD, maintain indentation
                fav.getroot().append(e)

    fav.write(sys.stdout, encoding="utf-8", xml_declaration=True)
    return 0

def install(f):
    subprocess.Popen(["sh"], stdin=subprocess.PIPE).communicate(input="""
pkg=net.osmand.plus
adb shell am force-stop $pkg
adb shell su -c "find /data/data/$pkg/ /sdcard/Android/data/$pkg/ -name 'favourites_*.gpx' -delete"
adb push "%s" /sdcard/Android/data/$pkg/files/favourites.gpx
""" % f)
    return 0

if __name__ == "__main__":
    if len(sys.argv) > 1 and sys.argv[1] == "-i":
        sys.exit(install(sys.argv[2]))
    else:
        sys.exit(export(*sys.argv[1:]))
