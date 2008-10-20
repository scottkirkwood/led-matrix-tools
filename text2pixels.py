#!/usr/bin/env python
import wx
import sys

def Init():
  """Start the app to make wxPython happy.
  You'll need to hold on to this for a long as you need to get pixels.
  Otherwise you'll get an error.
  """
  return wx.PySimpleApp()

def GetFontPixels(font, text, black, white):
  dc = wx.MemoryDC()
  bitmap = wx.EmptyBitmap(400, 80, -1)
  dc.SelectObject(bitmap)
  dc.SetFont(font)
  dc.SetBackground(wx.Brush("white", wx.SOLID))
  dc.Clear() # Uses background color
  dc.DrawText(text, 0, 0)
  w, h, descent, external_leading = dc.GetFullTextExtent(text)
  #print w, h, descent, external_leading
  ret = []
  for y in range(descent - 1, h - descent):
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
  return ret


def Get8PixelsHigh(text, color):
  """Useful for my 8x8 pixel LED matrix from sparkfun."""
  font = wx.Font(8, wx.SWISS, style=wx.NORMAL, weight=wx.BOLD)
  lines = GetFontPixels(font, text, color, ' ')
  return lines


if __name__ == "__main__":
  import optparse
  parse = optparse.OptionParser(('%prog [options] Text\n'
      ' Text can have \\u1234 style unicode escapes as well.'))
  parse.add_option('-s', '--size', dest='fsize', type='int',
      help='Font size to use in pixels', default=8)
  parse.add_option('-b', '--bold', dest='bold', action='store_true',
      help='Use bold version')
  parse.add_option('-i', '--italics', dest='italics', action='store_true',
      help='Use italics version')
  parse.add_option('-f', '--font', dest='font', default='verdana',
      help='Font to use')
  options, args = parse.parse_args()
  app = wx.PySimpleApp()
  size = (options.fsize + 5, options.fsize + 5)
  weight = wx.NORMAL
  if options.bold:
    weight = wx.BOLD
  style = wx.NORMAL
  if options.italics:
    style = wx.ITALIC
  font = wx.FontFromPixelSize(size, wx.SWISS, style=style, weight=weight)
  for arg in args:
    exec 'arg = u\'%s\'' % arg
    lines = GetFontPixels(font, arg, '#', ' ')
    for i, line in enumerate(lines):
      #sys.stdout.write('%02d: ' % (i + 1))
      sys.stdout.write(''.join(line))
      sys.stdout.write('\n')
