#!/usr/bin/python
"""Sanitise Google Calendar exported data.

Last updated 2014-11; Google may have changed their export format since then.
Furthermore, this script is incomplete and only handles some parts of the
export format. You should manually review the output and decide if it needs
further sanitising. If so, please also send in a pull request.

Usage: $0 <exported XML> <exported ICS> <sanitised ICS>
"""

import os
import sys

from lxml import etree

dom = etree.XML(open(sys.argv[1]).read())
namespaces = dom.nsmap
namespaces["atom"] = namespaces[None]
entries = dom.findall(".//atom:entry", namespaces)

cat_by_uid = {}
cat_by_pub = {}

for entry in entries:
	uid = os.path.split(entry.find(".//atom:id", namespaces).text)[1]
	published = entry.find(".//atom:published", namespaces).text.strip().replace(":", "").replace("-", "").replace(".000", "")
	# Custom event categories written by Mozilla Lightning end up like this in Google Calendar.
	# Instead, let's put them in the more standard CATEGORIES field.
	category = entry.find(".//gd:extendedProperty[@name='X-MOZ-CATEGORIES']", namespaces)
	if category is not None:
		cat_by_uid[uid] = category.get("value")
		cat_by_pub[published] = category.get("value")

in_event = False
cur_event_lines = []
cur_uid = None
cur_created = None

with open(sys.argv[2]) as fp, open(sys.argv[3], "w") as wfp:
	for line in fp.readlines():
		if line.rstrip("\r\n") == "BEGIN:VEVENT":
			in_event = True
			cur_event_lines.append(line)
		elif line.rstrip("\r\n") == "END:VEVENT":
			cur_event_lines.append(line)
			wfp.write("".join(cur_event_lines))
			in_event = False
			cur_event_lines = []
			cur_uid = None
			cur_created = None
		elif not in_event:
			wfp.write(line)
		else:
			if ":" in line:
				head, tail = line.split(":", 1)
				if head == "UID":
					tail = tail.replace("@google.com", "")
					cur_uid = tail.strip("\r\n")
					#line = "%s:%s" % (head, tail)
				elif head == "CREATED":
					cur_created = tail.strip("\r\n")
				elif head == "CATEGORIES":
					if cur_uid in cat_by_uid:
						category = cat_by_uid[cur_uid]
					elif cur_created in cat_by_pub:
						category = cat_by_pub[cur_created]
					else:
						raise ValueError("not found: %s created %s" % (cur_uid, cur_created))
					line = "%s:%s\r\n" % (head, category)
			cur_event_lines.append(line)

#import code; code.interact(local=locals())
