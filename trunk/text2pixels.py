#!/usr/bin/env python
"""Return a string of text as pixels where each pixel is a character.

You can pass unicode characters by passing \u0123, for example.
"""

import optparse
import sys
import wx


def Init():
  """Start the app to make wxPython happy.

  You'll need to hold on to this for a long as you need to get pixels.
  Otherwise you'll get an error.
  """
  return wx.PySimpleApp()


def GetFontPixels(font, text, black, white):
  """Draw the text and get the pixels."""

  dc = wx.MemoryDC()
  bitmap = wx.EmptyBitmap(400, 80, -1)
  dc.SelectObject(bitmap)
  dc.SetFont(font)
  dc.SetBackground(wx.Brush('white', wx.SOLID))
  dc.Clear()  # Uses background color
  dc.DrawText(text, 0, 0)
  w, h, descent, unused_ext_leading = dc.GetFullTextExtent(text)
  ret = []
  for y in range(descent - 1, h):
    line = []
    for x in range(w):
      col = dc.GetPixel(x, y)
      if col.Red() > 128:
        line.append(white)
      else:
        line.append(black)
    ret.append(''.join(line))

  # Clear the memory
  dc.SelectObject(wx.NullBitmap)

  # Strip trailing blank lines
  while True:
    if ret[-1].strip(white):
      break
    ret = ret[:-1]
  return ret


def Get8PixelsHigh(text, color):
  """Useful for my 8x8 pixel LED matrix from sparkfun."""
  font = wx.Font(8, wx.SWISS, style=wx.NORMAL, weight=wx.BOLD)
  lines = GetFontPixels(font, text, color, ' ')
  return lines


def Indent(indents):
  """Indent X number of indents."""
  return ' ' * (2 * indents)


def KingWen(font, hexid):
  """Output the a King Wen char.

  The unicode characters are from \u4DC0 - \u4DFF
  """

  ret = []
  ch = 0x4DC0 + hexid - 1
  exec 'char = u\'\u%4x\'' % ch
  lines = GetFontPixels(font, char, 'R', ' ')
  ret.append(' ' * 8)
  for line in lines[1::2]:
    hex_chars = ''.join(line[1:-1])
    ret.append(hex_chars[1:-1])
  ret.append(' ' * 8)
  return ret


def DoKingWen():
  """Do the King Wen sequence."""
  names = [
      'Creative Power', 'Natural Response', 'Difficult Beginnings',
      'Inexperience', 'Calculated Waiting', 'Conflict', 'Collective Force',
      'Unity', 'Restrained', 'Conduct', 'Prospering', 'Stagnation',
      'Community', 'Sovereignty', 'Moderation', 'Harmonize', 'Adapting',
      'Repair', 'Promotion', 'Contemplating', 'Reform', 'Grace',
      'Deterioration', 'Returning', 'Innocence', 'Potential Energy',
      'Nourishing', 'Critical Mass', 'Danger', 'Synergy', 'Attraction',
      'Continuing', 'Retreat', 'Great Power', 'Progress', 'Censorship',
      'Family', 'Contradiction', 'Obstacles', 'Liberation', 'Decline',
      'Benefit', 'Resolution', 'Temptation', 'Assembling', 'Advancement',
      'Adversity', 'The Source', 'Revolution', 'Cosmic Order', 'Shocking',
      'Meditation', 'Developing', 'Subordinate', 'Zenith', 'Traveling',
      'Penetrating Influence', 'Encouraging', 'Reuniting', 'Limitations',
      'Insight', 'Conscientiousness', 'After the End', 'Before the End'
  ]

  font = wx.FontFromPixelSize((17, 17), wx.SWISS,
                              style=wx.NORMAL, weight=wx.NORMAL)
  for ch in range(1, 65):
    print '%s\'hex%d\': (\'King Wen sequence %d (%s)\', [' % (Indent(2),
                                                              ch,
                                                              ch,
                                                              names[ch - 1])
    lines = KingWen(font, ch)
    assert 8 == len(lines)
    for line in lines:
      assert 8 == len(line)
      print '%s\'%s\',' % (Indent(4), line)
    print '%s]),' % Indent(2)


if __name__ == '__main__':
  parse = optparse.OptionParser(
      ('%prog [options] Text\n'
       ' Text can have \\u1234 style unicode escapes as well.'))
  parse.add_option('-s', '--size', dest='fsize', type='int',
                   help='Font size to use in pixels', default=8)
  parse.add_option('-b', '--bold', dest='bold', action='store_true',
                   help='Use bold version')
  parse.add_option('-i', '--italics', dest='italics', action='store_true',
                   help='Use italics version')
  parse.add_option('-f', '--font', dest='font', default='',
                   help='Font to use')
  parse.add_option('-g', '--grid', dest='grid', action='store_true',
                   default=False, help='Show the column, row numbers')
  parse.add_option('-c', '--char', dest='char', default='#',
                   help='Character to use')
  parse.add_option('-p', '--python', dest='python', action='store_true',
                   default=False,
                   help='Output as lines of python')
  parse.add_option('--kingwen', dest='kingwen', action='store_true',
                   default=False, help='Output King Wen sequence')
  options, args = parse.parse_args()
  app = wx.PySimpleApp()
  size = (options.fsize + 5, options.fsize + 5)
  weight = wx.NORMAL
  if options.bold:
    weight = wx.BOLD
  style = wx.NORMAL
  if options.italics:
    style = wx.ITALIC
  if options.font:
    afont = wx.FontFromPixelSize(size, wx.SWISS, style=style, weight=weight,
                                 name=options.font)
  else:
    afont = wx.FontFromPixelSize(size, wx.SWISS, style=style, weight=weight)

  if options.kingwen:
    DoKingWen()
    sys.exit(0)

  for arg in args:
    exec 'arg = u\'%s\'' % arg
    lines = GetFontPixels(afont, arg, options.char, ' ')
    if options.grid:
      line = '   '
      for col in range(len(lines[0])):
        line += '%d' % ((col + 1) % 10)
      print line

    for i, line in enumerate(lines):
      if options.grid:
        sys.stdout.write('%02d: ' % (i + 1))
      if options.python:
        sys.stdout.write('%s\'' % (Indent(4)))
      sys.stdout.write(''.join(line))
      if options.python:
        sys.stdout.write('\',')
      sys.stdout.write('\n')
