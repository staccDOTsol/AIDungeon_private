import os
import tarfile

import gpt_2_simple as gpt2
import ctypes

hllDll = ctypes.WinDLL("C:\\Program Files\\NVIDIA GPU Computing Toolkit\\CUDA\\v10.0\\bin\\cudart64_100.dll")
hllDll2 = ctypes.WinDLL("C:\\Program Files\\NVIDIA GPU Computing Toolkit\\CUDA\\v10.0\\bin\\cublas64_100.dll")
hllDll3 = ctypes.WinDLL("C:\\Program Files\\NVIDIA GPU Computing Toolkit\\CUDA\\v10.0\\bin\\cufft64_100.dll")
hllDll4 = ctypes.WinDLL("C:\\Program Files\\NVIDIA GPU Computing Toolkit\\CUDA\\v10.0\\bin\\curand64_100.dll")
hllDll5 = ctypes.WinDLL("C:\\Program Files\\NVIDIA GPU Computing Toolkit\\CUDA\\v10.0\\bin\\cusolver64_100.dll")
hllDll6 = ctypes.WinDLL("C:\\Program Files\\NVIDIA GPU Computing Toolkit\\CUDA\\v10.0\\bin\\cusparse64_100.dll")
hllDll7 = ctypes.WinDLL("C:\\Program Files\\NVIDIA GPU Computing Toolkit\\CUDA\\v10.0\\bin\\cudnn64_7.dll")

model_name = "124M"
if not os.path.isdir(os.path.join("models", model_name)):
    print("Downloading ", model_name, " model...")
    gpt2.download_gpt2(
        model_name=model_name
    )  # model is saved into current directory under /models/124M/

file_name = "text_adventures.txt"

sess = gpt2.start_tf_sess()
gpt2.finetune(
    sess,
    file_name,
    multi_gpu=True,
    batch_size=1,
    learning_rate=0.0001,
    model_name=model_name,
    sample_every=100,
    max_checkpoints=8,
    save_every=100,
    steps=5000,
)

gpt2.generate(sess)