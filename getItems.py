import arcgis
import pandas as pd

def getItems(link, u, p):
    '''
    This function takes the portal's URL, username, and password and saves an excel file in the home directory.
    '''
    # Authenticate
    gis = arcgis.gis.GIS(url = link, username=u, password=p)

    # Get info in a dataframe
    itemList = gis.users.search(u)[0].items() #NOTE This only looks at the root folder.  Pass items(folder='name') if needed.
    itemDF = pd.DataFrame(itemList)

    # Reduce the number of fields exported
    keeps = ['id', 'name', 'type', 'access', 'size']
    itemDF_select = itemDF[keeps]

    # Export the dataframe
    outputName = u + '_content.xlsx'
    itemDF_select.to_excel(outputName, index=False)