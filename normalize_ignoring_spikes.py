import argparse
import numpy as np
from scipy.io import wavfile

if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument("input")
    parser.add_argument("-p","--percentile", default=99.9, type=float)
    parser.add_argument("-f","--headroom_factor", default=2, type=float)
    parser.add_argument("-o","--output", default="output.wav", type=str)
    args = parser.parse_args()

    input = wavfile.read(args.input)
    wave_int = input[1]
    wave_type = wave_int.dtype
    wave_type_max = np.iinfo(wave_type).max
    wave_max = np.max(wave_int)
    wave_percentile = np.percentile(wave_int,args.percentile)

    print(f"Input| type max: {wave_type_max} | max: {wave_max} | percentile {args.percentile}: {wave_percentile}")

    wave_gain = float(wave_type_max)/float(wave_percentile)/args.headroom_factor

    print(f"Applied multiplier: {wave_gain}")

    wave_float = np.array(wave_int,dtype=float)
    wave_float_normalized = wave_float*wave_gain

    wave_normalized_int = np.array(wave_float_normalized, dtype=wave_type)

    wavfile.write(args.output, input[0], wave_normalized_int)

    print("Done.")
