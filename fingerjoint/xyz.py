import rhinoscriptsyntax as rs
from collections import defaultdict
from collections import Iterable
import Rhino

"""
# notes
- doesn't handle laser curf currently.  to do this, simple scale alternating
  cylinders along the intersection axis

"""

import finger
reload(finger)

def main():
  # first, select objects in three orthogonal planes
  xs = rs.GetObjects("select X objects", filter=16); # polysurface
  ys = rs.GetObjects("select Y objects", filter=16);
  zs = rs.GetObjects("select Z objects", filter=16);

  subdivisions = rs.GetInteger(message="enter subdivisions (o)", number=5, minimum=2, maximum=None)

  for positive, negative, hidden in ((xs, ys, zs), (xs, zs, ys), (ys, zs, xs)):
    rs.HideObjects(hidden)
    finger.make_fingers(positive, negative, subdivisions)
    rs.ShowObjects(hidden)

  finger.perform_subtraction()

if __name__ == '__main__':
  main()
