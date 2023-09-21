import enum
import math

import cv2 as cv
import numpy as np


class Shape(enum.Enum):
    circle = 1
    rectangle = 2
    polygon = 3


def update_mode_on_screen(text):
    global img, background_color, color
    text_size, _ = cv.getTextSize(text, cv.FONT_HERSHEY_SIMPLEX, 0.8, 2)
    cv.rectangle(img, (0, 0), (150, 50), background_color, -1)
    cv.putText(img, text, (10, 30), cv.FONT_HERSHEY_SIMPLEX, 0.8, color, 2)
    cv.imshow('Painter', img)


def painter(event, x, y, flags, param):
    global current_shape
    if current_shape == Shape.circle:
        draw_circle(event, x, y)
    elif current_shape == Shape.rectangle:
        draw_rectangle(event, x, y)
    elif current_shape == Shape.polygon:
        draw_vertex(event, x, y)
    else:
        pass


def calculate_euclidean_distance(x1, y1, x2, y2):
    return int(math.sqrt((x1 - x2) ** 2 + (y1 - y2) ** 2))


def draw_circle(event, x, y):
    global img, color, is_drawing, start_x, start_y
    if event == cv.EVENT_LBUTTONDOWN:
        start_x, start_y = x, y
        is_drawing = True

    if event == cv.EVENT_MOUSEMOVE and is_drawing:
        tmp_img = img.copy()
        cv.circle(tmp_img, (start_x, start_y), calculate_euclidean_distance(start_x, start_y, x, y), color, 2)
        cv.imshow('Painter', tmp_img)

    if event == cv.EVENT_LBUTTONUP:
        cv.circle(img, (start_x, start_y), calculate_euclidean_distance(start_x, start_y, x, y), color, 2)
        is_drawing = False
        cv.imshow('Painter', img)


def draw_rectangle(event, x, y):
    global img, color, is_drawing, start_x, start_y
    if event == cv.EVENT_LBUTTONDOWN:
        start_x, start_y = x, y
        is_drawing = True

    if event == cv.EVENT_MOUSEMOVE and is_drawing:
        tmp_img = img.copy()
        cv.rectangle(tmp_img, (start_x, start_y), (x, y), color, 2)
        cv.imshow('Painter', tmp_img)

    if event == cv.EVENT_LBUTTONUP:
        cv.rectangle(img, (start_x, start_y), (x, y), color, 2)
        is_drawing = False
        cv.imshow('Painter', img)


def draw_vertex(event, x, y):
    global img, color, vertices
    if event == cv.EVENT_LBUTTONDOWN:
        tmp_img = img.copy()
        vertices.append((x, y))
        for vertex in vertices:
            cv.circle(tmp_img, vertex, 2, color, -1)
        cv.imshow('Painter', tmp_img)


def draw_polygon():
    global img, color, vertices
    cv.polylines(img, [np.array(vertices).reshape((-1, 1, 2))], True, color, 2)
    vertices.clear()
    cv.imshow('Painter', img)


if __name__ == '__main__':
    is_drawing, is_erasing = False, False
    start_x, start_y = -1, -1
    thickness = 0
    vertices = []

    width, height = int(input('Enter width: ')), int(input('Enter height: '))
    print('Enter color values (0-255):')
    B, G, R = int(input('Enter blue: ')), int(input('Enter green: ')), int(input('Enter red: '))

    background_color = (B, G, R)
    color = (255 - B, 255 - G, 255 - R)

    cv.namedWindow('Painter')
    img = np.full((width, height, 3), (B, G, R), np.uint8)
    cv.imshow('Painter', img)

    current_shape = Shape.circle
    update_mode_on_screen('Circle')

    cv.setMouseCallback('Painter', painter)

    while True:
        key = cv.waitKey(0) & 0xFF

        if key == 27:
            break
        elif key == ord('c'):
            vertices.clear()
            current_shape = Shape.circle
            update_mode_on_screen('Circle')
        elif key == ord('r'):
            vertices.clear()
            current_shape = Shape.rectangle
            update_mode_on_screen('Rectangle')
        elif key == ord('p'):
            current_shape = Shape.polygon
            update_mode_on_screen('Polygon')
        elif key == ord('E'):
            draw_polygon()

    cv.destroyAllWindows()
