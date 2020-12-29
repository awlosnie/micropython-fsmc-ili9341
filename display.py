import glcdfont
import machine
import stm
import time
import micropython


LCD_REG = const(0x60000000)
LCD_RAM = const(0x60080000)


class Stm32F40x():
    def __init__(self):
        self.RCC_AHB3ENR_FSMCEN = 0x1  # bit to enable FSMC clock
        self.RCC_AHB1ENR_GPIODEN = 0x00000008  # bit to enable D port clock
        self.RCC_AHB1ENR_GPIOEEN = 0x00000010  # bit to enable E port clock
        self.FSMC_Bank1_base = 0xA0000000  # 0xA0000000 FSMC registers base address
        self.FSMC_BCR_bank1_offset = 0x0
        self.FSMC_BTR_bank1_offset = 0x4
        self.FSMC_BTR1_ADDSET_T = 0x00000001  # ILI9341, 90ns
        self.FSMC_BTR1_DATAST_T = 0x00000400  # HCLK cycles
        self.FSMC_BCR1_MWID_0 = 0x00000010
        self.FSMC_BCR1_WREN = 0x00001000
        self.FSMC_BCR1_MBKEN = 0x1
        self.FSMC_BTR1_ADDHLD_0 = 0x00000010

    @micropython.viper
    def init_fsmc(self):
        machine.mem32[stm.RCC + stm.RCC_AHB3ENR] |= self.RCC_AHB3ENR_FSMCEN
        machine.mem32[stm.RCC + stm.RCC_AHB1ENR] |= self.RCC_AHB1ENR_GPIODEN | self.RCC_AHB1ENR_GPIOEEN
        # 10 10 10 00 00 10 10 10 10 00 10 10 00 10 10 10
        machine.mem32[stm.GPIOD + stm.GPIO_MODER] = 0b10101000001010101000101000101010
        machine.mem32[stm.GPIOE + stm.GPIO_MODER] = 0xAAAA8000
        machine.mem32[stm.GPIOD + stm.GPIO_OSPEEDR] = 0xFFFFFFFF  # 0x54154525
        machine.mem32[stm.GPIOE + stm.GPIO_OSPEEDR] = 0xFFFFFFFF  # 0x55554000
        machine.mem32[stm.GPIOD + stm.GPIO_AFR0] =  ( (0b1100<<(4*0)) | (0b1100<<(4*1)) | (0b1100<<(4*2)) | (0b1100<<(4*4)) | (0b1100<<(4*5)) | (0b1100<<(4*7)) )
        machine.mem32[stm.GPIOD + stm.GPIO_AFR1] =  ( (0b1100<<(4*(8-8))) | (0b1100<<(4*(9-8))) | (0b1100<<(4*(10-8))) | (0b1100<<(4*(13-8))) | (0b1100<<(4*(14-8))) | (0b1100<<(4*(15-8))))
        machine.mem32[stm.GPIOE + stm.GPIO_AFR0] = 0b1100<<(4*7)
        machine.mem32[stm.GPIOE + stm.GPIO_AFR1] = 0xCCCCCCCC
        machine.mem32[self.FSMC_Bank1_base + self.FSMC_BTR_bank1_offset] = self.FSMC_BTR1_ADDSET_T | self.FSMC_BTR1_DATAST_T | self.FSMC_BTR1_ADDHLD_0 # | FSMC_BTR1_CLKDIV_1 | FSMC_BTR1_ACCMOD
        machine.mem32[self.FSMC_Bank1_base + self.FSMC_BCR_bank1_offset] = self.FSMC_BCR1_MWID_0 | self.FSMC_BCR1_WREN | self.FSMC_BCR1_MBKEN


class ILI9341_8Bit_Fsmc():
    def __init__(self, board: Stm32F40x = None):
        self.board: Stm32F40x = board
        if self.board is None:
            self.board = Stm32F40x()
        self.board.init_fsmc()
        self.init_display()
        self.clear(0x0)

    @micropython.native
    def __divide(self, a, b) -> int:
        return int(a / b)

    def init_display(self):
        self.cmd(0x01, bytearray(0))  # SOFTWARE RESET
        time.sleep_ms(200)
        self.cmd(0xCB, bytearray([0x39, 0x2C, 0x00, 0x34, 0x02]))  # POWER CONTROL A
        self.cmd(0xCF, bytearray([0x00, 0xC1, 0x30]))  # POWER CONTROL B
        self.cmd(0xE8, bytearray([0x85, 0x00, 0x78]))  # DRIVER TIMING CONTROL A
        self.cmd(0xEA, bytearray([0x00, 0x00]))  # DRIVER TIMING CONTROL B
        self.cmd(0xED, bytearray([0x64, 0x03, 0x12, 0x81]))  # POWER ON SEQUENCE CONTROL
        self.cmd(0xF7, bytearray([0x20]))  # PUMP RATIO CONTROL
        self.cmd(0xC0, bytearray([0x23]))  # POWER CONTROL,VRH[5:0]
        self.cmd(0xC1, bytearray([0x10]))  # POWER CONTROL,SAP[2:0]BT[3:0]
        self.cmd(0xC5, bytearray([0x3E, 0x28]))  # VCM CONTROL
        self.cmd(0xC7, bytearray([0x86]))  # VCM CONTROL 2
        self.cmd(0x36, bytearray([0x48]))  # MEMORY ACCESS CONTROL
        self.cmd(0x3A, bytearray([0x55]))  # PIXEL FORMAT 16bit
        self.cmd(0xB1, bytearray([0x00, 0x18]))  # FRAME RATIO CONTROL, STANDARD RGB COLOR
        self.cmd(0xB6, bytearray([0x08, 0x82, 0x27]))  # DISPLAY FUNCTION CONTROL
        self.cmd(0x11, bytearray(0))  # EXIT SLEEP (and wait 120ms)
        time.sleep_ms(120)
        self.cmd(0x29, bytearray(0))  # TURN ON DISPLAY
        self.cmd(0x36, bytearray([0x08]))  # setup Memory Access Control

    @micropython.viper
    def cmd(self, command: int, values):
        reg = ptr8(LCD_REG)
        ram = ptr8(LCD_RAM)
        reg[0] = command
        p_data = ptr8(values)
        for i in range(int(len(values))):
            ram[0] = p_data[i]

    @micropython.viper
    def draw_pixel(self, x: int, y: int, c: int):
        reg = ptr8(LCD_REG)
        ram = ptr8(LCD_RAM)
        reg[0] = 0x2A
        ram[0] = x >> 8
        ram[0] = x
        ram[0] = x >> 8
        ram[0] = x
        reg[0] = 0x2B
        ram[0] = y >> 8
        ram[0] = y
        ram[0] = y >> 8
        ram[0] = y
        reg[0] = 0x2C
        ram[0] = c >> 8
        ram[0] = c

    @micropython.viper
    def draw_raw(self, x1: int, y1: int, x2: int, y2: int, data):
        reg = ptr8(LCD_REG)
        ram = ptr8(LCD_RAM)
        p_data = ptr8(data)
        reg[0] = 0x2A
        ram[0] = x1 >> 8
        ram[0] = x1
        ram[0] = x2 >> 8
        ram[0] = x2
        reg[0] = 0x2B
        ram[0] = y1 >> 8
        ram[0] = y1
        ram[0] = y2 >> 8
        ram[0] = y2
        reg[0] = 0x2C
        for i in range((x2-x1+1) * (y2-y1+1) * 2):
            ram[0] = p_data[i]

    @micropython.viper
    def draw_rect(self, x1: int, y1: int, x2: int, y2: int, c: int):
        reg = ptr8(LCD_REG)
        ram = ptr8(LCD_RAM)
        reg[0] = 0x2A
        ram[0] = x1 >> 8
        ram[0] = x1
        ram[0] = x2 >> 8
        ram[0] = x2
        reg[0] = 0x2B
        ram[0] = y1 >> 8
        ram[0] = y1
        ram[0] = y2 >> 8
        ram[0] = y2
        reg[0] = 0x2C
        for i in range((x2-x1+1) * (y2-y1+1)):
            ram[0] = c >> 8
            ram[0] = c

    @micropython.viper
    def draw_line(self, x1: int, y1: int, x2: int, y2: int, c: int):
        if x1 == x2:
            if y2 > y1:
                self.draw_rect(x1, y1, x2+1, y2, c)
            else:
                self.draw_rect(x1, y2, x2+1, y1, c)
        elif y1 == y2:
            if x2 > x1:
                self.draw_rect(x1, y1, x2, y2+1, c)
            else:
                self.draw_rect(x2, y1, x1, y2+1, c)
        else:
            dp = self.draw_pixel
            shortLen: int = y2-y1
            longLen: int = x2-x1
            if abs(shortLen) > abs(longLen):
                swap: int = shortLen
                shortLen = longLen
                longLen = swap
                yLonger: bool = True
            else:
                yLonger: bool = False
            endVal: int = longLen
            if longLen < 0:
                incrementVal: int = -1
                longLen = -1 * longLen
            else:
                incrementVal: int = 1
            decInc = int(0)
            if longLen > int(0):
                decInc = int(self.__divide(shortLen << 16, longLen))
            j: int = int(0)
            if yLonger:
                for i in range(0, endVal, incrementVal):
                    dp(x1+(j >> 16), y1+int(i), c)
                    j += decInc
            else:
                for i in range(0, endVal, incrementVal):
                    dp(x1+int(i), y1+(j >> 16), c)
                    j += decInc

    @micropython.viper
    def draw_text(self, x: int, y: int, c: int, text):
        bma = bytearray(8)
        p_bm = ptr8(bma)
        for i in range(8):
            p_bm[i] = 1 << i
        dp = self.draw_pixel
        tlen = int(0)
        for t in text:
            cb, length = glcdfont.get_ch(t)
            p_cb = ptr8(cb)
            for r in range(int(len(cb))):
                for k in range(int(len(bma))):
                    if p_cb[r] & p_bm[k]:
                        dp(x+k, y+tlen+r, c)
            tlen += int(length)

    @micropython.viper
    def clear(self, color: int = 0x0000):
        self.draw_rect(0, 0, 240, 320, color)
