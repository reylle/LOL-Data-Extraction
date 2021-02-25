import constants
import logger as log
import pandas as pd
import pickle
import utils


def save_pickle(data, file_name):
    with open(file_name + '.p', 'wb') as fp:
        pickle.dump(data, fp, protocol=pickle.HIGHEST_PROTOCOL)
        fp.close()


def load_pickle(file_name):
    with open(file_name, 'rb') as fp:
        data = pickle.load(fp)
        fp.close()

    return data


def save(data, file_name):
    df = pd.DataFrame(data)
    path = constants.DATA_DIR + file_name
    extension = utils.find_extension(file_name)

    if extension == "csv":
        df.to_csv(path_or_buf=path, index=False)
    elif extension == "json":
        df.to_json(path_or_buf=path)
    else:
        error_message = constants.ERROR_NOT_IMPLEMENTED + "Only CSV and JSON extensions are accepted."
        log.inform(error_message)


def load(file_name):
    extension = utils.find_extension(file_name)

    if extension == "csv":
        result = pd.read_csv(constants.DATA_DIR + file_name).to_dict()
    elif extension == "json":
        result = pd.read_json(constants.DATA_DIR + file_name).to_dict()
    else:
        error_message = constants.ERROR_NOT_IMPLEMENTED + "Only CSV and JSON extensions are accepted."
        log.inform(error_message)
        result = None

    return result
