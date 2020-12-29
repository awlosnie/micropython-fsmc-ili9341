# micropython-fsmc-ili9341
MicroPython scripts to drive a ILI9341 LCD display with STM32F407 FSMC over an 8Bit parallel bus.
The scripts mostly use the @micropython.viper decorators to get better drawing speeds.
The code was tested with an ILI9341 8Bit Parallel LCD display and a DMORE STM32F407VGT6 board.

## Pins (wiring)
```code
ILI9341       STM32F407VGT6
LCD_RST <---> 3.3V
LCD_CS  <---> GND
LCD_RS  <---> PD13
LCD_WR  <---> PD5
LCD_RD  <---> PD4
GND     <---> GND
5V      <---> 5V

LCD_D2  <---> PD0
LCD_D3  <---> PD1
LCD_D4  <---> PE7
LCD_D5  <---> PE8
LCD_D6  <---> PE9
LCD_D7  <---> PE10
LCD_D0  <---> PD14
LCD_D1  <---> PD15
```

## Simple example
For a simple example only the `driver.py` and `glcdfont.py` files are required, so copy those two files to your board and run folowing code
```python
from display import ILI9341_8Bit_Fsmc

lcd = ILI9341_8Bit_Fsmc()
lcd.clear(0x0)  # clear screan to black
lcd.draw_line(0, 0, 240, 320, 0xffff)  # draw white line
```

## Run all examples
Copy all \*.py files to your board and run following code
```python
from display import ILI9341_8Bit_Fsmc
from display_test import run_all

lcd = ILI9341_8Bit_Fsmc()  # Create an instance of the class (initializes the LCD display)
run_all(lcd)  # Run all tests
```
## Run all demo video
https://streamable.com/gu54zt
