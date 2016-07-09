"""
mortise and tenon generator for rhino3d
"""

import Rhino
import System.Guid
import scriptcontext
import rhinoscriptsyntax as rs
from getsubsurface import GetSubSurface

def main():
  to_delete = []

  rs.ProjectOsnaps(False)

  positive_object = rs.GetObject("select positive object", 16)
  negative_object = rs.GetObject("select negative object", 16)
  rs.HideObject(negative_object)

  polysurface, face = GetSubSurface("select tenon surface")
  to_delete.append(face)

  normal = rs.VectorUnitize(rs.SurfaceNormal(face, (0.5,0.5)))
  plane = rs.PlaneFromNormal(rs.EvaluateSurface(face, 0.5, 0.5), normal)
  rs.ViewCPlane(plane=plane)
  rs.ProjectOsnaps(True)

  tenon_rects = rs.GetObjects(message="select tenon curves", filter=4)

  tenon_faces = []
  for rect in tenon_rects:
    tenon_faces.append(rs.AddPlanarSrf(rect)[0])

  rs.ShowObject(negative_object)

  rs.ProjectOsnaps(False)
  height_pt = rs.GetPoint("enter height point")

  # compule a vector normal to plane of the desired height
  extrude_vec_a = rs.EvaluateSurface(face, 0.5, 0.5)
  dist = rs.DistanceToPlane(plane, height_pt)
  extrude_vec_b = [ dist * el for el in normal]
  extrude_vec_b = rs.VectorAdd(extrude_vec_a, extrude_vec_b)
  extrude_curve = rs.AddCurve((extrude_vec_a, extrude_vec_b))
  to_delete.append(extrude_curve)

  tenons = []
  for tenon_face in tenon_faces:
    tenon = rs.ExtrudeSurface(tenon_face, extrude_curve)
    tenons.append(tenon)

  rs.BooleanUnion([positive_object] + tenons, delete_input=False)
  rs.BooleanDifference([negative_object], tenons, delete_input=False)

  to_delete.append(positive_object)
  to_delete.append(negative_object)

  rs.DeleteObjects(to_delete)
  rs.DeleteObjects(tenon_faces)
  rs.DeleteObjects(tenons)

if __name__ == '__main__':
  main()
