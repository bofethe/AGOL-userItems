import arcgis
import pandas as pd

def getItems(link, u, p):
    '''
    This function takes the portal's URL, username, and password and saves an excel file in the home directory with the user item details.
    '''
    # Authenticate
    gis = arcgis.gis.GIS(url = link, username=u, password=p)

    # Get folder names
    folderNames = pd.DataFrame(gis.users.me.folders)['title'].to_list()
    folderNames.insert(0, None) # Put the root folder in the begining of list

    # Get info in a dataframe
    dfList = []
    for folderName in folderNames:
        itemList = gis.users.search(u)[0].items(folder=folderName)
        itemDF = pd.DataFrame(itemList)

        # Skip empty folders
        if itemDF.empty:
            continue

        # Reduce the number of fields exported
        keeps = ['id', 'title', 'type', 'access', 'size']
        itemDF_select = itemDF[keeps].copy()

        # Store dataframe in list
        itemDF_select['folder'] = folderName
        dfList.append(itemDF_select)

    # Combine dataframes and export
    df = pd.concat(dfList)

    outputName = u + '_content.xlsx'
    df.to_excel(outputName, index=False)

    #Return user dataframe
    return df