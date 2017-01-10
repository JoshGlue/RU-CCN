import os
import pickle
rootdir = 'pickle'

for subdir, dirs, files in os.walk(rootdir):
    for file in files:
        filename = os.path.join(subdir, file)
        print(filename)
        if os.path.getsize(filename) == 0:
            continue
        with open(filename, 'rb') as f:
                data = pickle.load(f)
        with open(filename, 'wb') as f:
            pickle.dump(data, f, protocol=2)