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
  positive = rs.GetObjects("select plane 1 objects", filter=16) # polysurface
  negative = rs.GetObjects("select plane 2 objects", filter=16)

  subdivisions = rs.GetInteger(message="enter subdivisions (odd)", number=5, minimum=2, maximum=None)
  finger.make_fingers(positive, negative, subdivisions)

  finger.perform_subtraction()

if __name__ == '__main__':
  main()
