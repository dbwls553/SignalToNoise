import numpy as np
import wav
from math import ceil, log10


def SSNR(y_pred, target, Frame_size):
    target_signal, target_samplerate = wav.read_wav(target)
    target_signal = np.array(target_signal)
    size_of_target = target_signal.size
    y_pred_signal, y_pred_samplerate = wav.read_wav(y_pred)
    y_pred_signal = np.array(y_pred_signal)
    size_of_y_pred = y_pred_signal.size

    if size_of_target != size_of_y_pred:
        raise Exception("ERROR: Input output size mismatch")

    frame_size = Frame_size
    number_of_frame_size = ceil(size_of_target / frame_size)

    S_SNR = 0
    signal, origin, noise = [], [], []
    for i in range(number_of_frame_size):
        signal.append(y_pred_signal[frame_size * i:frame_size * (i + 1)])
        origin.append(target_signal[frame_size * i:frame_size * (i + 1)])
        noise.append(signal[i] - origin[i])
        segmental_signal_power = 0
        segmental_noise_power = 0
        for n in range(len(signal[i])):
            segmental_signal_power += pow(signal[i][n], 2)
            segmental_noise_power += pow(noise[i][n], 2)
        if segmental_noise_power == 0:
            segmental_noise_power = 0.0001
        if segmental_signal_power == 0:
            segmental_signal_power = 0.0001
        S_SNR += 10 * log10(segmental_signal_power / segmental_noise_power)

    S_SNR /= number_of_frame_size
    return S_SNR

def SNR(y_pred, target):
    target_signal, target_samplerate = wav.read_wav(target)
    target_signal = np.array(target_signal)
    size_of_target = target_signal.size
    y_pred_signal, y_pred_samplerate = wav.read_wav(y_pred)
    y_pred_signal = np.array(y_pred_signal)
    size_of_y_pred = y_pred_signal.size

    if size_of_target != size_of_y_pred:
        raise Exception("ERROR: Input output size mismatch")

    signal_power = 0
    noise_power = 0
    signal, origin, noise = [], [], []
    signal.extend(y_pred_signal[:])
    origin.extend(target_signal[:])
    noise.extend(y_pred_signal - target_signal)
    for i in range(size_of_y_pred):
        signal_power += pow(signal[i], 2)
        noise_power += pow(noise[i], 2)

    if noise_power == 0:
        raise Exception("ERROR: Not noisy")
    snr = 10 * log10(signal_power / noise_power)
    return snr



test_source = './train_data/source/result_male.wav'
test_target = './train_data/target/metro_male_orig.wav'
ssnr = SSNR(test_source, test_target, 640)
snr = SNR(test_source, test_target)
print("ssnr = {}".format(ssnr), "snr = {}".format(snr), sep="\n")