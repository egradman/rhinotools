import rhinoscriptsyntax as rs
from collections import defaultdict
from collections import Iterable
import Rhino
import getsubsurface
import math

inner_curves = None
outer_curves = None
curve_coords = None

def main():
  global inner_curves, outer_curves, curve_coords

  # save for later
  orig_hidden_objects = rs.HiddenObjects()

  # we put reference points in the dogbone-ref layer, so create it if it doesn't exist
  rs.AddLayer("dogbone-ref")

  panel, face = getsubsurface.GetSubSurface("select dogbone face")

  diameter = rs.GetReal("enter cutter diameter", number=0.25)
  diameter = diameter*1.1

  rs.EnableRedraw(False)

  # compute the plane
  normal = rs.VectorUnitize(rs.SurfaceNormal(face, (0.5,0.5)))
  plane = rs.PlaneFromNormal(rs.EvaluateSurface(face, 0.5, 0.5), normal)

  rs.ViewCPlane(plane=plane)
  rs.ProjectOsnaps(True)

  outer_curves = rs.DuplicateSurfaceBorder(face, 1)
  inner_curves = rs.DuplicateSurfaceBorder(face, 2)

  # make a dict mapping each curve to the coords in that curve
  curve_coords = dict()
  for curve in outer_curves + inner_curves:
    coords = rs.CurvePoints(curve)[:-1]
    curve_coords[curve] = coords

  # make a dict mapping each curve to the z component of its cross product at each index
  curve_cross_zs = dict()
  for curve, coords in curve_coords.items():
    proj_coords = [rs.SurfaceClosestPoint(face, coord) for coord in coords]
    cross_zs = []
    for idx in range(len(proj_coords)):
      triplet = [
        proj_coords[(idx+1)%len(proj_coords)],
        proj_coords[idx                ],
        proj_coords[(idx-1)%len(proj_coords)]
      ]

      v0 = (triplet[1][0]-triplet[0][0], triplet[1][1]-triplet[0][1], 0)
      v1 = (triplet[2][0]-triplet[1][0], triplet[2][1]-triplet[1][1], 0)
      cross_z = rs.VectorCrossProduct(v0, v1)[2]
      cross_zs.append(cross_z)
    curve_cross_zs[curve] = cross_zs

  points = []
  bones = []
  temp_points = []
  rs.EnableRedraw(True)
  while True:
    coord = rs.GetPoint("select corner")
    if coord is None:
      break
    try:
      curve, idx = get_curve_and_idx_for_coord(coord)
      point = rs.AddPoint(coord)
      rs.ObjectColor(point, (255, 0, 0))
      temp_points.append(point)
      bones.append((curve, idx))
    except ValueError:
      print "invalid curve point"
      continue
  rs.EnableRedraw(False)
  rs.DeleteObjects(temp_points)

  # try to automatically identify dogbone points if user selected none
  if len(bones) == 0:
    for curve, coords in curve_coords.items():
      proj_coords = [rs.SurfaceClosestPoint(face, coord) for coord in coords]
      for idx in range(len(proj_coords)):
        triplet = [
          proj_coords[(idx+1)%len(proj_coords)],
          proj_coords[idx                ],
          proj_coords[(idx-1)%len(proj_coords)]
        ]
        if curve_cross_zs[curve][idx] > 0:
          bones.append((curve, idx))

  # make the bones
  extrusions = []
  for bone in bones:
    curve, idx = bone

    coords = curve_coords[curve]

    point = rs.AddPoint(coords[idx])
    rs.ObjectLayer(point, "dogbone-ref")

    triplet = [
      coords[(idx+1)%len(coords)],
      coords[idx                ],
      coords[(idx-1)%len(coords)],
    ]

    angle = rs.Angle2(
        (triplet[1], triplet[0]),
        (triplet[1], triplet[2]),
    )
    angle = angle[0]

    # This is a hacky method to determine the handedness of the curve
    # the cross product SHOULD have worked here, but for some reason
    # it did not.
    v0 = triplet[2][0]-triplet[1][0], triplet[2][1]-triplet[1][1], 0
    v1 = triplet[1][0]-triplet[0][0], triplet[1][1]-triplet[0][1], 0
    _angle = math.degrees(math.atan2(v0[1], v0[0]) - math.atan2(v1[1], v1[0]))
    while _angle > 180: _angle -= 360
    while _angle < -180: _angle += 360
    if math.copysign(1, angle) != math.copysign(1, _angle):
      angle -= 180

    point = rs.VectorAdd(
      triplet[1], 
      rs.VectorRotate(0.5*diameter*rs.VectorUnitize(rs.VectorSubtract(triplet[2], triplet[1])), angle/2, (0,0,1))
    )

    circle = rs.AddCircle((point.X, point.Y, -10), diameter/2.0)
    circle_srf = rs.AddPlanarSrf(circle)
    p0 = (point.X, point.Y, -10)
    p1 = (point.X, point.Y,  10)
    line = rs.AddLine(p0, p1)

    extrusion = rs.ExtrudeSurface(circle_srf, line)
    extrusions.append(extrusion)
    rs.DeleteObjects([circle, circle_srf, line])

  rs.BooleanDifference([panel], extrusions, delete_input=True)

  rs.DeleteObject(panel)
  rs.DeleteObjects(extrusions)
  rs.DeleteObjects(points)
  rs.DeleteObjects(inner_curves)
  rs.DeleteObjects(outer_curves)
  rs.DeleteObject(face)
  rs.ShowObject(rs.AllObjects())
  rs.HideObjects(orig_hidden_objects)

  rs.EnableRedraw(True)

def get_curve_and_idx_for_coord(coord):
  coord = round(coord[0],4), round(coord[1],4)
  for curve, coords in curve_coords.items():
    coords = [(round(c.X,4), round(c.Y,4)) for c in coords]
    #for c in coords: print coord, c
    if coord in coords:
      return curve, coords.index(coord)
  raise ValueError

if __name__ == '__main__':
  main()
