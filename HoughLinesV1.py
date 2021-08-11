import cv2


def HL_Calvin(img, threshold=15):  # The image must be grayscale
    horizontal_his = [0 for _ in range(len(img))]
    vertical_his = [0 for _ in range(len(img[0]))]
    lines_dict = {}
    longest_line_index = 0
    lines = []
    for linenumber, line in enumerate(img):  # Adds the black pixels to their
        # corresponding line and column buckets
        for pixelnumber, pixel in enumerate(line):
            if pixel == 0:
                horizontal_his[linenumber] += 1
                vertical_his[pixelnumber] += 1
    for his in [horizontal_his, vertical_his]:  # Combines lines
        for index, line in enumerate(his):
            if line == 0:
                continue
            else:
                longest_line = 0
                for thickness, hori_line in enumerate(his[index:]):
                    if hori_line != 0:
                        if hori_line >= longest_line:
                            longest_line = hori_line
                            longest_line_index = index + thickness
                        elif hori_line < longest_line/4:
                            his[index+thickness] = 0
                            break
                        his[index+thickness] = 0
                    else:
                        break
                his[longest_line_index] = longest_line
    #  Eliminates the zero values but keeps the indices of the nonzero values
    lines_dict['horizontal'] = {i: x for i, x in enumerate(horizontal_his) if x != 0}
    lines_dict['vertical'] = {i: x for i, x in enumerate(vertical_his) if x != 0}
    # Finds the horizontal and vertical lines
    for lineindex, linevalue in lines_dict['horizontal'].items():
        img_line = img[lineindex]
        pixelindex = 0
        while pixelindex < len(img_line):
            pixel = img_line[pixelindex]
            if pixel == 0:
                for lengthindex, length in enumerate(img_line[pixelindex:]):
                    if length == 255:
                        break
                if lengthindex > 30:
                    line = [pixelindex, lineindex, pixelindex+lengthindex, lineindex]
                    lines.append(line)
                if lengthindex > linevalue * 0.85:
                    break
                else:
                    pixelindex = pixelindex+lengthindex
            else:
                pixelindex += 1
    for columnindex, columnvalue in lines_dict['vertical'].items():
        img_column = img[:, columnindex]
        pixelindex = 0
        while pixelindex < len(img_column):
            pixel = img_column[pixelindex]
            if pixel == 0:
                for lengthindex, length in enumerate(img_column[pixelindex:]):
                    if length == 255:
                        break
                if lengthindex > 30:
                    column = [columnindex, pixelindex, columnindex, pixelindex+lengthindex]
                    lines.append(column)
                if lengthindex > columnvalue * 0.85:
                    break
                else:
                    pixelindex = pixelindex+lengthindex
            else:
                pixelindex += 1
    img = cv2.cvtColor(img, cv2.COLOR_GRAY2BGR)
    #  Adds the lines to the image
    for line in lines:
        x1, y1, x2, y2 = line
        cv2.line(img, (x1, y1), (x2, y2), (0, 128, 0), 5)
    return lines, img


if __name__ == "__main__":
    img = cv2.imread("C:/Users/Calvin/find_lines/preprocessed_documents/L1-2010-1.tif", 0)
    lines, img = HL_Calvin(img, 500)
    cv2.imshow('Image with lines', img)
    cv2.waitKey(0)

