#!/usr/bin/env python
import serial
import time
import text2pixels


special = {
  'smile' : [
     '  GGGG  ',
     ' G    G ',
     'G G  G G',
     'G      G',
     'G G  G G',
     'G  GG  G',
     ' G    G ',
     '  GGGG  ', 
  ],
  'smilie' : [
     ' GG  GG ',
     ' GG  GG ',
     '        ',
     '   GG   ',
     'G  GG  G',
     'GG    GG',
     'GGGGGGGG',
     '  GGGG  ', 
  ],
  'frownie' : [
     ' RR  RR ',
     ' RR  RR ',
     '        ',
     '   RR   ',
     '        ',
     ' RRRRRR ',
     'RRRRRRRR',
     'R      R', 
  ],
  'sad' : [
     '  RRRR  ',
     ' R    R ',
     'R R  R R',
     'R      R',
     'R  RR  R',
     'R R  R R',
     ' R    R ',
     '  RRRR  ', 
  ]
}

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


def MovingText(text, color, times=1):
  lines = text2pixels.Get8PixelsHigh(text, color)
  for x in range(times):
    ScrollingInfo(lines, speed=0.1, leadin=0, leadout=0)


def OneColor(color):
  ser.write('\n')
  ser.write(color * 64)
  ser.flush()


def SetImage(image):
  for row in special[image]:
    ser.write(row)
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
  parse = optparse.OptionParser()
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
    MovingText(' '.join(args), ch, options.times)
  ser.close()
