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

def line_detection_non_vectorized(image, edge_image, num_rhos=180, num_thetas=180, t_count=220):
    edge_height, edge_width = edge_image.shape[:2]
    edge_height_half, edge_width_half = edge_height / 2, edge_width / 2
    #
    d = np.sqrt(np.square(edge_height) + np.square(edge_width))
    dtheta = 180 / num_thetas
    drho = (2 * d) / num_rhos
    #
    thetas = np.arange(0, 180, step=dtheta)
    rhos = np.arange(-d, d, step=drho)
    #
    cos_thetas = np.cos(np.deg2rad(thetas))
    sin_thetas = np.sin(np.deg2rad(thetas))
    #
    accumulator = np.zeros((len(rhos), len(rhos)))
    #
    figure = plt.figure(figsize=(12, 12))
    subplot1 = figure.add_subplot(1, 4, 1)
    subplot1.imshow(image)
    subplot2 = figure.add_subplot(1, 4, 2)
    subplot2.imshow(edge_image, cmap="gray")
    subplot3 = figure.add_subplot(1, 4, 3)
    subplot3.set_facecolor((0, 0, 0))
    subplot4 = figure.add_subplot(1, 4, 4)
    subplot4.imshow(image)
    #
    for y in range(edge_height):
        for x in range(edge_width):
            if edge_image[y][x] != 0:
                edge_point = [y - edge_height_half, x - edge_width_half]
                ys, xs = [], []
                for theta_idx in range(len(thetas)):
                    rho = (edge_point[1] * cos_thetas[theta_idx]) + (edge_point[0] * sin_thetas[theta_idx])
                    theta = thetas[theta_idx]
                    rho_idx = np.argmin(np.abs(rhos - rho))
                    accumulator[rho_idx][theta_idx] += 1
                    ys.append(rho)
                    xs.append(theta)
                subplot3.plot(xs, ys, color="white", alpha=0.05)

    for y in range(accumulator.shape[0]):
        for x in range(accumulator.shape[1]):
            if accumulator[y][x] > t_count:
                rho = rhos[y]
                theta = thetas[x]
                a = np.cos(np.deg2rad(theta))
                b = np.sin(np.deg2rad(theta))
                x0 = (a * rho) + edge_width_half
                y0 = (b * rho) + edge_height_half
                x1 = int(x0 + 1000 * (-b))
                y1 = int(y0 + 1000 * a)
                x2 = int(x0 - 1000 * (-b))
                y2 = int(y0 - 1000 * a)
                subplot3.plot([theta], [rho], marker='o', color="yellow")
                subplot4.add_line(mlines.Line2D([x1, x2], [y1, y2]))

    subplot3.invert_yaxis()
    subplot3.invert_xaxis()

    subplot1.title.set_text("Original Image")
    subplot2.title.set_text("Edge Image")
    subplot3.title.set_text("Hough Space")
    subplot4.title.set_text("Detected Lines")
    plt.show()
    return accumulator, rhos, thetas


if __name__ == "__main__":
    img = cv2.imread("C:/Users/Calvin/find_lines/preprocessed_documents/L1-2010-1.tif", 0)
    # line_detection_non_vectorized(img, img)
    print(HL_Calvin(img, 500))

