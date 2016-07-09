import Rhino
import System.Guid
import scriptcontext
import rhinoscriptsyntax as rs

def GetSubSurface(prompt="select subsurface"):
  # get a surface of an object
  go=Rhino.Input.Custom.GetObject()
  go.GeometryFilter=Rhino.DocObjects.ObjectType.Surface
  go.SetCommandPrompt(prompt)
  go.Get()
  objref = go.Object(0)
  polysurface = objref.ObjectId
  go.Dispose()

  brep = objref.Face().DuplicateFace(True)
  guid = scriptcontext.doc.Objects.AddBrep(brep)

  if (guid != System.Guid.Empty):
    rc = Rhino.Commands.Result.Success
    scriptcontext.doc.Views.Redraw()
  return polysurface, guid


