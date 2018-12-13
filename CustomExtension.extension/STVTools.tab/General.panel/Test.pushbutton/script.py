from pyrevit.framework import List
from pyrevit import revit, DB
import clr, sys, re, os, imp
clr.AddReference('RevitAPI')
clr.AddReference('RevitAPIUI')
clr.AddReference("System")
from Autodesk.Revit.DB import FilteredElementCollector, Structure
from Autodesk.Revit.DB import BuiltInCategory, ElementId, XYZ, Point, Transform, Transaction,FamilySymbol
from System.Collections.Generic import List
from Autodesk.Revit.UI import *
from Autodesk.Revit.DB import *
from Autodesk.Revit.Creation import *
from pyrevit import script
from pyrevit import forms
import pyrevit
clr. AddReferenceByPartialName('PresentationCore')
clr.AddReferenceByPartialName('PresentationFramework')
clr.AddReferenceByPartialName('System.Windows.Forms')
uidoc = __revit__.ActiveUIDocument
doc = __revit__.ActiveUIDocument.Document

archive = '\\\\stvgroup.stvinc.com\\v3\\DGPA\\Vol3\\Projects\\3019262\\3019262_0001\\' \
          '90_CAD Models and Sheets\\17017000\\_PIM\\PointData\\Archive\\'
root, dirs, files = os.walk(archive).next()
print root
print dirs
print files