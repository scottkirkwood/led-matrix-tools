#!/usr/bin/env python
import serial
import time
import text2pixels

special = {}
execfile('special.py')

def ScrollingInfo(lines, speed=0.1, leadin=0, leadout=0):
  """Must be 8 lines."""
  ser.write('\r') # Reset
  width = len(lines[0])
  if leadin > 8:
    leadin = 8
  for x in range(leadin):
    for row in lines:
      ser.write(' ' * (8 - x) + row[:x])
    ser.write('\n')
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


def MovingText(text, color, times=1):
  lines = text2pixels.Get8PixelsHigh(text, color)
  for x in range(times):
    ScrollingInfo(lines, speed=0.1, leadin=0, leadout=0)

def MovingText2(text, color):
  ser.write('\r')
  lines = text2pixels.Get8PixelsHigh(text, color)
  for line in lines:
    ser.write(line)
    ser.write('\n')

def OneColor(color):
  ser.write('\r')
  for row in range(8):
    ser.write(color * 8)
    ser.write('\n')
  ser.flush()


def SetImage(image):
  ser.write('\r') # Reset
  for row in special[image]:
    ser.write(row)
    ser.write('\n')
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
  for color in ['G', 'R', 'O', ' ']:
    OneColor(color)
    time.sleep(0.2)


if __name__ == '__main__':
  import optparse
  desc = ('For text you can pass some words to show.  '
    'If it\'s one of the following, however it will show something '
    'special:\n%s') % '\n'.join(['  %r: %s' % (k, v[0]) for k, v, in special.items()])

  parse = optparse.OptionParser('%prog [options] text\n' + desc)
  parse.add_option('-g', '--green', dest='green', action='store_true',
      help='Show text in green')
  parse.add_option('-r', '--red', dest='red', action='store_true',
      help='Show text in red')
  parse.add_option('-o', '--orange', dest='orange', action='store_true',
      help='Show text in orange')
  parse.add_option('-t', '--times', dest='times', type='int',
      help='Number of times to scroll text', default=100)

  options, args = parse.parse_args()

  app = text2pixels.Init()
  ser = serial.Serial('/dev/ttyUSB0', 9600)
  WarmUp()
  if args[0] in special:
    SetImage(args[0])
  else:
    ch = 'G'
    if options.red:
      ch = 'R'
    elif options.orange:
      ch = 'O'
    print ' '.join(args)
    MovingText2(' '.join(args), ch)
  ser.close()
