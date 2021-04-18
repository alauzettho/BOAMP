import glob
import pandas as pd
import xml.etree.ElementTree as ET


# Generate a CSV file containing all id to parse


def checkIfNumberOfItemsLesserThousandInXMLFile(filePath : str) -> bool :
    chec = False
    tree = ET.parse(filePath)
    root = tree.getroot()
    size = len(root.getchildren())
    
    if size > 999 :
        print(size)
    else :
        chec = True

    return chec


def getListOfFilesToMerge(pathFiles : str) -> list :
    print(f"Getting List Of Files \n")
    listFiles = glob.glob(pathFiles)
    print(f"Number of Files : {len(listFiles)} \n")
    return listFiles


def mergeAllFilesIntoSingleFile(listFiles : list, fileOut : str) :
    df_listXml = pd.DataFrame(columns = ['id', 'value', 'schema', 'description'])
    df_listXml = df_listXml.fillna(0)
    for files in listFiles :
        tree = ET.parse(files)
        root = tree.getroot()
        for x in root.findall('item') :
            df_listXml = df_listXml.append(x.attrib, ignore_index = True)
    df_listXml.to_csv(fileOut)


def mainManagement(pathFiles : str, pathOutput : str) :
    listFiles = getListOfFilesToMerge(pathFiles)
    for files in listFiles :
        assert checkIfNumberOfItemsLesserThousandInXMLFile(files) == True
    mergeAllFilesIntoSingleFile(listFiles, pathOutput)



folder = "/home/alauzettho/BOAMP/ScriptsParseDateRegion/resultsTest/*"  # folder to parse
resultXML = "/home/alauzettho/BOAMP/ScriptsParseDateRegion/combinedXML.xml" # backup file containing all dataID


if __name__ == "__main__" :
    # Generate csv containing all values combinedXML
    # Uncomment this to rerun all gathering
    # mainManagement(folder, resultXML)
    print('DONE')