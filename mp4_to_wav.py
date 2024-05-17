import os
import librosa
import soundfile
import mutagen
from tqdm import tqdm as tq
from multiprocessing.pool import Pool

from function_call_counter import func_pbar


music_dir = 'music'
new_dir = 'music_new'
music_list = os.listdir(music_dir)
new_list = os.listdir(new_dir)

downloaded_set = set(map(lambda x: x[:-4], os.listdir(new_dir)))
not_downloaded = list(filter(lambda x: x[:-4] not in downloaded_set, music_list))

music_len = list(map(lambda x: mutagen.File(music_dir + '/' + x).info.length, tq(music_list)))
new_len = list(map(lambda x: mutagen.File(new_dir + '/' + x).info.length, tq(new_list)))
distances = [abs(l1 - l2) for l1, l2 in zip(music_len, new_len)]
differences = [l1 != l2 for l1, l2 in zip(music_len, new_len)]
difference_names = [music_list[i] if diff else None for i, diff in enumerate(differences)]
corrupted = list(filter(lambda x: x is not None, difference_names))

to_download = not_downloaded + corrupted

args = [(fn, music_dir, new_dir) for fn in to_download]

@func_pbar(len(to_download), tq)
def convert(filename: str, path, new_path):
    f, sr = librosa.load(path + '/' + filename, sr=44100, mono=False)
    soundfile.write(new_path + '/' + filename[:filename.rfind('.')] + '.wav', f.T, sr)

threads = 20
pool = Pool(threads)
pool.starmap(convert, args)
pool.close()
pool.join()