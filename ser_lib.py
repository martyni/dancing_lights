from hue_lib import get_lights, set_color, get_rgb, get_xy
from serial import Serial
from time import sleep
import socket
import phue
BRIGHTNESS = 1
TIMEOUT = 1 
SERIAL_PORT = "/dev/ttyUSB0"
SER = Serial(SERIAL_PORT, 9600, timeout=TIMEOUT)
def log(message):
    #pass
    #pass
    print(message)

def serial_send(string, ser=SER):
    buff = b''
    loops = 0
    while b"\n" not in buff:
          value1 = ser.readline()
          buff += value1
          loops +=1
          #log("loops " +  str(loops) + str(buff))
    read = ser.write(bytes(string,'ascii'))

def set_lights(left_color, right_color, brightness):
    rl, gl, bl = left_color
    rr, gr, br = right_color
    serial_send('{0:03d}{1:03d}{2:03d}{3:03d}{4:03d}{5:03d}\n'.format(
        int(rl * brightness),
        int(gl * brightness),
        int(bl * brightness),
        int(rr * brightness),
        int(gr * brightness),
        int(br * brightness)
        )
    )


def get_left_right_lights():
    right = None
    left  = None
    #log("Requesting lights")
    for l in get_lights():
       if "right" in l.name.lower():
          right = right or l
       if "left" in l.name.lower():
          left  = left or l
    #log(str(right) + str(left))
    return right, left

def get_color(light):
    x,y = light.xy
    br  = light.brightness 
    return get_rgb(x, y, br * BRIGHTNESS)


def make_vibrant(r, g, b):
    scale = 10
    thresh = 88
    log('{} {} {}'.format(r,g,b))
    if g < thresh and b < thresh/2:
        g = g/3
        b = b/3
    if r < thresh and g < thresh/2:
        r = r/3 
        g = g/3
    if r < thresh:
        r = 0
    if b < thresh:
        b = 0
    if g < thresh:
        g = 0
    if g > r and g > b:
        r = r/3
        b = b/2

    return r, g, b    

def main():
    total =0
    old_left = 0
    old_right = 0
    lights = right_light, left_light = get_left_right_lights()
    sleep_time = 0
    sleep_max  = 0.5
    addition = 0.01
    boring_counter = 0
    boring_max = 600
    mode = 'hue_sync'
    count=0
    try:
        while True:
            right_color = make_vibrant(*get_color(right_light))
            left_color  = make_vibrant(*get_color(left_light))
            if right_color != old_right or left_color != old_left:
                mode = 'hue_sync'
                log(' right {} left {}'.format(right_color, left_color))
                set_lights(left_color, right_color, BRIGHTNESS)
                sleep_time = 0.2
                boring_counter = 0
            else:
                log(sleep_time)
                sleep(sleep_time)
                if sleep_time < sleep_max:
                    sleep_time += addition
                if boring_counter < boring_max:
                    boring_counter += 1
                elif mode != 'random':    
                    serial_send('random\n')
                    sleep_time = 2
                    mode = 'random'
            total += 1
            old_right = tuple(right_color)
            old_left = tuple(left_color)
            count += 1
    except (socket.timeout, phue.PhueRequestTimeout) as error:
        log('telnet error: {}'.format( error))
        log('timeout')
        sleep(2)
        main() 
    except:
       serial_send('random\n')
       print('sent random')


if __name__ == "__main__":
    main()
