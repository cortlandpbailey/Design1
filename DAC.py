from machine import SPI, Pin, ADC
import time
import math
import utime

#SPI Setup:
spi = SPI(0, baudrate=400000,polarity = 0, phase = 0, bits = 8, sck = Pin(18), mosi = Pin(19))
cs = Pin(17, mode=Pin.OUT, value=1)

#button Setup:
HB = 0
LB = 0
debounce_time0 = 0
interrupt_flag0 = 0
debounce_time1 = 0
interrupt_flag1 = 0
button0 = Pin(13, Pin.IN, Pin.PULL_UP)
button1 = Pin(9, Pin.IN, Pin.PULL_UP)
function_sel = [0,0]


#potentiometer setup:
freq = ADC(Pin(26))
conv_factor = 10 / 65535
frequency = 0

sin_wave = [512,639,758,862,943,998,1022,1014,974,906,812,700,576,447,323,211,117,49,9,1,25,80,161,265,384]

tri_wave = [80,165,248,331,414,496,579,662,744,827,910,993,1023,993,910,827,744,662,579,496,414,331,248,165,72]

saw_wave = [0, 41, 82, 123, 164, 205, 246, 286, 327, 368, 409, 450, 491, 532, 573, 614, 655, 696, 737, 777, 818, 859, 900, 941, 982]

#Button interrupt routine for debouncing:
def callback0(button0):
    global interrupt_flag0, debounce_time0
    if (time.ticks_ms()-debounce_time0)>200:
        interrupt_flag0 = 1
        debounce_time0=time.ticks_ms()   

def callback1(button1):
    global interrupt_flag1, debounce_time1
    if (time.ticks_ms()-debounce_time1)>200:
        interrupt_flag1 = 1
        debounce_time1=time.ticks_ms()   
        
button0.irq(trigger=Pin.IRQ_FALLING, handler=callback0)    
button1.irq(trigger=Pin.IRQ_FALLING, handler=callback1)




#wake up DAC
try:
    cs(1)
    spi.write(b"1000000000000000")
finally:
    cs(0)
#main routine
while True:
    
    f=0
    for i in range(10):
        f = f + freq.read_u16() * conv_factor
    frequency = round(f)+1
    if frequency < 10:
        frequency = 10
        
    w = int(  (1/frequency)*100000  )-6200
    if w < 225:
        w = 225
        
    
    if interrupt_flag0==1:
        interrupt_flag0=0
        if function_sel[0]==0:
            function_sel[0] = 1
        else:
            function_sel[0] = 0
            
        
    if interrupt_flag1==1:
        interrupt_flag1=0
        if function_sel[1]==0:
            function_sel[1] = 1
        else:
            function_sel[1] = 0
            
    if function_sel == [0,0]:
        #sine wave
        for i in range(25):
            LB = (sin_wave[i] << 2)
            HB = (144 | (sin_wave[i] >> 6))
            txdata =bytearray([HB, LB])
            cs(0)
            spi.write(txdata)
            cs(1)
            utime.sleep_us(w)
    elif function_sel == [0,1]:
        #saw
        for i in range(25):
            LB = (saw_wave[i] << 2)
            HB = (144 | (saw_wave[i] >> 6))
            txdata =bytearray([HB, LB])
            cs(0)
            spi.write(txdata)
            cs(1)
            utime.sleep_us(w)
    
    elif function_sel == [1,0]:
        for i in range(25):
            LB = (tri_wave[i] << 2)
            HB = (144 | (tri_wave[i] >> 6))
            txdata =bytearray([HB, LB])
            cs(0)
            spi.write(txdata)
            cs(1)
            utime.sleep_us(w)
    
    elif function_sel == [1,1]:
        #square
        LB = 255
        HB = (144 | 15)
        txdata = bytearray([HB,LB])
        cs(0)
        spi.write(txdata)
        cs(1)
        utime.sleep_us(w *20)
        
        LB = 0
        HB = (144 | 0)
        txdata = bytearray([HB,LB])
        cs(0)
        spi.write(txdata)
        cs(1)
        utime.sleep_us(w * 20)
        