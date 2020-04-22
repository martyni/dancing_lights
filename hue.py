import os
from rgbxy import ColorHelper, Converter
from random import randint
from time import sleep
from datetime import datetime, timedelta
from beautifulhue.api import Bridge
from hue_lib import get
from serial import Serial
from autoyaml import load_config
import request
from pprint import pprint

config = load_config("dancing_lights")
bridge = Bridge(device=config['device'], user=config['user'])
LOG_LEVEL = "verbose"

def change_lights(colour2, colour1):
    resource = {
    'which':2,
    'data':{
        'state':{'on':True,'xy':colour1}
    }
    }
    bridge.light.update(resource)
    resource = {
    'which':1,
    'data':{
        'state':{'on':True,'xy': colour2}
    }
    }
    bridge.light.update(resource)

def log(message, level="log"):
    if LOG_LEVEL=="verbose" and level == "log" or level == "error":
        pprint({datetime.utcnow(): message})
    elif LOG_LEVEL=="error" and level == "error":
        pprint({datetime.utcnow(): message})

def get_hue_light_colours(left_light, right_light):
    resource = {'which':'all'}
    info =  bridge.light.get(resource)
    ob1 = info['resource'][left_light].get('state')['xy'] +  [ info['resource'][left_light].get('state')['bri'] ]
    ob2 = info['resource'][right_light].get('state')['xy'] + [ info['resource'][right_light].get('state')['bri'] ]
    log(ob1)
    log(ob2)
    '''
    resource = {
      'which':2
    }
    ob1 = bridge.light.get(resource)['resource'].get('state')['xy'] + [ bridge.light.get(resource)['resource'].get('state')['bri'] ]
    resource = {
      'which':1
    }
    ob2 = bridge.light.get(resource)['resource'].get('state')['xy'] + [ bridge.light.get(resource)['resource'].get('state')['bri'] ]
    '''
    return ob1, ob2


def return_xy(r, g, b):
    r = int(r)
    g = int(g)
    b = int(b)
    return converter.rgb_to_xy(r, g, b)

resource = {'which':'all'}
info = bridge.light.get(resource)['resource']

helper = ColorHelper()
converter = Converter()
helper.get_rgb_from_xy_and_brightness(0.1056, 0.0065, 254/255.0)
x1, y1 = info[0]['state']['xy']
x2, y2 = info[2]['state']['xy']
b1 = info[0]['state']['bri']
b2 = info[2]['state']['bri']

for i in 0,1,2:
    if info[i]['name'] == "Left living room":
        left_light = i
        log("left is " + str(i))
    elif info[i]['name'] == "Right living room":
        right_light = i
        log("right is " +  str(i))
log(str(helper.get_rgb_from_xy_and_brightness(x1,y1,b1)))
log(str(helper.get_rgb_from_xy_and_brightness(x2,y2,b2)))

def main(serial_port='/dev/ttyACM0', limit=1, timeout=5):
   #try:
   skip_read = False
   ser = Serial(serial_port, 9600,timeout=timeout)
   old_serial_cmd = '' 
   wait = 0
   multiplier = 2
   time_since_last_wait = datetime.utcnow()
   while True:
       buff = ""
       #colours = r1, g1, b1, r2, g2, b2 = (randint(0,255), randint(0,255), randint(0,255), randint(0,255), randint(0,255) ,randint(0,255))
       log("Asking bridge")
       l1, l2 = get_hue_light_colours(left_light, right_light)
       '''
       l2[2] = l2[2] -15 if l2[2] > 30 else 1
       l1[2] = l1[2] -15 if l1[2] > 30 else 1
       #print l2, l1
       l1[2] = l1[2] - 50  if l1[2] >50 else l1[2]
       l2[2] = l2[2] - 50  if l2[2] >50 else l2[2]
       '''
       br1= float(l1[2])/255
       br2 =float(l2[2])/255
       colours = helper.get_rgb_from_xy_and_brightness(*l1) + helper.get_rgb_from_xy_and_brightness(*l2) 
       r1 = int(colours[0]  * br1) if int(colours[0]  * br1) > limit else limit 
       g1 = int(colours[1]  * br1) if int(colours[1]  * br1) > limit else limit
       b1 = int(colours[2]  * br1) if int(colours[2]  * br1) > limit else limit
       r2 = int(colours[3]  * br2) if int(colours[3]  * br2) > limit else limit
       g2 = int(colours[4]  * br2) if int(colours[4]  * br2) > limit else limit
       b2 = int(colours[5]  * br2) if int(colours[5]  * br2) > limit else limit
       loops = 0
       while "\n" not in buff:
          value1 = ser.read()
          buff += value1
          loops +=1
          log("loops " +  str(loops))   
       log("loops " +  str(loops))   
       #if len(buff.split()) > 1:
       #r1, g1, b1, r2, g2, b2 = buff.split()
       #light_1 = return_xy(r1, g1, b1)
       #light_2 =  return_xy(r2, g2, b2)
       #print light_1
       #print light_2
       #else:
       #   print buff
       exists = os.path.isfile('/etc/dl/random')
       before = datetime.utcnow()
       if exists and not skip_read:
          serial_cmd = 'random\n'
          wait = 0.1
          ser.write(serial_cmd)
       else:
          serial_cmd = '{0:03d}{1:03d}{2:03d}{3:03d}{4:03d}{5:03d}\n'.format(r1, g1, b1, r2, g2, b2)
          log("{}:{}:{}".format(old_serial_cmd, serial_cmd, old_serial_cmd == serial_cmd))
          if old_serial_cmd == serial_cmd and wait < 4:
              wait += 0.01
          else:
              wait = 0.2
              log("Sending " + serial_cmd)
       ser.write(serial_cmd)
       after = datetime.utcnow()
       diff = after - before
       if diff.seconds > 2:
           ser.close()
           ser = Serial(serial_port, 9600,timeout=timeout)
           last_break_time = datetime.utcnow() - time_since_last_wait 
           log("Reseting connection", level="error")
           log(last_break_time, level="error")
           time_since_last_wait = datetime.utcnow() 

       log("Sent \nWaiting: " + str(wait))
       #change_lights( light_1, light_2)

       old_serial_cmd = str(serial_cmd)
       sleep(wait)
   #except Exception as e:
   #   print datetime.utcnow(), ": crashed", e
   #   main()
if __name__ == "__main__":
   main()
