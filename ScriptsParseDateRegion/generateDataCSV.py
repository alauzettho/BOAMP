import os
import time
import subprocess
import numpy as np
import pandas as pd
import pandas_read_xml as pdx


# Import all XML files and write them in a csv file


def generateCleanDfID(xmlPath) -> pd.DataFrame :
    df_xml = pd.read_csv(xmlPath)
    df_xml = df_xml.loc[:,~df_xml.columns.str.match("Unnamed")]
    df_xml = df_xml.reset_index().set_index('value')
    df_xml = df_xml.drop(index = None, columns = ['id', 'index'])
    df_xml = df_xml.dropna()
    df_xml = df_xml.replace(to_replace=r'http://schemas.journal-officiel.gouv.fr/schemabook/boamp/Boamp_v010.xsd', value = 'v010', regex = True)
    df_xml = df_xml.replace(to_replace=r'http://schemas.journal-officiel.gouv.fr/schemabook/boamp/Boamp_v110.xsd', value = 'v110', regex = True)
    df_xml = df_xml.replace(to_replace=r'http://schemas.journal-officiel.gouv.fr/schemabook/boamp/Boamp_v230.xsd', value = 'v230', regex = True)
    df_xml = df_xml[df_xml.schema == 'v230']
    return df_xml


def generateFile(id : str, curlOut : str) -> str :
    # Use curl to generate a file containing the XML
    print(id)
    fileOut = curlOut
    idString = "{}' > ".format(id)
    mainString = "curl -X GET --header 'Accept: application/xml' 'http://api.dila.fr/opendata/api-boamp/annonces/v230/" + idString + fileOut
    p = subprocess.Popen(mainString, shell=True)
    p.communicate()
    return mainString


def cleanOneRow(df_row : pd.DataFrame) -> pd.DataFrame :
    # Clean a row only dataframe
    listKeys = df_row.keys()
    df_Collect = pd.DataFrame()

    for i in listKeys :
        if i != "ANNONCE|GESTION|NOM_HTML" :
            normalizedSlice = pd.json_normalize(df_row[i])

        df_Collect = pd.concat([df_Collect, normalizedSlice], axis = 1)

    df_Collect = df_Collect.replace(to_replace=r'http://www.w3.org/2001/XMLSchema-instance', value = np.nan, regex = True)
    df_Collect = df_Collect.loc[:,~df_Collect.columns.duplicated()]
    return(df_Collect.dropna(axis = 1))


def generatOneRow(filePath : str) -> pd.DataFrame :
    # Create a dataframe from a xml file
    df_singleRowXml = pdx.read_xml(filePath)
    df_singleRowXml = pdx.auto_flatten(df_singleRowXml).dropna(axis = 1)
    df_singleRowXml = cleanOneRow(df_singleRowXml)
    return df_singleRowXml


def mergeXmlIntoDataframe(listID : list, curlOut : str) -> pd.DataFrame :
    # Generate the XML from a list of ID
    # Merge the above XML into a df
    # Export df into a csv 
    df_all_xml = pd.DataFrame()

    for i in listID :

        max_runs = 3
        run = 0
        while run < max_runs :
            try :
                generateFile(str(i), curlOut)
                tempDf = generatOneRow(curlOut)
                df_all_xml = df_all_xml.append(tempDf)
            except :
                continue
            else:
                break
            finally :
                run += 1

        print("----------------------------------------------------------------------------")
        # df_all_xml.to_csv(finalCSV)

    return df_all_xml


def createListOfFilesToParse(df_xml : pd.DataFrame) -> list :
    # Parse the csv file containing all XML ID and generate the list of ID
    output = df_xml.reset_index()['value'].to_list()

    # output = output[0:70] #TODO
    return output


def cleanDataframe(df_data : pd.DataFrame) -> pd.DataFrame :
    #TODO
    # print(df_data.keys())
    return df_data


def main() -> int :
    resultXML = "/home/alauzettho/BOAMP/ScriptsParseDateRegion/combinedXML.xml"     # file containing all raw XML ID
    finalCSV  = "/home/alauzettho/BOAMP/ScriptsParseDateRegion/dataAquitaine_0.csv"   # file containing all clean data
    tempFile  = "curl_api_output.xml"   # temp file that contains the request of the curl request, if code crash => the file is the source of the problem

    # Generate df from XML file and clean it
    df_xml = generateCleanDfID(resultXML)

    # Generate list of files to parse
    all_list = createListOfFilesToParse(df_xml)
    print("----------------------------------------------------------------------------")

    # Merge all XML into a df
    df_data = mergeXmlIntoDataframe(all_list, tempFile)
    os.remove(tempFile)

    # Clean data
    df_data = cleanDataframe(df_data)

    # Write that down Patrick
    df_data.to_csv(finalCSV)

    return (0)


cProfile.run("run()", "output.dat")

with open("out_time.txt", "w") as f :
    p = pstats.Stats("output.dat", stream=f)
    p.sort_stats("time").print_stats()

with open("out_calls.txt", "w") as f :
    p = pstats.Stats("output.dat", stream=f)
    p.sort_stats("calls").print_stats()