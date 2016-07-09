import rhinoscriptsyntax as rs
from collections import defaultdict
from collections import Iterable
import Rhino

def faces():
  surfaces = rs.GetObjects("select surfaces", filter=rs.filter.surface)
  
  points = [rs.EvaluateSurface(surface, *rs.SurfaceParameter(surface, (0.5, 0.5))) for surface in surfaces]
  x = reduce(lambda s, point: s+point.X, points, 0) / len(points)
  y = reduce(lambda s, point: s+point.Y, points, 0) / len(points)
  z = reduce(lambda s, point: s+point.Z, points, 0) / len(points)

  # find the center of the object
  mass_center = rs.AddPoint(x,y,z)

  extrude_curves = {}
  # find the appropriate extrusion curve with the lowest dot product
  for surface in surfaces:
    surface_center = rs.EvaluateSurface(surface, *rs.SurfaceParameter(surface, (0.5, 0.5)))
    center_vector = rs.VectorCreate(surface_center, mass_center)

    normals = []
    normals.append(rs.SurfaceNormal(surface, rs.SurfaceParameter(surface, (0.5, 0.5))))
    normals.append(-rs.SurfaceNormal(surface, rs.SurfaceParameter(surface, (0.5, 0.5))))

    if (rs.VectorDotProduct(normals[0], center_vector) < rs.VectorDotProduct(normals[1], center_vector)):
      extrude_curve = normals[0]
    else:
      extrude_curve = normals[1]
    extrude_curve = rs.VectorUnitize(extrude_curve)
    extrude_curve = rs.VectorScale(extrude_curve, 0.25)
    extrude_curve = [surface_center, rs.VectorAdd(surface_center, extrude_curve)]
    extrude_curve = rs.AddCurve(extrude_curve)
    
    rs.ExtrudeSurface(surface, extrude_curve)
    rs.DeleteObject(extrude_curve)
    rs.DeleteObject(surface)

  rs.DeleteObject(mass_center)








if __name__=='__main__':
  faces()

#"""
## notes
#- doesn't handle laser curf currently.  to do this, simple scale alternating
#  cylinders along the intersection axis
#
#"""
#
## this dictionary maps a guid to the fingers
## which will be booleansubtracted from it
## in the final step
#guid_to_difference = defaultdict(list)
#
#def perform_subtraction():
#  # each time make_fingers is run, it fills guid_to_difference
#  # with more fingers to subtract.
#  # after all the fingers are subtracted at once
#  for guid, objs in guid_to_difference.items():
#    print guid, len(objs)
#    rs.BooleanDifference(guid, objs)
#
#def make_fingers(positive, negative, subdivisions):
#  """
#  intersect two collections of planes
#  subdivide the intersections
#  assign each subdivision to a guid from which it will be subtracted
#  """
#
#  # this vector is used to indicate axis of the intersection.
#  # it needs to be parallel to the intersection
#  # (there are other ways of doing this!)
#  p0 = rs.GetPoint("select start of intersection")
#  p1 = rs.GetPoint("select end of intersection")
#
#  edge = rs.AddLine(p0, p1)
#  vector = rs.VectorCreate(p0, p1)
#
#  rs.EnableRedraw(False)
#
#  # this dict maps a pair of planes (ps, ns) to their booleanintersection
#  intersections = {}
#
#  for ps in positive:
#    for ns in negative:
#      intersection = rs.BooleanIntersection(ps, ns, False)
#      intersections[(ps, ns)] = intersection
#
#  # here we construct some very large cylinders aligned with the axis you drew
#  origins = []
#  cylinders = []
#  for i in range(subdivisions+1):
#    origin = rs.EvaluateCurve(edge, rs.CurveParameter(edge, i * 1.0/(subdivisions)))
#    origins.append(origin)
#
#  rs.DeleteObject(edge)
#
#  for i in range(subdivisions):
#    plane = rs.PlaneFromNormal(origins[i], vector)
#    circle = rs.AddCircle(plane, 100)
#    planar_circle = rs.AddPlanarSrf(circle)
#
#    extrusion_curve = rs.AddLine(origins[i], origins[i+1])
#    cylinders.append(rs.ExtrudeSurface(planar_circle, extrusion_curve))
#
#    rs.DeleteObject(circle)
#    rs.DeleteObject(planar_circle)
#    rs.DeleteObject(extrusion_curve)
#
#
#  # we perform a boolean intersection between each intersection and
#  # the cylinders to construct the fingers
#  for key, intersection in intersections.items():
#    ps, ns = key
#
#    for i, cylinder in enumerate(cylinders):
#      print "intersection", intersection
#      print "cylinder", cylinder
#      objs = [brep for brep in rs.BooleanIntersection(intersection, cylinder, False) if rs.IsBrep(brep)]
#      # assign the resulting fingers to either the positive or negative
#      if i % 2 == 0:
#        guid_to_difference[ps].extend(objs)
#      else:
#        guid_to_difference[ns].extend(objs)
#
#  DeleteItemOrList(cylinders)
#  DeleteItemOrList(intersections.values())
#
#  rs.EnableRedraw(True)
#
#def DeleteItemOrList(d):
#  """
#  helper to delete a guid or a list of guids
#  """
#  if isinstance(d, Iterable):
#    for item in d: DeleteItemOrList(item)
#  else:
#    rs.DeleteObject(d)
#
#if __name__ == '__main__':
#  main()
