#!/usr/bin/env python
import serial
import time
import text2pixels

ser = serial.Serial('/dev/ttyUSB0', 9600)

def ScrollingInfo(lines, speed=0.1, leadin=0, leadout=0):
  """Except 8 lines."""
  width = len(lines[0])
  if leadin > 8:
    leadin = 8
  for x in range(leadin):
    for row in lines:
      ser.write(' ' * (8 - x) + row[:x])
    ser.flush()
    time.sleep(speed)
  for x in range(width - 8 + leadout):
    for row in lines:
      ser.write(row[x: x + 8])
      if width - x < 8:
        rest = 8 - (width - x)
        ser.write(' ' * rest)
    ser.flush()
    time.sleep(speed)

def MovingText(text):
  lines = text2pixels.Get8PixelsHigh(text, 'G')
  ScrollingInfo(lines, speed=0.001, leadin=8, leadout=8)

def OneColor(color):
  ser.write('\n')
  ser.write(color * 64)
  ser.flush()

def MovingLines():
  for i in range(1000):
    lines = []
    for line in range(8):
      if (i + line) % 8 == 0:
        lines.append('RRRRRRRR')
      elif (i + line) % 8 == 1:
        lines.append('GGGGGGGG')
      else:
        lines.append('        ')
      ser.write(''.join(lines))
      ser.flush()
      time.sleep(0.5)

def WarmUp():
  OneColor('G')
  time.sleep(0.2)
  OneColor('R')
  time.sleep(0.2)
  OneColor('O')
  time.sleep(0.2)
  OneColor(' ')
  time.sleep(0.2)

app = text2pixels.Init()
WarmUp()
MovingText('Cruzeiro!')
ser.close()
