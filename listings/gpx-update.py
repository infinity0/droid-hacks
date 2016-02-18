#!/usr/bin/python
"""
Export KDE Marble KML bookmarks to OsmAnd GPX favourites.
Requires: python-lxml, gpsbabel

Usage: $0 EXPORT_DIR [EXPORT_FOLDER ..]
where
  EXPORT_DIR is where to write bookmarks.kml and favourites.gpx
  EXPORT_FOLDER are the bookmark folders (in Marble) to export

TODO: write this up in the main droid-hacks doc. Roughly:
- add this script to a crontab
- expose EXPORT_DIR via a stealth hidden service
- periodically download it to your phone
- su -c 'ln -sf ../Downloads/favourites.gpx /data/media/0/osmand/'
"""

import lxml.etree
import os.path
import subprocess
import sys

p = os.path.expanduser

def do_export(*args):
    export_dir = args[0]
    export_folders = frozenset(args[1:])

    kml_in = p("~/.local/share/marble/bookmarks/bookmarks.kml")
    kml_out = p("%s/bookmarks.kml" % export_dir)
    gpx_out = p("%s/favourites.gpx" % export_dir)

    r = lxml.etree.parse(kml_in)
    for e in r.findall("//k:Document/k:Folder", namespaces={"k":"http://www.opengis.net/kml/2.2"}):
        if e.getchildren()[0].text not in export_folders:
            r.getroot().getchildren()[0].remove(e)
    r.write(kml_out, encoding="utf-8", xml_declaration=True)

    subprocess.check_call(["/usr/bin/gpsbabel", "-i", "kml", "-o", "gpx", kml_out, gpx_out])
    return 0

if __name__ == "__main__":
    sys.exit(do_export(*sys.argv[1:]))
