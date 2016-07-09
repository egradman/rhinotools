import rhinoscriptsyntax as rs
import getsubsurface
import math

def main():
  rs.AddLayer("laydown")

  while True:
    panel, face = getsubsurface.GetSubSurface("select down face")
    if panel is None or face is None:
      break

    # compute the plane
    normal = rs.VectorUnitize(rs.SurfaceNormal(face, (0.5,0.5)))
    plane = rs.PlaneFromNormal(rs.EvaluateSurface(face, 0.5, 0.5), normal)

    rs.ViewCPlane(plane=plane)
    box = rs.BoundingBox(face, rs.ViewCPlane(), in_world_coords=True)

    proj_coords = [rs.SurfaceClosestPoint(face, coord) + (0,) for coord in box]
    laydown = rs.OrientObject(panel, box[0:3], proj_coords[0:3], flags=1)
    rs.ObjectLayer(laydown, "laydown")

    rs.DeleteObject(face)
    rs.HideObject(panel)

if __name__ == '__main__':
  main()
