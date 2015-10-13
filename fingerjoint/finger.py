import rhinoscriptsyntax as rs
from collections import defaultdict
from collections import Iterable
import Rhino

"""
# notes
- doesn't handle laser curf currently.  to do this, simple scale alternating
  cylinders along the intersection axis

"""

# this dictionary maps a guid to the fingers
# which will be booleansubtracted from it
# in the final step
guid_to_difference = defaultdict(list)

def perform_subtraction():
  # each time make_fingers is run, it fills guid_to_difference
  # with more fingers to subtract.
  # after all the fingers are subtracted at once
  for guid, objs in guid_to_difference.items():
    print guid, len(objs)
    rs.BooleanDifference(guid, objs)

def make_fingers(positive, negative, subdivisions):
  """
  intersect two collections of planes
  subdivide the intersections
  assign each subdivision to a guid from which it will be subtracted
  """

  # this vector is used to indicate axis of the intersection.
  # it needs to be parallel to the intersection
  # (there are other ways of doing this!)
  p0 = rs.GetPoint("select start of intersection")
  p1 = rs.GetPoint("select end of intersection")

  edge = rs.AddLine(p0, p1)
  vector = rs.VectorCreate(p0, p1)

  rs.EnableRedraw(False)

  # this dict maps a pair of planes (ps, ns) to their booleanintersection
  intersections = {}

  for ps in positive:
    for ns in negative:
      intersection = rs.BooleanIntersection(ps, ns, False)
      if intersection is not None:
        intersections[(ps, ns)] = intersection

  # here we construct some very large cylinders aligned with the axis you drew
  origins = []
  cylinders = []
  for i in range(subdivisions+1):
    origin = rs.EvaluateCurve(edge, rs.CurveParameter(edge, i * 1.0/(subdivisions)))
    origins.append(origin)

  rs.DeleteObject(edge)

  for i in range(subdivisions):
    plane = rs.PlaneFromNormal(origins[i], vector)
    circle = rs.AddCircle(plane, 100)
    planar_circle = rs.AddPlanarSrf(circle)

    extrusion_curve = rs.AddLine(origins[i], origins[i+1])
    cylinders.append(rs.ExtrudeSurface(planar_circle, extrusion_curve))

    rs.DeleteObject(circle)
    rs.DeleteObject(planar_circle)
    rs.DeleteObject(extrusion_curve)


  # we perform a boolean intersection between each intersection and
  # the cylinders to construct the fingers
  for key, intersection in intersections.items():
    ps, ns = key

    for i, cylinder in enumerate(cylinders):
      print "intersection", intersection
      print "cylinder", cylinder
      objs = [brep for brep in rs.BooleanIntersection(intersection, cylinder, False) if rs.IsBrep(brep)]
      # assign the resulting fingers to either the positive or negative
      if i % 2 == 0:
        guid_to_difference[ps].extend(objs)
      else:
        guid_to_difference[ns].extend(objs)

  DeleteItemOrList(cylinders)
  DeleteItemOrList(intersections.values())

  rs.EnableRedraw(True)

def DeleteItemOrList(d):
  """
  helper to delete a guid or a list of guids
  """
  if isinstance(d, Iterable):
    for item in d: DeleteItemOrList(item)
  else:
    rs.DeleteObject(d)

if __name__ == '__main__':
  main()
