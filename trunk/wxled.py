#!/usr/bin/python

import wx


class MyFrame(wx.Frame):
  def __init__(self, parent, id, title, width=8, height=8):
    size = 35
    self.width = width
    self.height = height
    wx.Frame.__init__(self, parent, id, title, (-1, -1), 
                      wx.Size(size*width + 5, size*height + 5))
    panel = wx.Panel(self, -1)
    vert = wx.BoxSizer(wx.VERTICAL)
    imageEmpty = 'empty-circle.png'
    imageRed = 'red-circle.png'
    imageGreen = 'green-circle.png'
    imageOrange = 'orange-circle.png'
    self.states = [' ' for i in range(width*height)]
    self.startId = 100
    self.imageEmpty = wx.Image(imageEmpty, wx.BITMAP_TYPE_ANY).ConvertToBitmap()
    self.imageRed = wx.Image(imageRed, wx.BITMAP_TYPE_ANY).ConvertToBitmap()
    self.imageGreen = wx.Image(imageGreen, wx.BITMAP_TYPE_ANY).ConvertToBitmap()
    self.imageOrange = wx.Image(imageOrange, wx.BITMAP_TYPE_ANY).ConvertToBitmap()
    for row in range(height):
      horz = wx.BoxSizer(wx.HORIZONTAL)
      for col in range(width):
        buttonId = self.startId + row * width + col
        off = 15
        button = wx.BitmapButton(panel, id=buttonId, bitmap=self.imageEmpty,
          size=(self.imageEmpty.GetWidth() + off, self.imageEmpty.GetHeight() + off))
        horz.Add(button, 1)
        button.Bind(wx.EVT_BUTTON, self.buttonClick)
      vert.Add(horz)

    panel.SetSizer(vert)
    self.Center()
    self.Bind(wx.EVT_CLOSE, self.onClose)

  def buttonClick(self, event):
    curId = event.GetId() - self.startId
    state = self.states[curId]
    stateTransition = { ' ':'R', 'R':'G', 'G':'O', 'O':' ' }
    state = stateTransition[state]
    imageToState = {
      ' ' : self.imageEmpty,
      'R' : self.imageRed,
      'G' : self.imageGreen,
      'O' : self.imageOrange,
    }
    self.states[curId] = state
    event.GetEventObject().SetBitmapLabel(imageToState[state])

  def onClose(self, evt):
    lines = []
    for row in range(self.height):
      line = []
      for col in range(self.width):
        line.append(self.states[row * self.width + col])
      lines.append(''.join(line))
   
    for line in lines:
      print '    "%s",' % line
    self.Destroy()

class MyApp(wx.App):
  def OnInit(self):
    frame = MyFrame(None, -1, 'LED Grid', 8, 8)
    frame.Show(True)
    return True

if __name__ == '__main__':
  app = MyApp(0)
  app.MainLoop()
