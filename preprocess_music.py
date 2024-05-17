import librosa
import numpy as np
import os
from multiprocessing import Pool
import audioread

async def preprocess(filename: str, new_filename: str, cqt_time_reduction=20) -> None:
    read = audioread.audio_open(filename)
    song, sr = librosa.load(read)
    cqt = np.abs(librosa.cqt(y=song, sr=sr))
    height, length = cqt.shape
    cqt_compressed = cqt[:, :(length//cqt_time_reduction)*cqt_time_reduction].reshape(height, -1, cqt_time_reduction).mean(axis=2)
    np.save(new_filename, cqt_compressed)

def preprocess_path(path: str, out_path: str, cqt_time_reduction = 20, threads: int = 1) -> None:
    file_list = os.listdir(path)
    new_file_list = list(map(lambda x: out_path + '/' + x[:x.rfind('.')] + '.npy', file_list))
    os.makedirs(out_path, exist_ok=True)
    if threads == 1:
        for file, new_file in zip(file_list, new_file_list):
            preprocess(file, new_file, cqt_time_reduction)
    elif threads < 1:
        raise ValueError("Threads must be a positive integer")
    else:
        pool = Pool(threads)
        pool.starmap(preprocess, list(zip(file_list, new_file_list, [cqt_time_reduction]*len(file_list))))
        pool.map()
        pool.close()
        pool.join()
'''
file_list = os.listdir('music')
preprocess('music/' + file_list[0], 'sample.npy')
arr = np.load('sample.npy')
print(arr.shape)
'''