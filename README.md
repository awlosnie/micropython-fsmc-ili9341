# micropython-fsmc-ili9341
MicroPython scripts to drive a ILI9341 8Bit LCD display with STM32F407 FSMC

## Pins (wiring)
```code
ILI9341       STMF407VGT6
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
