SparkFun LED matrix tools to draw text across the matrix.

![http://led-matrix-tools.googlecode.com/svn/trunk/completed.jpg](http://led-matrix-tools.googlecode.com/svn/trunk/completed.jpg)

Requirements:
  * [Python](http://www.python.org/)
  * [wxPython](http://www.wxpython.org/)
  * [pySerial](http://pyserial.wiki.sourceforge.net/pySerial)

I use wxPython to get pixel representations of text. This is quite useful on it's own and is offered as a separate package (text2pixels.py).

```
$ ./text2pixels.py --help
Usage: text2pixels.py [options] Text
 Text can have \u1234 style unicode escapes as well.

Options:
  -h, --help            show this help message and exit
  -s FSIZE, --size=FSIZE
                        Font size to use in pixels
  -b, --bold            Use bold version
  -i, --italics         Use italics version
  -f FONT, --font=FONT  Font to use
```


ex. output the Airplane Unicode character U+2708 ✈

```
$ ./text2pixels.py --size 19 \\u2708
      ##         
       ###       
       ##        
       ####      
  #     ###      
  #     ####     
  ############## 
  ##    ####     
  #     ###      
        ###      
       ###       
       ###       
      ##         
      #        
```

This is a great way to get an image since Unicode has a [ton of symbols](http://en.wikipedia.org/wiki/Unicode_Symbols).

```
$ ./text2pixels.py --size 18 --bold Arduino
     #####                       ###                  ###                             
     #####                       ###                  ###                             
    #######                      ###                  ###                             
    ### ###                      ###                                                  
    ### ###     ###  ###   ####  ###    ###    ###    ###    ###  ###        #####    
   ###   ###    ########  ##########    ###    ###    ###    #########     #########  
   ###   ###    ####      ###   ####    ###    ###    ###    ####  ####    ###   ###  
  ####   ####   ###      ###     ###    ###    ###    ###    ###    ###   ###     ### 
  ###     ###   ###      ###     ###    ###    ###    ###    ###    ###   ###     ### 
  ###########   ###      ###     ###    ###    ###    ###    ###    ###   ###     ### 
 #############  ###      ###     ###    ###    ###    ###    ###    ###   ###     ### 
 ###       ###  ###       ###   ####    ####  ####    ###    ###    ###    ###   ###  
 ###       ###  ###       ##########     #########    ###    ###    ###    #########  
###         ### ###        ####  ###      ###  ###    ###    ###    ###      #####    
```

```
$ ./text2pixels.py --help           
Usage: text2pixels.py [options] Text
 Text can have \u1234 style unicode escapes as well.

Options:
  -h, --help            show this help message and exit
  -s FSIZE, --size=FSIZE
                        Font size to use in pixels
  -b, --bold            Use bold version
  -i, --italics         Use italics version
  -f FONT, --font=FONT  Font to use
  -g, --grid            Show the column, row numbers
  -c CHAR, --char=CHAR  Character to use
  -p, --python          Output as lines of python
  --kingwen             Output King Wen sequence

```
But the main purpose of this code is to be able to output to the SparkFun
[LED matrix](http://www.sparkfun.com/commerce/product_info.php?products_id=759).

Example 1: Here's how to have Hello scrolled across the screen:
```
$ ./matrix_led.py --green Hello
```
![http://led-matrix-tools.googlecode.com/svn/trunk/hello.jpg](http://led-matrix-tools.googlecode.com/svn/trunk/hello.jpg)

Example 2: How to show the smilie face.
```
$ ./matrix_led.py smilie
```
![http://led-matrix-tools.googlecode.com/svn/trunk/smilie.jpg](http://led-matrix-tools.googlecode.com/svn/trunk/smilie.jpg)

Example 3: And the frownie face
```
$  ./matrix_led.py frownie
```
![http://led-matrix-tools.googlecode.com/svn/trunk/frownie.jpg](http://led-matrix-tools.googlecode.com/svn/trunk/frownie.jpg)

Example 3: Show the +- symbol (unicode 00B1 or ±)
```
$  ./matrix_led.py -g \\u00B1
```
![http://led-matrix-tools.googlecode.com/svn/trunk/plusminus.jpg](http://led-matrix-tools.googlecode.com/svn/trunk/plusminus.jpg)
