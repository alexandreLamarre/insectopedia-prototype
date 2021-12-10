import pytest
import json
import pathlib  # Requires Python >= 3.5
import os
from setup_api import dumpInsectIndex, requestSpeciesData, setupSimpleDatabase

TMP_DIR = '/tmp/insectopedia/test/database'
TEST_API = '1035929'
TMP_API_DIR = TMP_DIR + '/' + TEST_API


@pytest.fixture
def setupTestDatabaseDirectory():
    '''!
    @brief
    Creates a Test directory that mimcs the structure of the default kaggle dataset
    '''
    pathlib.Path(TMP_DIR).mkdir(parents=True, exist_ok=True)
    pathlib.Path(TMP_API_DIR).mkdir(parents=True, exist_ok=True)


def test_requestSpeciesData():
    '''!
    @brief

    Tests requestSpeciesData and GBIF API is available
    '''

    # Expect sucess scenario
    resp = requestSpeciesData(int(TEST_API))

    assert resp.status_code == 200, 'Expected gbif API to have a HTTP return code of 200, instead got : {}'.format(
        resp.status_code)

    data = resp.json()
    expected_data = json.loads(''' {"key": 1035929, "nubKey": 1035929, "nameKey": 1427062, "taxonID": "gbif:1035929", "sourceTaxonKey": 174449233, "kingdom": "Animalia", "phylum": "Arthropoda", "order": "Coleoptera", "family": "Carabidae", "genus": "Bembidion", "species": "Bembidion testaceum", "kingdomKey": 1, "phylumKey": 54, "classKey": 216, "orderKey": 1470, "familyKey": 3792, "genusKey": 1035920, "speciesKey": 1035929, "datasetKey": "d7dddbf4-2cf0-4f39-9b2a-bb099caae36c", "constituentKey": "7ddf754f-d193-4cc9-b351-99906754a03b", "parentKey": 1035920, "parent": "Bembidion", "scientificName": "Bembidion testaceum (Duftschmid, 1812)", "canonicalName": "Bembidion testaceum", "authorship": " (Duftschmid, 1812)", "nameType": "SCIENTIFIC", "rank": "SPECIES", "origin": "SOURCE", "taxonomicStatus": "ACCEPTED", "nomenclaturalStatus": [], "remarks": "", "numDescendants": 3, "lastCrawled": "2021-11-29T13:11:38.124+0000", "lastInterpreted": "2021-11-29T11:53:37.544+0000", "issues": [], "synonym": false, "class": "Insecta"}''')
    assert data == expected_data, 'API data mismatch from expected values (valid as of Dec 2021)'

    # expect failure scenario
    with pytest.raises(TypeError):
        resp = requestSpeciesData(['arbitrary type'])


def test_dumpInsectIndex(setupTestDatabaseDirectory):
    '''!
    @brief
    Checks that we dump api results correctly in test database directory
    '''
    dumpInsectIndex(TMP_DIR, TEST_API)

    with open(TMP_API_DIR+'/index.json', 'r') as f:
        read_data = f.readlines()
        read_data = ''.join(read_data)
        read_data = json.loads(read_data)
        expected_data = json.loads(''' {"key": 1035929, "nubKey": 1035929, "nameKey": 1427062, "taxonID": "gbif:1035929", "sourceTaxonKey": 174449233, "kingdom": "Animalia", "phylum": "Arthropoda", "order": "Coleoptera", "family": "Carabidae", "genus": "Bembidion", "species": "Bembidion testaceum", "kingdomKey": 1, "phylumKey": 54, "classKey": 216, "orderKey": 1470, "familyKey": 3792, "genusKey": 1035920, "speciesKey": 1035929, "datasetKey": "d7dddbf4-2cf0-4f39-9b2a-bb099caae36c", "constituentKey": "7ddf754f-d193-4cc9-b351-99906754a03b", "parentKey": 1035920, "parent": "Bembidion", "scientificName": "Bembidion testaceum (Duftschmid, 1812)", "canonicalName": "Bembidion testaceum", "authorship": " (Duftschmid, 1812)", "nameType": "SCIENTIFIC", "rank": "SPECIES", "origin": "SOURCE", "taxonomicStatus": "ACCEPTED", "nomenclaturalStatus": [], "remarks": "", "numDescendants": 3, "lastCrawled": "2021-11-29T13:11:38.124+0000", "lastInterpreted": "2021-11-29T11:53:37.544+0000", "issues": [], "synonym": false, "class": "Insecta"}''')
        assert read_data == expected_data, 'Expected to read the same data that was written'

    os.remove(TMP_API_DIR + '/index.json')


def test_setupSimpleDatabase(setupTestDatabaseDirectory):
    '''!
    @brief
    tests setting up a Simple Database from the default kaggle set
    '''
    print('failed return', requestSpeciesData(123123712379812739).status_code)
    # scenarios where we expect simpleDatabase to raise an Error
    FAILED_PATH_1 = 560
    FAILED_PATH_2 = TMP_DIR + '.tar'
    FAILED_PATH_3 = TMP_DIR + '/some_non_database_ending_string'

    with pytest.raises(TypeError):
        setupSimpleDatabase(FAILED_PATH_1)

    with pytest.raises(RuntimeError):
        setupSimpleDatabase(FAILED_PATH_2)

    with pytest.raises(RuntimeError):
        setupSimpleDatabase(FAILED_PATH_3)

    # Scenario where we expect simpleDatabase to succeed
    setupSimpleDatabase(TMP_DIR)

    with open(TMP_API_DIR+'/index.json') as f:
        db_data = f.readlines()
        db_data = ''.join(db_data)
        db_data = json.loads(db_data)
        expected_data = json.loads(''' {"key": 1035929, "nubKey": 1035929, "nameKey": 1427062, "taxonID": "gbif:1035929", "sourceTaxonKey": 174449233, "kingdom": "Animalia", "phylum": "Arthropoda", "order": "Coleoptera", "family": "Carabidae", "genus": "Bembidion", "species": "Bembidion testaceum", "kingdomKey": 1, "phylumKey": 54, "classKey": 216, "orderKey": 1470, "familyKey": 3792, "genusKey": 1035920, "speciesKey": 1035929, "datasetKey": "d7dddbf4-2cf0-4f39-9b2a-bb099caae36c", "constituentKey": "7ddf754f-d193-4cc9-b351-99906754a03b", "parentKey": 1035920, "parent": "Bembidion", "scientificName": "Bembidion testaceum (Duftschmid, 1812)", "canonicalName": "Bembidion testaceum", "authorship": " (Duftschmid, 1812)", "nameType": "SCIENTIFIC", "rank": "SPECIES", "origin": "SOURCE", "taxonomicStatus": "ACCEPTED", "nomenclaturalStatus": [], "remarks": "", "numDescendants": 3, "lastCrawled": "2021-11-29T13:11:38.124+0000", "lastInterpreted": "2021-11-29T11:53:37.544+0000", "issues": [], "synonym": false, "class": "Insecta"}''')
        assert db_data == expected_data, 'Expected data written to sample database to be the same as the API data'

    os.remove(TMP_API_DIR + '/index.json')

    # Scenario where we expect warnings
    warning_no_int_path = pathlib.Path(TMP_DIR + '/some_other')
    warning_no_int_path.mkdir(parents=True, exist_ok=True)

    with pytest.warns(RuntimeWarning):
        setupSimpleDatabase(TMP_DIR)

    does_not_exist = pathlib.Path(TMP_DIR + '/some_other/index.json')
    assert not does_not_exist.is_file(
    ), 'Expected non integer file to not have index.json data from API'

    # api call should be != 200, generating
    warning_api_not_200 = pathlib.Path(TMP_DIR+'/2131892379812739172398')
    warning_api_not_200.mkdir(parents=True, exist_ok=True)
    warning_no_int_path.rmdir()

    with pytest.warns(RuntimeWarning):
        setupSimpleDatabase(TMP_DIR)

    does_not_exist = pathlib.Path(TMP_DIR + '/2131892379812739172398')
    assert not does_not_exist.is_file()

    warning_api_not_200.rmdir()
