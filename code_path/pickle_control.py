import pickle
import os

def save_data(files_obj, file):
    with open(file, 'wb') as f:
        # Pickle the 'data' dictionary using the highest protocol available.
        pickle.dump(files_obj, f, pickle.HIGHEST_PROTOCOL)

def load_data(data_path):
    #print(data_path)
    if os.path.exists(data_path):
        with open(data_path, 'rb') as f:
            # The protocol version used is detected automatically, so we do not
            # have to specify it.
            data = pickle.load(f)
        return data
    else:
        return {}

def delete_data(filepath):
    save_data({}, filepath)