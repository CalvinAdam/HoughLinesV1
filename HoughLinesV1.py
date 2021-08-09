import cv2
import numpy as np
import matplotlib.pyplot as plt
import matplotlib.lines as mlines
import time


def HL_Calvin(img, threshold=15):  # The image must be grayscale
    # horizontal_his = np.zeros(len(img), dtype=np.int16)
    # vertical_his = np.zeros(len(img[0]), dtype=np.int16)
    horizontal_his = [0 for _ in range(len(img))]
    vertical_his = [0 for _ in range(len(img[0]))]
    lines_dict = {}
    start = time.perf_counter_ns()
    for linenumber, line in enumerate(img):
        for pixelnumber, pixel in enumerate(line):
            if pixel == 0:
                horizontal_his[linenumber] += 1
                vertical_his[pixelnumber] += 1
    print(f"The statement took {(time.perf_counter_ns() - start)/10**9} seconds to execute")
    lines_dict['horizontal'] = [(lambda x, xpos: xpos if x > threshold else None)(x, xpos) for xpos, x in enumerate(horizontal_his)]
    lines_dict['horizontal'] = [x for x in lines_dict['horizontal'] if x is not None]
    lines_dict['vertical'] = [(lambda x, xpos: xpos if x > threshold else None)(x, xpos) for xpos, x in enumerate(vertical_his)]
    lines_dict['vertical'] = [x for x in lines_dict['vertical'] if x is not None]
    return lines_dict


if __name__ == "__main__":
    img = cv2.imread("document", 0)
    print(HL_Calvin(img, 500))

