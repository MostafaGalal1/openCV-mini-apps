import enum
import cv2 as cv
import numpy as np


class Mode(enum.Enum):
    draw = 1
    erase = 2


def update_mode_on_screen(text):
    global img
    text_size, _ = cv.getTextSize(text, cv.FONT_HERSHEY_SIMPLEX, 0.8, 2)
    cv.rectangle(img, (0, 0), (200, 50), (0, 0, 0), -1)
    cv.putText(img, text, (10, 30), cv.FONT_HERSHEY_SIMPLEX, 0.8, (255, 255, 255), 2)
    cv.imshow('Painter', img)


def painter(event, x, y, flags, param):
    global current_mode, vertices
    if current_mode == Mode.draw:
        if event == cv.EVENT_LBUTTONDOWN:
            vertices.append((x, y))
        draw_lines(event, x, y)
    elif current_mode == Mode.erase:
        eraser(event, x, y)
    else:
        pass


def crop_image():
    if len(vertices) == 4:
        mask = np.zeros_like(img, np.uint8)
        cv.fillPoly(mask, [np.array(vertices)], (255, 255, 255))
        cropped_img = np.bitwise_and(img, mask)

        min_x, min_y = min(vertices, key=lambda point: point[0])[0], min(vertices, key=lambda point: point[1])[1]
        max_x, max_y = max(vertices, key=lambda point: point[0])[0], max(vertices, key=lambda point: point[1])[1]
        vertices.clear()

        cv.namedWindow('Cropped image')
        cv.imshow('Cropped image', cropped_img[min_y:max_y, min_x:max_x])


def draw_lines(event, x, y):
    global img, vertices, is_drawing, start_x, start_y, lines_list
    if event == cv.EVENT_LBUTTONDOWN:
        start_x, start_y = x, y
        is_drawing = True

    if event == cv.EVENT_MOUSEMOVE and is_drawing:
        tmp_img = img.copy()
        cv.line(tmp_img, (start_x, start_y), (x, y), (255, 255, 255), 3)
        cv.imshow('Painter', tmp_img)

    if event == cv.EVENT_LBUTTONUP:
        if x != start_x or y != start_y:
            vertices.clear()
            cv.line(img, (start_x, start_y), (x, y), (255, 255, 255), 3)
            lines_list.append(((start_x, start_y), (x, y)))
            print(lines_list)
            cv.imshow('Painter', img)
        crop_image()
        is_drawing = False


def eraser(event, x, y):
    global img, is_erasing, thickness
    half_thickness = thickness // 2

    if event == cv.EVENT_LBUTTONDOWN:
        is_erasing = True

    if event == cv.EVENT_MOUSEMOVE and is_erasing:
        cv.rectangle(img, (x-half_thickness, y-half_thickness), (x+half_thickness, y+half_thickness), (0, 0, 0), -1)
        cv.imshow('Painter', img)

    if event == cv.EVENT_LBUTTONUP:
        cv.rectangle(img, (x-half_thickness, y-half_thickness), (x+half_thickness, y+half_thickness), (0, 0, 0), -1)
        is_erasing = False
        cv.imshow('Painter', img)


if __name__ == '__main__':
    is_drawing, is_erasing = False, False
    start_x, start_y = -1, -1
    lines_list = []
    vertices = []
    thickness = 0

    cv.namedWindow('Painter')
    img = np.zeros((512, 512, 3), np.uint8)
    cv.imshow('Painter', img)

    current_mode = Mode.draw
    update_mode_on_screen('Drawing mode')

    cv.setMouseCallback('Painter', painter)

    while True:
        key = cv.waitKey(0) & 0xFF

        if key == 27:
            break
        elif key == ord('d'):
            current_mode = Mode.draw
            update_mode_on_screen('Drawing mode')
        elif key == ord('e'):
            thickness = int(input('Enter thickness: '))
            current_mode = Mode.erase
            update_mode_on_screen('Erasing mode')

    cv.destroyAllWindows()
