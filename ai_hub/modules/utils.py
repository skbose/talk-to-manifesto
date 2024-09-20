import os

import numpy as np
import scipy.io.wavfile


def save_wav_file(
    audio: np.ndarray,
    filename: str,
    sampling_rate: int,
    output_dir: str,
):
    scipy.io.wavfile.write(
        os.path.join(output_dir, filename),
        rate=sampling_rate,
        data=audio,
    )
