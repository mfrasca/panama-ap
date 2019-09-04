# -*- coding: utf-8 -*-
#
# Copyright (c) 2019 Mario Frasca <mario@anche.no>
#
# This file is part of panama-ap.
#
# panama-ap is free software: you can redistribute it and/or modify
# it under the terms of the GNU General Public License as published by
# the Free Software Foundation, either version 3 of the License, or
# (at your option) any later version.
#
# panama-ap is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE. See the
# GNU General Public License for more details.
#
# You should have received a copy of the GNU General Public License
# along with panama-ap. If not, see <http://www.gnu.org/licenses/>.
#

import sys
import utm
source = iter(sys.stdin.readline, '')
points = []
fictive_ids = {}
while True:
    three_lines = []
    for line in source:
        three_lines.append(line.replace('\n', ''))
        if len(three_lines) == 3:
            break
    else:
        break
    points.append(tuple(three_lines))
fictive_id = -101000
print("""\
<?xml version='1.0' encoding='UTF-8'?>
<osm version='0.6' generator='panama-ap'>""")
for point in points:
    name, easting_str, northing_str = point
    easting = float(easting_str[5:])
    northing = float(northing_str[6:])
    latitude, longitude = utm.to_latlon(easting, northing, 17, northern=True)
    if point not in fictive_ids:
        fictive_ids[point] = fictive_id
        print("""\
  <node id='{0}' action='modify' visible='true' lat='{2}' lon='{3}'><tag k='ref:no' v='{1}' /></node>"""
          .format(fictive_id, name, latitude, longitude))
        fictive_id -= 1
print("""  <way id='{0}' action='modify' visible='true'>""".format(fictive_id))
for point in points:
    print("""    <nd ref='{0}' />""".format(fictive_ids[point]))
print("""\
  </way>
</osm>""")
