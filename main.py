import sys
import os
import customfunction as cf
import get_signal_to_noise as stn

frame_size = 1601

if len(sys.argv) < 3:
    print("Insufficient Arguments!")
    sys.exit()
else:
    # training_source_path is path or file?
    test_source_path = sys.argv[1]
    source_path_isdir = os.path.isdir(test_source_path)

    test_target_path = sys.argv[2]

    # make test data
    if source_path_isdir:
        test_source_file_list = cf.read_path_list(test_source_path, "wav")
        test_target_file_list = cf.read_path_list(test_target_path, "wav")
    else:
        test_source_file_list = [test_source_path]
        test_target_file_list = [test_target_path]

    # set frame_size, optional
    if len(sys.argv) == 4:
        frame_size = int(sys.argv[3])

    with open('log.csv', 'w') as csvfile:
        csvfile.write("file name, ssnr(dB), snr(dB)\n")

    for i in range(len(test_source_file_list)):
        source = test_source_file_list[i]
        target = test_target_file_list[i]

        ssnr = stn.SSNR(source, target, frame_size)
        snr = stn.SNR(source, target)

        str = "{} | ssnr = {}dB | snr = {}dB".format(source, ssnr, snr)
        print(str)

        with open('log.txt', 'a') as f:
            f.write(str + "\n")
        with open('log.csv', 'a') as csvfile:
            csvfile.write("{}, {}, {}\n".format(source, ssnr, snr))