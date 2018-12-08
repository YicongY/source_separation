import librosa
import numpy as np
import scipy
from mir_eval.separation import bss_eval_sources 

def load_wav(filename, sr=16000):
	'''
	returns the wav format using sampling rate of 16000
	'''
	data, sr = librosa.load(filename, sr=sr, mono=False)
	mixed = librosa.to_mono(data)
	s1, s2 = data[0,:], data[1,:]
	return mixed, s1, s2

def reconstruct_wav(mag, phase, hop_length=256):
	'''
	using istft to reconstruct the wav format
	'''
	new_phase = np.exp(1.j * phase)
	new_wav = librosa.istft(mag*new_phase, hop_length=hop_length)

	return new_wav

def get_spec(wav, n_fft=1024, window="hamming", hop_length=256):
	return librosa.stft(wav, window=window, n_fft=n_fft, hop_length=hop_length)

def get_angle(spec):
	return np.angle(spec)

def get_mag(spec):
	'''
	should we also take the log?
	'''
	return np.abs(spec)

def save_wav(filename, wav, sr=16000):
	'''
	saves the wav to filename
	'''
	scipy.io.wavfile.write(filename, sr, wav)

def bss_eval(mixed_wav, src1_wav, src2_wav, pred_src1_wav, pred_src2_wav):
    len = pred_src1_wav.shape[0]
    src1_wav = src1_wav[:len]
    src2_wav = src2_wav[:len]
    mixed_wav = mixed_wav[:len]
    sdr, sir, sar, _ = bss_eval_sources(np.array([src1_wav, src2_wav]),
                                        np.array([pred_src1_wav, pred_src2_wav]), compute_permutation=True)
    sdr_mixed, _, _, _ = bss_eval_sources(np.array([src1_wav, src2_wav]),
                                          np.array([mixed_wav, mixed_wav]), compute_permutation=True)
    # sdr, sir, sar, _ = bss_eval_sources(src2_wav,pred_src2_wav, False)
    # sdr_mixed, _, _, _ = bss_eval_sources(src2_wav,mixed_wav, False)
    nsdr = sdr - sdr_mixed
    return nsdr, sir, sar, len



