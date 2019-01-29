from pyrevit.framework import List
from pyrevit import revit, DB, forms
from openpyxl import load_workbook
import clr
import csv
import os
import EwrQcUtils
import xlsxwriter
clr.AddReference('RevitAPI')
clr.AddReference("System")
from Autodesk.Revit.DB import FilteredElementCollector, Transaction, ImportInstance, \
	OpenOptions,WorksetConfiguration, WorksetConfigurationOption, DetachFromCentralOption,\
    ModelPathUtils, SaveAsOptions, WorksharingSaveAsOptions
from System.Collections.Generic import List
from Autodesk.Revit.UI.Events import DialogBoxShowingEventArgs
from Autodesk.Revit.UI import UIApplication
from Autodesk.Revit.ApplicationServices import Application
clr. AddReferenceByPartialName('PresentationCore')
clr.AddReferenceByPartialName('PresentationFramework')
clr.AddReferenceByPartialName('System.Windows.Forms')
clr.AddReference('RevitAPIUI')
# Collect Save location and Rvt Files
collectorFiles = forms.pick_file(file_ext='rvt', multi_file=True, unc_paths=False)
destinationFolder = forms.pick_folder(title='SaveTo.....')

def RVTFileCollector(dir):
    files = []
    for file in os.listdir(dir):
        if file.endswith(".rvt"):
            #print(str(file))
            files.append(str(file))
    print files
    return files

def OpenFiles(oFile, app, audit):

    openOpt = OpenOptions()
    if audit == True:
        openOpt.Audit = True
    else:
        openOpt.Audit = False
    openOpt.DetachFromCentralOption = DetachFromCentralOption.DetachAndPreserveWorksets
    wsopt = WorksetConfiguration(WorksetConfigurationOption.CloseAllWorksets)
    # wsopt.Open(worksetList)
    openOpt.SetOpenWorksetsConfiguration(wsopt)
    modelPath = ModelPathUtils.ConvertUserVisiblePathToModelPath(oFile)
    currentdoc = app.OpenDocumentFile(modelPath, openOpt)
    try:
        DialogBoxShowingEventArgs.OverrideResult(1)
    except:
        pass
    print(str(doc) +' Opened')
    return currentdoc


# Main
uidoc = __revit__.ActiveUIDocument
doc = __revit__.ActiveUIDocument.Document

__doc__ = 'Open projects and resave in a specific location'\
            'Please do not use lightly'
uiapp = UIApplication(doc.Application)
application = uiapp.Application

# Transaction
if len(collectorFiles) > 0:
    t = Transaction(doc, 'Check QAQC Elements')
    t.Start()
    for aDoc in collectorFiles:
        openedDoc = OpenFiles(aDoc, application, audit = False)
        workshareOp = WorksharingSaveAsOptions()
        # Define the name and location of excel file
        fileName = destinationFolder +'\\' + openedDoc.Title + '.xlsx'
        # Define and Open Excel File
        excelFile = EwrQcUtils.ExcelOpener(fileName)
        # TODO: Create Text Tab
        # TODO: Titleblock Tab
        # TODO: Survey Point Tab
        # TODO: BasePoint Tab
        # TODO: Site Shared Point Tab
        # TODO: Categories in Workset Tab
        # TODO: Family Tab
        # TODO: Workset Tab
        # TODO: Links Tab
        # TODO: Sheetstab, Viewstab
        # TODO: Dimentions Tab
        collectorLevels = EwrQcUtils.LevelCheck(openedDoc)
        EwrQcUtils.ExcelWriter(excelFile, 'LEVEL', 1, 0, collectorLevels)
        collectorSheetElements = EwrQcUtils.SheetElementCheck(openedDoc)
        EwrQcUtils.ExcelWriter(excelFile, 'SHEET ELEMENT', 1, 0, collectorSheetElements)
        collectorLines = EwrQcUtils.LineCheck(openedDoc)
        EwrQcUtils.ExcelWriter(excelFile, 'LINES', 1, 0, collectorLines)
        # Close Excel and Revit File
        excelFile.close()
        openedDoc.Close(False)
        print('File Saved' + fileName)
    wb = load_workbook('C:\\Users\\loum\\Desktop\\QAQC Excel\\N17017000-3D_CENTRAL.xlsx')
    # EwrQaUtils.FormattingLine(wb['LINE'])
    t.Commit()

else:
    forms.alert('No File is selected', title='', sub_msg=None, expanded=None, footer='', ok=True, cancel=False, yes=False,
                        no=False, retry=False, warn_icon=True, options=None, exitscript=False)