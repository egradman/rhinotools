import rhinoscriptsyntax as rs
from collections import defaultdict
from collections import Iterable
import Rhino

def main():

  diameter = rs.GetReal("enter cutter diameter", number=0.25)
  diameter = diameter*1.1
  # first, select objects in three orthogonal planes
  obj = rs.GetObject("select object", filter=4) # curve
  curve_points = rs.CurvePoints(obj)[:-1]

  circles = []
  while True:
    point = rs.GetPoint("select point")
    if point is None:
      break
    try:
      idx = curve_points.index(point)
      print "clicked index", idx
    except ValueError:
      print "invalid point"
      continue

    points = [
      curve_points[(idx+1)%len(curve_points)],
      curve_points[idx                      ],
      curve_points[(idx-1)%len(curve_points)],
    ]
    print points

    angle = rs.Angle2(
        (points[1], points[0]),
        (points[1], points[2]),
    )
    angle = angle[0]

    point = rs.VectorAdd(
      points[1], 
      rs.VectorRotate(0.5*diameter*rs.VectorUnitize(rs.VectorSubtract(points[2], points[1])), angle/2, (0,0,1))
    )

    #p0 = (point.X, point.Y, point.Z + 1000)
    #p1 = (point.X, point.Y, point.Z - 1000)

    circle = rs.AddCircle(point, diameter/2.0)
    circles.append(circle)

    #extrusion = rs.ExtrudeCurveStraight(circle, p0, p1)

  for circle in circles:
    before_obj = obj
    obj = rs.CurveBooleanDifference(obj, circle)
    rs.DeleteObject(before_obj)

  rs.DeleteObjects(circles)
  #rs.DeleteObject(obj)



if __name__ == '__main__':
  main()
