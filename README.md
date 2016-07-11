# Eric's Useful Rhino3d Tools
## For Makers Who Are Better Programmers Than Carpenters

Hello Internet!

This repository contains some python scripts for Rhino3d that are useful for anyone who works with sheet materials.

The explanations below will only get you so far.  See the playlist below for more detailed demonstrations of how to use these tools.

https://www.youtube.com/playlist?list=PL6vjZyexULrxROMOXeZTPhfKZhv0Ogfqv



### How to use these tools

1. Clone this repository.
1. Open Rhino preferences.  Add aliases to `RunPythonScript` as indicated below.  This will let you run these scripts by name just like executing any other built-in Rhino command.  What you choose to call each alias is up to you.  I've shared the names I use.

### Finger Jointing

Anyone who has a laser cutter knows: you spend a lot of time making boxes.  Fingerjoints are a quick form of joinery often used to make quick boxes.

Like most people, I used http://boxdesigner.connectionlab.org/ by @rahulbot to generate PDFs.  This is still a great tool. But for more complex builds that incorporate additional features you have to import PDF outlines into Rhino, extrude them, and assemble the box.  Then you make your changes and re-flatten the parts for cutting.

This tool improves on this workflow by enabling you to automatically fingerjoint any set of intersecting orthogonal extrusions (or extrusion-like polysurfaces).

In the simplest case, you have two extrusions that intersect at a right angle.  This may be a *L* intersection or a *T* intersection.  The `finger2` script will let you fingerjoint these extrusions with one another.  You're not limited to a pair of orthogonal extrusions.  You can fingerjoint any two orthogonal sets of extrusions.

When prompted, draw a line indicating an edge of intersection between the extrusions.  It doesn't matter which edge you draw; this line designates the length and direction of the finger operation.

The `finger3` script is designed to fingerjoint three mutually orthogonal sets of extrusions.  This is the scenario of making a box.  In this case, you have to draw three such edges, one for each pair of intersecting planes.  The script will hide certain geometry to make it clear which line it wants you to draw.

#### TODO

* allow the user to specify the length of the fingers (currently only supports "number of fingers")
* kerf control
* automatically determine plane of intersection (cross-product)

#### My aliases

```
finger2
!-_RunPythonScript (Y:\cad\rhinopython\fingerjoint\two.py)
```

create fingerjoints between three orthogonal sets of "planar-ish" polysurfaces

```
finger3
!-_RunPythonScript (Y:\cad\rhinopython\fingerjoint\xyz.py)
```

create fingerjoints between three mutually orthogonal sets of "planar-ish" polysurfaces

### Lay parts flat

You've designed a beautiful thing made of variously joineried pieces of sheet goods.  Now you have to lay all those parts down flat so you can laser-cut or path them for your router.

Frankly TDM Solutions has a tool that does this better than I could ever do, but it's just a part of their $1,300 RhinoNest product.  Buy it if you can; use my free Python knockoff if you can't.

This is a quick and easy way to lay down planar surfaces on the TOP construction plane (for laser cutting, pathing, etc).  Click on each part in turn, on the "down" face, which will be rotated and placed face down on the TOP plane.  Each polysurface you click will be hidden as you click on it.  Just hit `<esc>` when you're done and ignore the scary error message (FIXME).  You can `show` your original parts when you're done.

```
lay
!-_RunPythonScript (Y:\cad\rhinopython\laydown.py)
```

### Dogbone

A problem you encounter if you're using a CNC router table.  Your endmill has non-zero radius, which produces an unintended fillet on sharp inner corners.

Better explanation here: http://www.kontraptionist.com/post/45218053861/slotted-construction-its-a-pretty-nice-thing-to

You need relief cuts.  This set of scripts generates my favorite flavor of relief cut, the "dogbone."

```
innerhole
!-_RunPythonScript (Y:\cad\rhinopython\innerhole.py)
```

perform 45° "dogbone" corner modification for inner profiles.  works on closed curves.  If you get funky results, try `flip`ping the curve. FIXME

```
outerhole
!-_RunPythonScript (Y:\cad\rhinopython\outerhole.py)
```

perform 45° "dogbone" corner modification for outer profiles.  works on closed curves.  If you get funky results, try `flip`ping the curve

```
dogbone
!-_RunPythonScript (Y:\cad\rhinopython\dogbone.py)
```

perform 45° "dogbone" corner modification for extrusions.  Requires you to _subselect_ a planar surface (shift-control-alt) click on my setup... ymmv).  If you get funky results, try subselecting the opposite face of the extrusion (FIXME).  Leaves point objects in the original location  of the corner.

### Slotting

Coming soon

### Notes

I have a 1x2' laser cutter and a 4x8' router table.
