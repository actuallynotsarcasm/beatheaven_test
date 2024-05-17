from datasets import load_dataset, Audio
from tqdm import tqdm
import soundfile

print('loading')
dataset = load_dataset("Myrtle/CAIMAN-ASR-BackgroundNoise")
print('decoding')
sr = 44100
dataset_decoded = dataset['train'].cast_column("audio", Audio(sampling_rate=sr, mono=False))
print('transforming')
audio_data = list(tqdm(map(lambda x: x['array'], tqdm(dataset_decoded['audio']))))
data_dir = 'data'
print('saving to disk')
for i, array in enumerate(tqdm(audio_data)):
    soundfile.write(f'{data_dir}/{i}.wav', array, sr)
print('done')