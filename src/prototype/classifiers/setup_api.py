'''!
@brief Script for setting up a Sample Database containing insect data.

Expects the data from https://www.kaggle.com/kmldas/insect-identification-from-habitus-images
to be somewhere on the disk, and expects you to provide the path to it
in this file.
'''
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

    @param path_to_kaggle_database : path to the downloaded kaggle dataset called 'database'
    '''
    if not isinstance(path_to_kaggle_database, str):
        raise TypeError("Expected path to database directory to be a string")

    if path_to_kaggle_database.endswith('.tar'):
        raise RuntimeError(
            'Database needs to be extracted before being processed')

    if not path_to_kaggle_database.endswith('database'):
        raise RuntimeError('Expected database directory to have default name "database". \
                                            please do not change anything about the dataset provided')

    # Walk through provided sample dataset
    for (dirPath, dirName, _) in os.walk(path_to_kaggle_database):

        for dir in dirName:
            if dir:
                print('Parsing information from directory {}'.format(dir))
            if not dir.isdigit():
                warnings.warn('sample dataset directory "{}" could not be parsed as integer please investigate'.format(
                    dir), RuntimeWarning)
                print('Failed! Continuing...\n')
            else:
                dumpInsectIndex(dirPath, dir)


def dumpInsectIndex(dirPath, dir):
    '''!
    @brief Fetches insect information from API endpoint and write to appropriate index.json file

    Throws warnings if something fails along the way
    @param dirPath: current kaggle dataset path being investigated
    @param dir : current directory being investigated : expects a directory name composed of only digits
    '''
    insect_id = int(dir)
    print(
        'Requesting API information for insect with ID "{}"'.format(insect_id))
    info = requestSpeciesData(insect_id)

    if info.status_code == 200:
        print('Hit API Endpoint! Continuing...')
        # Write json info to index.json in database directory,
        # so we don't need to call API constantly
        json_info = info.json()
        data = json.dumps(json_info)
        outdir = dirPath + '/' + dir + '/index.json'
        print('Dumping retrieved information into {}...'.format(outdir))
        with open(outdir, 'w') as f:
            f.write(data)
        print('Done!\n')
    else:
        warnings.warn('Received status code {} from source {} for insect_id {}'.format(
            info.status_code, 'https://api.gbif.org/v1/species/', insect_id), RuntimeWarning)


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
    # Uncomment this and change variable to the location on your system
    #  where the kaggle dataset is
    # KAGGLE_DB_PATH = '/Study/dataset/simple_insect'
    # setupSimpleDatabase('/Volumes/Study/dataset/insect_simple/database')
    pass
