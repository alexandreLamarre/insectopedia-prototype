import requests
import os
import json
import warnings

def setupSimpleDatabase(path_to_kaggle_database):
    '''!
    @brief 

    Make API calls to insect GBIF (https://api.gbif.org/v1/)
    base on the directory structure of the dataset found here :
    https://www.kaggle.com/kmldas/insect-identification-from-habitus-images

    Make sure you don't modify the format provided from kaggle, since we 
    use this assumption about the directory structure to make the GBIF
    '''
    if not isinstance(path_to_kaggle_database,str):
        raise TypeError("Expected path to database directory to be a string")
    

    if path_to_kaggle_database.endswith('.tar'):
        raise RuntimeError('Database needs to be extracted before being processed')

    if not path_to_kaggle_database.endswith('database'):
        raise RuntimeError('Expected database directory to have default name "database". \
                                            please do not change anything about the dataset provided')    


    # Walk through provided sample dataset
    for (dirPath, dirName, filenames) in os.walk(path_to_kaggle_database):
        if not dirName.isDigit():
            warnings.warn('sample dataset directory "{}" could not be parsed as integer,\
                 please investigate'.format(dirName), RuntimeWarning)
        else:
            insect_id = int(dirName)
            info = requestSpeciesData(insect_id)

            if info.status_code == 200:
                # Write json info to index.json in database directory,
                # so we don't need to call API constantly
                json_info = info.json()
                data = json.dumps(json_info)
                with open(dirPath+'/index.json', 'w') as f:
                    f.write(data)
            else:
                warnings.warn('Received status code {} from source {} for insect_id {}'.format(\
                    info.status_code,'https://api.gbif.org/v1/species/', insect_id ))




def requestSpeciesData(id):
    '''
    !
    @brief Make an API call to GBIF based on species

    
    @returns requests Request wrapper that contains data relevant to that species
    '''
    if not isinstance(id, int):
        raise TypeError('Expected Integer argument for species')

    response = requests.get('https://api.gbif.org/v1/species/' + str(id))
    return response

if __name__ == "__main__":
    
    # !!!
    # Change this to your kaggle db path
    KAGGLE_DB_PATH='/Study/dataset/simple_insect'
    print(requestSpeciesData(1035929))
    # setupSimpleDatabase(path)