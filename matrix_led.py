#!/usr/bin/env python

"""Send something for the SparkFun LED matrix to display.

Code to send something to the LED matrix.
It can handle both 8x8 images or scrolling images.
Scrolling text also accepted and is handled with text2pixels.
"""
import optparse
import sys
import time
import serial
import text2pixels

special = {}
execfile('special.py')


def ScrollingInfo(lines, speed=0.1, leadin=0, leadout=0):
  """Scrolls the text using python.

  Args:
    lines: Must be exactly 8 lines.
    speed: How much of a delay between frames.
    leadin: how many blank pixels on the LHS to lead-in to.
    leadout: how many blank pixels at the end of the image.
  """
  ser.write('\r')  # Reset
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
  """Scroll the text."""
  lines = text2pixels.Get8PixelsHigh(text, color)
  for unused_x in range(times):
    ScrollingInfo(lines, speed=0.1, leadin=0, leadout=0)


def MovingText2(text, color):
  """This version assumes that the arduino can scroll the text.

  Args:
    text: text to scroll
    color: color of the text ('R', 'G', 'O')
  """
  ser.write('\r')  # Reset
  lines = text2pixels.Get8PixelsHigh(text, color)
  assert len(lines) == 8
  for line in lines:
    ser.write(line)
    ser.write('\n')


def OneColor(color):
  """Fill the LED with one color."""
  ser.write('\r')
  for unused_row in range(8):
    ser.write(color * 8)
    ser.write('\n')
  ser.flush()


def SetSpecialImage(image):
  """Set the image to one of the 'special' images."""
  ser.write('\r')  # Reset
  for row in special[image][1]:
    ser.write(row)
    ser.write('\n')
  ser.flush()


def MovingLines():
  """Moving lines animation."""
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
  """Show something at startup."""
  for color in ['G', 'R', 'O', ' ']:
    OneColor(color)
    time.sleep(0.2)

def DoKingWen():
  for hex in range(64):
    name = 'hex%d' % (hex+1)
    SetSpecialImage(name)
    time.sleep(1)

if __name__ == '__main__':
  help_info = [x for x in sorted(special.keys()) if not x.startswith('hex')]
  lines = ['  %r: %s' % (k, special[k][0]) for k in help_info]
  lines.append('  \'hexN\': Show the Kin Wen hexagram numbered N (1-64)')
  desc = ('For text you can pass some words to show.  '
          'If it\'s one of the following, however it will show something '
          'special:\n%s') % '\n'.join(lines)

  parse = optparse.OptionParser('%prog [options] text\n' + desc)
  parse.add_option('-g', '--green', dest='green', action='store_true',
                   help='Show text in green')
  parse.add_option('-r', '--red', dest='red', action='store_true',
                   help='Show text in red')
  parse.add_option('-o', '--orange', dest='orange', action='store_true',
                   help='Show text in orange')
  parse.add_option('-t', '--times', dest='times', type='int',
                   help='Number of times to scroll text', default=100)
  parse.add_option('-k', '--kingwen', dest='kingwen', action='store_true',
                   help='Do the King Wen sequence.')

  options, args = parse.parse_args()

  app = text2pixels.Init()
  ser = serial.Serial('/dev/ttyUSB0', 9600)  #115200)
  WarmUp()
  if options.kingwen:
    DoKingWen()
    sys.exit(0)
  if not args:
    print 'Pass in a string'
    sys.exit(-1)
  if args[0] in special:
    SetSpecialImage(args[0])
  else:
    ch = 'G'
    if options.red:
      ch = 'R'
    elif options.orange:
      ch = 'O'
    uargs = []
    for arg in args:
      exec 'arg = u\'%s\'' % arg
      uargs.append(arg)
    print ' '.join(args)
    MovingText2(u' '.join(uargs), ch)
  ser.close()
