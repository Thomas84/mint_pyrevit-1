
import sys, clr
import ConfigParser
from os.path import expanduser


import System, Selection
from Autodesk.Revit.DB import Document, Transaction, XYZ
clr. AddReferenceByPartialName('PresentationCore')
clr.AddReferenceByPartialName('PresentationFramework')
clr.AddReferenceByPartialName('System.Windows.Forms')
uidoc = __revit__.ActiveUIDocument
doc = __revit__.ActiveUIDocument.Document

__doc__ = 'Align text notes to right.'

selection = Selection.get_selected_elements(doc)
t = Transaction(doc, 'Rid Leader')
t.Start()
if selection:
	for i in selection:
		i.HasLeader = False
t.Commit()

selection = Selection.get_selected_elements(doc)
t = Transaction(doc, 'Align Max')
t.Start()
if selection:
	max = selection[0].get_BoundingBox(doc.ActiveView).Max
	location = max.X
	for i in selection:
		eleMin = i.get_BoundingBox(doc.ActiveView).Max.X
		distance = location - eleMin
		i.Location.Move(XYZ(distance, 0 , 0))
t.Commit()

selection = Selection.get_selected_elements(doc)
t = Transaction(doc, 'Enable Leader')
t.Start()
if selection:
	for i in selection:
		i.HasLeader = True
t.Commit()

