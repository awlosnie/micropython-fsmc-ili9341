from umatrix import matrix
from math import sin, cos, radians


def scale(s):
    S = matrix(
        [s, 0, 0, 0], [0, s, 0, 0], [0, 0, s, 0], [0, 0, 0, 1])
    return S


def rotate_x(angle):
    s = sin(angle)
    c = cos(angle)
    R = matrix(
        [1, 0, 0, 0], [0, c, -s, 0], [0, s, c, 0], [0, 0, 0, 1])
    return R


def rotate_y(angle):
    s = sin(angle)
    c = cos(angle)
    R = matrix(
        [c,  0, s, 0], [0, 1, 0, 0], [-s, 0, c, 0], [0, 0, 0, 1])
    return R


def rotate_z(angle):
    s = sin(angle)
    c = cos(angle)
    R = matrix(
        [c, -s, 0, 0], [s, c, 0, 0], [0, 0, 1, 0], [0, 0, 0, 1])
    return R


def projection(width, height, near, far):
    w = 1 / width
    h = 1 / height
    n = 2 / (far - near)
    f = (far + near) / (far - near)
    P = matrix(
        [w, 0, 0, 0], [0, h, 0, 0], [0, 0, -n, 0], [0, 0, 0, -f])
    return P


@micropython.native
def render(lcd):
    cube = matrix(
            [ 1,  1,  1, 0], [ 1,  1, -1, 0],
            [ 1, -1, -1, 0], [ 1, -1,  1, 0],
            [-1,  1,  1, 0], [-1,  1, -1, 0],
            [-1, -1, -1, 0], [-1, -1,  1, 0])
    edges = [
        [0, 1, 0xf800], [1, 2, 0x07e0], [2, 3, 0x07e0],
        [3, 0, 0xf800], [4, 5, 0x001f], [5, 6, 0x001f],
        [6, 7, 0xffe0], [7, 4, 0xffe0], [0, 4, 0xf800],
        [1, 5, 0x001f], [2, 6, 0x07e0], [3, 7, 0xffe0]]
    cx = [None] * 8
    cy = [None] * 8
    angle = 0
    dl = lcd.draw_line
    clear = lcd.draw_rect
    P = projection(240, 320, -3, 3)
    cube = cube * scale(48)
    rang1 = range(8)
    rang2 = range(12)
    while angle < 500:
        angle += 5
        Rx = rotate_x(radians(angle))
        Ry = rotate_y(radians(angle))
        Rz = rotate_z(radians(angle))
        R = Rx * Ry * Rz
        m = cube * R * P
        for i in rang1:
            cx[i] = int(m[i][0] * 240 + 120)
            cy[i] = int(m[i][1] * 320 + 160)
        clear(30, 70, 210, 250, 0x0)
        for r in rang2:
            e = edges[r]
            dl(cx[e[0]], cy[e[0]], cx[e[1]], cy[e[1]], e[2])
