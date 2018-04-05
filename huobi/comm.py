from os import listdir
import pickle

def loaddict(path, extand):
    filename_list = listdir(path)
    h = []
    for x in filename_list:
        if x.endswith(extand):
            h.append(x)
    h.reverse()

    with open(h[0],'rb') as f:
        d = pickle.load(f)

    return d
