# -*- coding: UTF-8 -*-
"""print all clashes.

Lists all linked and imported DWG instances with worksets and creator.

Copyright (c) 2018 Martin Lou

--------------------------------------------------------

"""
from pyrevit.framework import List
from pyrevit import revit, DB
import clr, pprint,os
from collections import defaultdict
import re, sys
from pyrevit import revit, DB
from pyrevit import script
from pyrevit import forms
clr.AddReference('RevitAPI')
clr.AddReference('RevitAPIUI')
clr.AddReference("System")
from Autodesk.Revit.DB import FilteredElementCollector, Structure, DeleteElements
from Autodesk.Revit.DB import BuiltInCategory, ElementId, XYZ, Point, Transform, Transaction,FamilySymbol
from System.Collections.Generic import List
from Autodesk.Revit.UI import *
from Autodesk.Revit.DB import *
from Autodesk.Revit.Creation import *
clr. AddReferenceByPartialName('PresentationCore')
clr.AddReferenceByPartialName('PresentationFramework')
clr.AddReferenceByPartialName('System.Windows.Forms')
uidoc = __revit__.ActiveUIDocument
doc = __revit__.ActiveUIDocument.Document


__title__ = 'Declash screen'
__author__ = 'Martin Lou'
__contact__ = 'mengfan.lou@stvinc.com'


__doc__ = 'Select the shared point of the model '\
          'This is helpful check project info'


# input ---------------------

# Get the right point data from the right direcory
fName = doc.Title
modelRegex = re.compile(r'\w\d\d\d\d\d\d\d\d-\S\S_CENTRAL')
modelRegex2 = re.compile(r'\w\d\d\d\d\d\d\d\d-\S\S_CENTRAL_\w?\w?\w')
approvedTail = ['ENC', 'FFE', 'GEN', 'INT', 'SSM', 'C', 'CP', 'PBB', ]
noTail = modelRegex.findall(fName)
tail = modelRegex2.findall(fName)
if len(tail) == 0:
    sys.path.append('\\\\stvgroup.stvinc.com\\v3\\DGPA\\Vol3\\Projects\\3019262\\3019262_0001\\'
                    '90_CAD Models and Sheets\\17017000\\_PIM\\PointData\\' + fName[0: 20])
    print('\\\\stvgroup.stvinc.com\\v3\\DGPA\\Vol3\\Projects\\3019262\\3019262_0001\\'
        '90_CAD Models and Sheets\\17017000\\_PIM\\PointData\\' + fName[0: 20])
else:
    nameLst = re.split('_', fName)
    if nameLst[2] in approvedTail:
        sys.path.append('\\\\stvgroup.stvinc.com\\v3\\DGPA\\Vol3\\Projects\\3019262\\3019262_0001\\'
                        '90_CAD Models and Sheets\\17017000\\_PIM\\PointData\\' + tail[0])
        print('\\\\stvgroup.stvinc.com\\v3\\DGPA\\Vol3\\Projects\\3019262\\3019262_0001\\'
                '90_CAD Models and Sheets\\17017000\\_PIM\\PointData\\' + tail[0])
    else:
        sys.path.append('\\\\stvgroup.stvinc.com\\v3\\DGPA\\Vol3\\Projects\\3019262\\3019262_0001\\'
                        '90_CAD Models and Sheets\\17017000\\_PIM\\PointData\\' + fName[0: 20])
# Be sure to import the right one as in all point data files are named the same.
import Pointdata


__doc__ = 'Select the shared point of the model '\
          'This is helpful check project info'


# input ---------------------

ew = doc.ActiveProjectLocation.GetProjectPosition(XYZ(0,0,0)).EastWest * float(-1.0)
ns = doc.ActiveProjectLocation.GetProjectPosition(XYZ(0,0,0)).NorthSouth * float(-1.0)
elevation = doc.ActiveProjectLocation.GetProjectPosition(XYZ(0,0,0)).Elevation * float(-1.0)
angle = doc.ActiveProjectLocation.GetProjectPosition(XYZ(0,0,0)).Angle  * float(-1.0)
rotationTransform = Transform.CreateRotation(XYZ.BasisZ, angle)
translationVector = XYZ(ew,ns,elevation)
translationTransform = Transform.CreateTranslation(translationVector)
finalTransform = translationTransform.Multiply(rotationTransform)
count = 0
outLst = []
# Just to be sure how many points will be created and each list are the same length
print(len(Pointdata.pointX))
print(len(Pointdata.pointY))
print(len(Pointdata.pointZ))


# Transaction Start
t = Transaction(doc, 'Add CLash Points')

# Clash point Calculation
FSymbol = DB.FilteredElementCollector(doc) \
    .OfClass(clr.GetClrType(FamilySymbol)) \
    .ToElements()

clashPoint = ()
for i in FSymbol:
    if i.Family.Name == 'Site-Generic-Clashpoint':
        clashPoint = i
if not clashPoint:
    print('Please Load the Clash Point Family')
else:
    t.Start()
    print(clashPoint.Family.Name)
    print(clashPoint)
    count = 0
    elements = []
    for el in Pointdata.pointX:
        x = float(Pointdata.pointX[count]) + ew
        y = float(Pointdata.pointY[count]) + ns
        z = float(Pointdata.pointZ[count]) + elevation
        clashName = str('No. ' + str(count + 1) + ' ID: ' + Pointdata.clashName[count])
        clashwithID = str(Pointdata.otherFile[count] + ' ID: ' + Pointdata.clashwithID[count])
        pnt = XYZ(x,y,z)
        bPnt = Transform.CreateRotation(XYZ.BasisZ, angle).OfPoint(pnt)
        print(bPnt)

        # Clash point creation
        boxes = doc.Create.NewFamilyInstance(bPnt, clashPoint, Structure.StructuralType.NonStructural)
        elements.append(boxes)

        boxes.LookupParameter('Clash Name').Set(clashName)
        boxes.LookupParameter('Clash with ID').Set(clashwithID)
        count += 1
    t.Commit()

    selSet = []

    for el in elements:
        selSet.append(el.Id)


    revit.get_selection().set_to(selSet)


output = script.get_output()
def listclashes(current_view_only=False):
    dwgs = DB.FilteredElementCollector(revit.doc)\
             .OfClass(DB.ImportInstance)\
             .WhereElementIsNotElementType()\
             .ToElements()

    dwgInst = defaultdict(list)
    workset_table = revit.doc.GetWorksetTable()

    output.print_md("## LINKED AND IMPORTED DWG FILES:")
    output.print_md('By: [{}]({})'.format(__author__, __contact__))

    for dwg in dwgs:
        if dwg.IsLinked:
            dwgInst["LINKED DWGs:"].append(dwg)
        else:
            dwgInst["IMPORTED DWGs:"].append(dwg)

    for link_mode in dwgInst:
        output.print_md("####{}".format(link_mode))
        for dwg in dwgInst[link_mode]:
            dwg_id = dwg.Id
            dwg_name = dwg.LookupParameter("Name").AsString()
            dwg_workset = workset_table.GetWorkset(dwg.WorksetId).Name
            dwg_instance_creator = \
                DB.WorksharingUtils.GetWorksharingTooltipInfo(revit.doc,
                                                              dwg.Id).Creator

            if current_view_only \
                    and revit.activeview.Id != dwg.OwnerViewId:
                continue

            print('\n\n')
            output.print_md("**DWG name:** {}\n\n"
                            "- DWG created by:{}\n\n"
                            "- DWG id: {}\n\n"
                            "- DWG workset: {}\n\n"
                            .format(dwg_name,
                                    dwg_instance_creator,
                                    output.linkify(dwg_id),
                                    dwg_workset))


selected_option = \
    forms.CommandSwitchWindow.show(
        ['In Current View',
         'In Model'],
        message='Select search option:'
        )

if selected_option:
    listdwgs(current_view_only=selected_option == 'In Current View')