#!/bin/sh
# Run this in /data/data/restore/ after you extract the backup.tar, and after
# opening up the app for the first time (so expected files are created).
set -e
package="$1"

cd "$(dirname "$(readlink -f "$0")")"

chmod 771 "$package"
chown -hR "$(stat -c %u:%g ../$package                    )" "$package"
chcon -hR "$(ls -Zd        ../$package     | cut '-d ' -f1)" "$package"
if [ -h ../$package/lib ]; then
	ln -snf   "$(readlink      ../$package/lib                )" "$package"/lib
	chown -h  "$(stat -c %u:%g ../$package/lib                )" "$package"/lib
	chcon -h  "$(ls -Zd        ../$package/lib | cut '-d ' -f1)" "$package"/lib
fi
chmod 751 "$package"
mv "../$package" "../_old_$package"
mv "$package" ..
