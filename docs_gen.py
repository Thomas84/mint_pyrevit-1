import os
import shutil

def GetDescription(path):
    des = "\n Description: "
    truePath = path + "\\script.py"


path = 'W:\Tools\Repo\pyRevit_custom_Mint\CustomExtension.extension\\Nerv.tab'
docPath = 'W:\\Tools\\Repo\pyRevit_custom_Mint\\docs\\nerv'

index = "\n\
===========================\n\
\n\
Description\n\
\n\
.. toctree::\n\
   :maxdepth: 1\n\
   :name: "

buttonTemplate = "\n\
*********************\n\
\n\
.. figure:: {0}\n\
   :align: left\n\
\n\
   "

masterFileAdd = open("W:\Tools\Repo\pyRevit_custom_Mint\docs\index.rst", "a+")
masterFileRead = open("W:\Tools\Repo\pyRevit_custom_Mint\docs\index.rst", "r").read()
# print(masterFileRead)
for i, j, y in os.walk(path):
    if i[-5:] == 'panel':
        # sprint(j)
        dir = os.path.join(docPath, os.path.basename(i[:-6]).replace(' ', '_').lower())
        # print(dir)

        # Make directory of a panel and create an index file
        if not os.path.exists(dir):
            os.mkdir(dir)
        if not os.path.exists(dir + "\\_static"):
            os.mkdir(dir + "\\_static")
        if not os.path.isfile(dir + "\\index.rst"):
            f = open(dir + "\\index.rst", "w")
            f.write(os.path.basename(i[:-6]).replace(' ', '_').lower() + index + 'toc-' + os.path.basename(i[:-6]).replace(' ', '_').lower() + "\n")
            f.close()

        else:
            # print(os.path.basename(i[:-6]).replace(' ', '_').lower() + " panel index already exists")
            pass

        # Make the directory of a panel in mater index file
        pathText = "nerv/{0}/index.rst".format(os.path.basename(i[:-6]).replace(' ', '_').lower())
        if not pathText in str(masterFileRead):
            masterFileAdd.write("\n    " + pathText)
            # print("Path " + pathText + "added in Master index")
        else:
            # print("Path " + pathText + " already exists in Master index")
            pass

        # make pushbutton .rst for each push button
        for item in j:
            # Create .rst for pushbutton
            if ".pushbutton" in item:
                if not os.path.isfile(dir + "\\" + item[:-11] + ".rst"):
                    imageDis = dir + "\\" + "_static" + "\\" + item[:-11].replace(' ', '_').lower() + ".png"
                    shutil.copy(i + '\\' + item + "\\" + "icon.png", imageDis)
                    pushButtonFile = open(dir + "\\" + item[:-11].replace(' ', '_').lower() + ".rst", "w")
                    pushButtonFile.write(item[:-11] + buttonTemplate.format("_static" + "/" + item[:-11].replace(' ', '_').lower() + ".png") + item[:-11].replace(' ', '_').lower())
                    pushButtonFile.close()
                    panelIndex = open(dir + "\\index.rst", "a+")
                    panelIndexRead = open(dir + "\\index.rst", "r").read()
                    if not item[:-11].replace(' ', '_').lower() in panelIndexRead:
                        panelIndex.write("\n   " + item[:-11].replace(' ', '_').lower())
            else:
                # Create Sub-index files
                subName = item.split(".")[0].replace(' ', '_').lower()
                if not os.path.exists(dir + "\\" + subName):
                    os.mkdir(dir + "\\" + subName)
                if not os.path.exists(dir + "\\" + subName + "\\_static"):
                    os.mkdir(dir + "\\" + subName + "\\_static")
                if not os.path.isfile(dir + subName + "\\index.rst"):
                    f = open(dir + '\\' + subName + "\\index.rst", "w")
                    f.write(subName.replace(' ', '_').lower() + index + 'toc-' + subName.replace(' ', '_').lower() + "\n")
                    f.close()
                    subPanelIndex = open(dir + "\\index.rst", "a+")
                    subPanelIndexRead = open(dir + "\\index.rst", "r").read()
                    if not subName.replace(' ', '_').lower() + '/' + "index.rst" in subPanelIndexRead:
                        subPanelIndex.write("\n   " + subName.replace(' ', '_').lower() + '/' + "index.rst")

                    if not "stack" in item.lower() and not "smartbutton" in item.lower():
                        # print(i + '\\'+ item)
                        for aa, bb, cc in os.walk(i + '\\' + item):
                            if bb:
                                for subButton in bb:
                                    imageDis = dir + '\\' + subName + "\\" + "_static" + "\\" + subButton.split(".")[0].replace(' ',
                                                                                                  '_').lower() + ".png"
                                    try :
                                        shutil.copy(i + '\\' + item + "\\" + subButton + "\\"+ "icon.png", imageDis)
                                    except:
                                        shutil.copy(i + '\\' + item  + "\\" + "icon.png", imageDis)
                                    if not os.path.isfile(dir + '\\' + subName + "\\" + subButton.split(".")[0].replace(' ', '_').lower() + ".rst"):
                                        subPushButtonFile = open(dir + '\\' + subName + "\\" + subButton.split(".")[0].replace(' ', '_').lower() + ".rst", "w")
                                        subPushButtonFile.write(subButton.split(".")[0] + buttonTemplate.format(
                                            "_static" + "/" + subButton.split(".")[0].replace(' ', '_').lower() + ".png") + subButton.split(".")[0].replace(
                                            ' ', '_').lower())
                                        subPushButtonFile.close()
                                        subPanelIndex = open(dir + '\\' + subName + "\\index.rst", "a+")
                                        subPanelIndexRead = open(dir + '\\' + subName + "\\index.rst", "r").read()
                                        if not subButton.split(".")[0].replace(' ', '_').lower() in subPanelIndexRead:
                                            subPanelIndex.write("\n   " + subButton.split(".")[0].replace(' ', '_').lower())

                                # dir = os.path.join(docPath, os.path.basename(i[:-6]).replace(' ', '_').lower())
                                # print(dir)
                #else:
                    #if not os.path.exists(dir + "\\" + subName + ):
                        #os.mkdir(dir + "\\" + subName)




