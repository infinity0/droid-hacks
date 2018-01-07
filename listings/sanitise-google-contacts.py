#!/usr/bin/python3
"""Sanitise Google Contacts exported data.

Last updated 2014-11; Google may have changed their export format since then.
Furthermore, this script is incomplete and only handles some parts of the
export format. You should manually review the output and decide if it needs
further sanitising. If so, please also send in a pull request.

Usage: $0 <CSV export> <sanitised VCF>
"""

import csv
import logging
import sys

logging.getLogger().setLevel(logging.INFO)

keys = []

def process_entry(k, v, types):
	if k.endswith(" - Type"):
		head, tail = k[:-7].rsplit(" ", 1)
		types[(head, tail)] = v
		return
	elif k.endswith(" - Value"):
		head, tail = k[:-8].rsplit(" ", 1)
		k = ":".join((head, types.get((head, tail), ""), tail))
	if " ::: " in v:
		return k, v.split(" ::: ")
	else:
		return k, v

def to_list(l):
	return l if type(l) == list else [l]

def dict_to_vcard(obj):
	lines = ["BEGIN:VCARD", "VERSION:2.1"]
	lines.append("FN:%s" % obj.pop("Name"))
	lines.append("N:%s;%s;%s;%s;%s" % (
		obj.pop("Family Name", ""),
		obj.pop("Given Name", ""),
		obj.pop("Additional Name", ""),
		obj.pop("Name Prefix", ""),
		obj.pop("Name Suffix", "")
	))
	for k in list(obj.keys()):
		if ":" not in k:
			continue
		head, tail, n = k.split(":")
		#pref = ";PREF" if n == 1 else ""
		vv = to_list(obj[k])

		if head == "Phone":
			head = "TEL"
		elif head == "E-mail":
			head = "EMAIL"
		elif head == "Website":
			head = "URL"
		else:
			continue

		tail = ("CELL" if (tail == "Mobile" and head == "TEL") else
				"HOME" if tail == "Home" else
				"WORK" if tail == "Work" else
				"X-%s" % tail if tail else "")
		if tail.startswith("X-"):
			logging.info("saw unusual %s type: %s", head, tail)

		for v in vv:
			if tail:
				lines.append("%s;%s:%s" % (head, tail, v))
			else:
				lines.append("%s:%s" % (head, v))
		del obj[k]

	if "Notes" in obj:
		lines.append("NOTE:%s" % obj.pop("Notes"))
	if "Organization 1 - Name" in obj:
		lines.append("ORG:%s" % obj.pop("Organization 1 - Name"))
	if "Group Membership" in obj:
		lines.append("CATEGORIES:%s" % ",".join(to_list(obj.pop("Group Membership"))))
	lines.append("END:VCARD")
	if obj:
		print("DROPPED data:", obj)
	return lines

with open(sys.argv[1], encoding="utf-16") as fp, open(sys.argv[2], "w") as wfp:
	reader = csv.reader(fp.readlines())
	for row in reader:
		if not keys:
			keys = row
			continue
		types = {}
		obj = dict(filter(None, [process_entry(k, v, types) for (k, v) in filter(lambda p: bool(p[1]), zip(keys, row))]))
		vcard = dict_to_vcard(obj)
		for line in vcard:
			print(line, file=wfp)
