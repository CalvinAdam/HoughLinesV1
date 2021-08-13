import cv2


def HL_Calvin(img, threshold=15, min_line_length=30, max_line_skip=1):  # The image must be grayscale
    horizontal_his = [0 for _ in range(len(img))]
    vertical_his = [0 for _ in range(len(img[0]))]
    lines_dict = {}
    longest_line_index = 0
    lines = []
    for linenumber, line in enumerate(img):  # Adds the black pixels to their
        # corresponding line and column buckets
        for pixelnumber, pixel in enumerate(line):
            horizontal_his[linenumber] += not bool(pixel)
            vertical_his[pixelnumber] += not bool(pixel)
    #  Eliminates the zero values but keeps the indices of the nonzero values
    lines_dict['horizontal'] = {i: x for i, x in enumerate(horizontal_his) if x > threshold}
    lines_dict['vertical'] = {i: x for i, x in enumerate(vertical_his) if x > threshold}
    # Finds the horizontal and vertical lines
    for lineindex, linevalue in lines_dict['horizontal'].items():
        img_line = img[lineindex]
        pixelindex = 0
        current_line_value = linevalue
        while pixelindex < len(img_line):
            pixel = img_line[pixelindex]
            if pixel == 0:
                line_skip = max_line_skip
                for lengthindex, length in enumerate(img_line[pixelindex:]):
                    if length == 255:
                        line_skip -= 1
                        if line_skip <= 0:
                            break
                    else:
                        line_skip = max_line_skip
                if lengthindex > min_line_length:
                    line = [pixelindex, lineindex, pixelindex+lengthindex, lineindex]
                    lines.append(line)
                    current_line_value -= lengthindex
                if current_line_value < min_line_length:
                    break
                else:
                    pixelindex = pixelindex+lengthindex
            else:
                pixelindex += 1
    for columnindex, columnvalue in lines_dict['vertical'].items():
        img_column = img[:, columnindex]
        pixelindex = 0
        current_column_value = columnvalue
        while pixelindex < len(img_column):
            pixel = img_column[pixelindex]
            if pixel == 0:
                line_skip = max_line_skip
                for lengthindex, length in enumerate(img_column[pixelindex:]):
                    if length == 255:
                        line_skip -= 1
                        if line_skip <= 0:
                            break
                    else:
                        line_skip = max_line_skip
                if lengthindex > min_line_length:
                    column = [columnindex, pixelindex, columnindex, pixelindex+lengthindex]
                    lines.append(column)
                    current_column_value -= lengthindex
                if current_column_value < min_line_length:
                    break
                else:
                    pixelindex = pixelindex+lengthindex
            else:
                pixelindex += 1
    img = cv2.cvtColor(img, cv2.COLOR_GRAY2BGR)
    #  Adds the lines to the image
    for line in lines:
        x1, y1, x2, y2 = line
        cv2.line(img, (x1, y1), (x2, y2), (0, 128, 0), 1)
    return lines, img


if __name__ == "__main__":
    img = cv2.imread("document", 0)
    lines, img = HL_Calvin(img, threshold=50, max_line_skip=3)
    cv2.imshow('Image with lines', img)
    cv2.imwrite('linesdoc.jpg', img)
    cv2.waitKey(0)
