import tkinter.filedialog as filedialog
import tkinter as tk
import customfunction as cf
import get_signal_to_noise as stn
import os

master = tk.Tk()
master.title("Signal to Noise Ratio")

def input1():
    input1_path = tk.filedialog.askdirectory()
    input1_entry.delete(1, tk.END)  # Remove current text in entry
    input1_entry.insert(0, input1_path)  # Insert the 'path'

def input2():
    input2_path = tk.filedialog.askdirectory()
    input2_entry.delete(1, tk.END)  # Remove current text in entry
    input2_entry.insert(0, input2_path)  # Insert the 'path'

def begin():
    frame_size = 1601

    # training_source_path is path or file?
    test_source_path = input1_entry.get()
    source_path_isdir = os.path.isdir(test_source_path)

    test_target_path = input2_entry.get()

    # make test data
    if source_path_isdir:
        test_source_file_list = cf.read_path_list(test_source_path, "wav")
        test_target_file_list = cf.read_path_list(test_target_path, "wav")
    else:
        test_source_file_list = [test_source_path]
        test_target_file_list = [test_target_path]

    for i in range(len(test_source_file_list)):
        source = test_source_file_list[i]
        target = test_target_file_list[i]

        ssnr = stn.SSNR(source, target, frame_size)
        snr = stn.SNR(source, target)

        str = "{} | ssnr = {}dB | snr = {}dB".format(source, ssnr, snr)
        print(str)

        with open('log.txt', 'a') as f:
            f.write(str + "\n")
    master.destroy()

top_frame = tk.Frame(master)
bottom_frame = tk.Frame(master)
line = tk.Frame(master, height=1, width=400, bg="grey80", relief='groove')
input1_path = tk.Label(top_frame, text="Source File Path:")
input1_entry = tk.Entry(top_frame, text="", width=40)
browse1 = tk.Button(top_frame, text="Browse", command=input1)
input2_path = tk.Label(bottom_frame, text="Target File Path:")
input2_entry = tk.Entry(bottom_frame, text="", width=40)
browse2 = tk.Button(bottom_frame, text="Browse", command=input2)
begin_button = tk.Button(bottom_frame, text='Begin!', command=begin)
top_frame.pack(side=tk.TOP)
line.pack(pady=10)
bottom_frame.pack(side=tk.BOTTOM)
input1_path.pack(pady=5)
input1_entry.pack(pady=5)
browse1.pack(pady=5)
input2_path.pack(pady=5)
input2_entry.pack(pady=5)
browse2.pack(pady=5)
begin_button.pack(pady=20, fill=tk.X)
master.mainloop()
