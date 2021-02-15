import numpy as np
import wav
from math import ceil, log10

"""
If file is not noisy then SNR and SSNR are about 100dB.
"""

def SSNR(y_pred, source, target, Frame_size):
    target_signal, target_samplerate = wav.read_wav(target)
    target_signal = np.array(target_signal)
    size_of_target = target_signal.size
    y_pred_signal, y_pred_samplerate = wav.read_wav(y_pred)
    y_pred_signal = np.array(y_pred_signal)
    size_of_y_pred = y_pred_signal.size
    source_signal, source_samplerate = wav.read_wav(source)
    source_signal = np.array(source_signal)
    size_of_source = source_signal.size

    if (size_of_target != size_of_y_pred) | (size_of_target != size_of_source):
        raise Exception("ERROR: Input output size mismatch")

    frame_size = Frame_size
    number_of_frame_size = ceil(size_of_target / frame_size)

    source_SSNR = 0
    y_pred_SSNR = 0
    nonzero_frame_number = 0
    input1, input2, signal, noise1, noise2 = [], [], [], [], []
    for i in range(number_of_frame_size):
        input1.append(source_signal[frame_size * i:frame_size * (i + 1)])
        input2.append(y_pred_signal[frame_size * i:frame_size * (i + 1)])
        signal.append(target_signal[frame_size * i:frame_size * (i + 1)])
        noise1.append(input1[i] - signal[i])
        noise2.append(input2[i] - signal[i])
        segmental_signal_power = 0
        segmental_noise1_power = 0
        segmental_noise2_power = 0
        for n in range(len(signal[i])):
            segmental_signal_power += pow(signal[i][n], 2)
            segmental_noise1_power += pow(noise1[i][n], 2)
            segmental_noise2_power += pow(noise2[i][n], 2)

        if segmental_noise1_power == 0:
            segmental_noise1_power = pow(0.1, 10)
        if segmental_noise2_power == 0:
            segmental_noise2_power = pow(0.1, 10)

        if segmental_signal_power != 0:
            nonzero_frame_number += 1
            source_SSNR += 10 * log10(segmental_signal_power / segmental_noise1_power)
            y_pred_SSNR += 10 * log10(segmental_signal_power / segmental_noise2_power)

    source_SSNR /= nonzero_frame_number
    y_pred_SSNR /= nonzero_frame_number
    gain = y_pred_SSNR - source_SSNR
    return y_pred_SSNR, source_SSNR, gain

def SNR(y_pred, source, target):
    target_signal, target_samplerate = wav.read_wav(target)
    target_signal = np.array(target_signal)
    size_of_target = target_signal.size
    y_pred_signal, y_pred_samplerate = wav.read_wav(y_pred)
    y_pred_signal = np.array(y_pred_signal)
    size_of_y_pred = y_pred_signal.size
    source_signal, source_samplerate = wav.read_wav(source)
    source_signal = np.array(source_signal)
    size_of_source = source_signal.size

    if (size_of_target != size_of_y_pred) | (size_of_target != size_of_source):
        raise Exception("ERROR: Input output size mismatch")

    signal_power = 0
    noise1_power = 0
    noise2_power = 0
    signal, noise1, noise2 = [], [], []
    signal.extend(target_signal[:])
    noise1.extend(source_signal - target_signal)
    noise2.extend(y_pred_signal - target_signal)
    for i in range(size_of_y_pred):
        signal_power += pow(signal[i], 2)
        noise1_power += pow(noise1[i], 2)
        noise2_power += pow(noise2[i], 2)

    if noise1_power == 0:
        noise1_power = pow(0.1, 10)
        # raise Exception("ERROR: Not noisy")
    if noise2_power == 0:
        noise2_power = pow(0.1, 10)

    source_SNR = 10 * log10(signal_power / noise1_power)
    y_pred_SNR = 10 * log10(signal_power / noise2_power)
    gain = y_pred_SNR - source_SNR
    return y_pred_SNR, source_SNR, gain