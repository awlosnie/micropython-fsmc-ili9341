import time
import random
from display import ILI9341_8Bit_Fsmc


def test_lines_1(lcd: ILI9341_8Bit_Fsmc):
    color1 = 0xf800
    color2 = 0x0ce0
    color3 = 0x001f
    colors = [0xffff, 0x0ff0, color1, color2, color3]
    draw_line = lcd.draw_line
    clear = lcd.clear
    ts = time.ticks_ms()
    for i in range(5):
        clear(0)
        for x in range(31):
            draw_line(0, 0, x*8, 320, colors[i])
        for y in range(41):
            draw_line(0, 0, 240, y*8, colors[i])
    te = time.ticks_ms()
    print("Lines x5", time.ticks_diff(te, ts), "ms")


def test_lines_2(lcd: ILI9341_8Bit_Fsmc):
    color1 = 0xf800
    color2 = 0x0ce0
    color3 = 0x001f
    colors = [0xffff, 0x0ff0, color1, color2, color3]
    draw_line = lcd.draw_line
    clear = lcd.clear
    ts = time.ticks_ms()
    for i in range(5):
        clear(0)
        for x in range(41):
            draw_line(0, x*8, x*6, 320, colors[i])
        for y in range(41):
            draw_line(y*6, 0, 240, y*8, colors[i])
    te = time.ticks_ms()
    print("Lines2 x5", time.ticks_diff(te, ts), "ms")


def test_clear(lcd: ILI9341_8Bit_Fsmc):
    color1 = 0xf800
    color2 = 0x0ce0
    color3 = 0x001f
    clear = lcd.clear
    clear(0)
    ts = time.ticks_ms()
    for _ in range(10):
        clear(color1)
        clear(color2)
        clear(color3)
    te = time.ticks_ms()
    print("Clear x30:", time.ticks_diff(te, ts), "ms")


def test_rand_pixel(lcd: ILI9341_8Bit_Fsmc):
    color1 = 0xf800
    color2 = 0x0ce0
    color3 = 0x001f
    clear = lcd.clear
    draw_pixel = lcd.draw_pixel
    clear(0)
    ts = time.ticks_ms()
    for _ in range(15000):
        x = random.randint(0, 240)
        y = random.randint(0, 320)
        draw_pixel(x, y, color1)
        x = random.randint(0, 240)
        y = random.randint(0, 320)
        draw_pixel(x, y, color2)
        x = random.randint(0, 240)
        y = random.randint(0, 320)
        draw_pixel(x, y, color3)
    te = time.ticks_ms()
    print("Random pixel x45000:", time.ticks_diff(te, ts), "ms")


def test_text_1(lcd: ILI9341_8Bit_Fsmc):
    clear = lcd.clear
    clear(0)
    ts = time.ticks_ms()
    text = "This is a long demo text example 123!@#$9sdf !!@>>K<"
    for x in range(24):
        lcd.draw_text(x * 10, 0, 0xffff, text)
    te = time.ticks_ms()
    print("Text x24:", time.ticks_diff(te, ts), "ms")


def test_text_2(lcd: ILI9341_8Bit_Fsmc):
    clear = lcd.clear
    color1 = 0xf800
    color2 = 0x0ce0
    color3 = 0x001f
    clear(0)
    ts = time.ticks_ms()
    text = "This is a long demo text example 123!@#$9sdf !!@>>K<"
    for x in range(8):
        lcd.draw_text(x * 30,      0, color1, text)
        lcd.draw_text(x * 30 + 10, 0, color2, text)
        lcd.draw_text(x * 30 + 20, 0, color3, text)
    te = time.ticks_ms()
    print("Text x24:", time.ticks_diff(te, ts), "ms")


def test_3d_cube(lcd: ILI9341_8Bit_Fsmc):
    clear = lcd.clear
    import simple3dcube
    clear(0)
    ts = time.ticks_ms()
    simple3dcube.render(lcd)
    te = time.ticks_ms()
    print("3d cube x100:", time.ticks_diff(te, ts), "ms")


def run_all(lcd: ILI9341_8Bit_Fsmc = None):
    if lcd is None:
        lcd = ILI9341_8Bit_Fsmc()
    test_lines_1(lcd)
    test_lines_2(lcd)
    test_clear(lcd)
    test_rand_pixel(lcd)
    test_text_1(lcd)
    test_text_2(lcd)
    test_3d_cube(lcd)
