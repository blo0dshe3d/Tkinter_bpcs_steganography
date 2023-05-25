* This Repository only converting console to UI of the original code that can be found at https://github.com/mobeets/bpcs

- Step

# TKinter & Bpcs steganography

python 2.7.15 / 14 < requirement<br/>
pip requirement :exclamation:<br/>

pillow<br/>
bpcs<br/>
numpy<br/>
matplotlib<br/>

>act_on_image < replace import image > from PIL import image

### > INCASE OF get_n_message_grids ERROR

> take a look at line 148 and<br/>

 try:<br/>
 ... <br/>
 except Exception as error:<br/>
     print('caught error : ' + repr(error))<br/>

### update 2020-20
use import __builtin__ at bpcs_steg_capacity to printout (nbytes) value <br/>
