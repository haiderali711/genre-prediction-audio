import librosa
import numpy as np


# Extract features using librosa
def extract(audio_file):
    y, sr = librosa.load(audio_file, mono=True, duration=30)

    chroma_stft = librosa.feature.chroma_stft(y=y, sr=sr)
    rmse = librosa.feature.rms(y=y)
    spec_cent = librosa.feature.spectral_centroid(y=y, sr=sr)
    spec_bw = librosa.feature.spectral_bandwidth(y=y, sr=sr)
    rolloff = librosa.feature.spectral_rolloff(y=y, sr=sr)
    zcr = librosa.feature.zero_crossing_rate(y)
    mfcc = librosa.feature.mfcc(y=y, sr=sr)
    harmonics, perceptual = librosa.effects.hpss(y)
    tempo, _ = librosa.beat.beat_track(y=y, sr=sr)

    # Building tuple to insert
    tuple_data = f'{np.mean(chroma_stft)} {np.var(chroma_stft)} '
    tuple_data += f'{np.mean(rmse)} {np.var(rmse)} '
    tuple_data += f'{np.mean(spec_cent)} {np.var(spec_cent)} '
    tuple_data += f'{np.mean(spec_bw)} {np.var(spec_bw)} '
    tuple_data += f'{np.mean(rolloff)} {np.var(rolloff)} '
    tuple_data += f'{np.mean(zcr)} {np.var(zcr)} '
    tuple_data += f'{np.mean(harmonics)} {np.var(harmonics)} '
    tuple_data += f'{np.mean(perceptual)} {np.var(perceptual)} '
    tuple_data += f'{tempo} '

    for e in mfcc:
        tuple_data += f' {np.mean(e)} {np.var(e)}'

    return tuple(tuple_data.split())
