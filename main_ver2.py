import sys
import os
import customfunction as cf
import get_signal_to_noise_ver2 as stn

frame_size = 1601

if len(sys.argv) < 4:
    print("Insufficient Arguments!")
    print("help: source target y_pred (option: frame size)")
    sys.exit()
else:
    # training_source_path is path or file?
    test_source_path = sys.argv[1]
    source_path_isdir = os.path.isdir(test_source_path)

    test_target_path = sys.argv[2]
    y_pred_path = sys.argv[3]

    # make test data
    if source_path_isdir:
        test_source_file_list = cf.read_path_list(test_source_path, "wav")
        test_target_file_list = cf.read_path_list(test_target_path, "wav")
        y_pred_file_list = cf.read_path_list(y_pred_path, "wav")
    else:
        test_source_file_list = [test_source_path]
        test_target_file_list = [test_target_path]
        y_pred_file_list = [y_pred_path]

    # set frame_size, optional
    if len(sys.argv) == 5:
        frame_size = int(sys.argv[4])

    with open('log.csv', 'w') as csvfile:
        csvfile.write("file name, ssnr(dB), , snr(dB), , gain, \n")
        csvfile.write(" , source, y_pred, source, y_pred, SSNR, SNR\n")

    for i in range(len(test_source_file_list)):
        source = test_source_file_list[i]
        target = test_target_file_list[i]
        y_pred = y_pred_file_list[i]

        y_pred_ssnr, source_ssnr , ssnr_gain= stn.SSNR(y_pred, source, target, frame_size)
        y_pred_snr, source_snr, snr_gain = stn.SNR(y_pred, source, target)

        str = "{} | source_ssnr = {}dB | y_pred_ssnr = {}dB | source_snr = {}dB | y_pred_snr = {}dB | SSNR_gain = {}dB | SNR_gain = {}dB"\
            .format(source, source_ssnr, y_pred_ssnr, source_snr, y_pred_snr, ssnr_gain, snr_gain)
        print(str)

        with open('log.txt', 'a') as f:
            f.write(str + "\n")
        with open('log.csv', 'a') as csvfile:
            csvfile.write("{}, {}, {}, {}, {}, {}, {}\n".format(source, source_ssnr, y_pred_ssnr, source_snr, y_pred_snr, ssnr_gain, snr_gain))