#!/usr/bin/python
# -*- coding: utf-8 -*-
__version__ = '0.3.0'

import threading
from time import sleep
from threading import Thread
import os

import logging
log = logging.getLogger(__name__)


class PinState(object):
    """An ultra simple pin-state object.
    Keeps track data related to each pin.
    Args:
        value: the file pointer to set/read value of pin.
        direction: the file pointer to set/read direction of the pin.
        active_now: the file pointer to set/read if the pin is active_low.
    """
    def __init__(self, value, direction, active_low):
        self.value = value
        self.direction = direction
        self.active_low = active_low

path = os.path
pjoin = os.path.join

gpio_root = '/sys/class/gpio'
gpiopath = lambda pin: os.path.join(gpio_root, 'gpio{0}'.format(pin))
_export_lock = threading.Lock()

_pyset = set

_open = dict()
FMODE = 'w+'

IN, OUT = 'in', 'out'
LOW, HIGH = 'low', 'high'


def _write(f, v):
    log.debug("writing: {0}: {1}".format(f, v))
    f.write(str(v))
    f.flush()


def _read(f):
    log.debug("Reading: {0}".format(f))
    f.seek(0)
    return f.read().strip()


def _verify(function):
    """decorator to ensure pin is properly set up"""
    # @functools.wraps
    def wrapped(pin, *args, **kwargs):
        pin = int(pin)
        if pin not in _open:
            ppath = gpiopath(pin)
            if not os.path.exists(ppath):
                log.debug("Creating Pin {0}".format(pin))
                with _export_lock:
                    with open(pjoin(gpio_root, 'export'), 'w') as f:
                        _write(f, pin)
            value, direction, active_low = None, None, None
            try:
                value = open(pjoin(ppath, 'value'), FMODE)
                direction = open(pjoin(ppath, 'direction'), FMODE)
                active_low = open(pjoin(ppath, 'active_low'), FMODE)
            except Exception as e:
                if value: value.close()
                if direction: direction.close()
                if active_low: active_low.close()
                raise e
            _open[pin] = PinState(value=value, direction=direction, active_low=active_low)
        return function(pin, *args, **kwargs)
    return wrapped


def cleanup(pin=None, assert_exists=False):
    """Cleanup the pin by closing and unexporting it.
    Args:
        pin (int, optional): either the pin to clean up or None (default).
            If None, clean up all pins.
        assert_exists: if True, raise a ValueError if the pin was not
            setup. Otherwise, this function is a NOOP.
    """
    if pin is None:
        # Take a list of keys because we will be deleting from _open
        for pin in list(_open):
            cleanup(pin)
        return
    if not isinstance(pin, int):
        raise TypeError("pin must be an int, got: {}".format(pin))

    state = _open.get(pin)
    if state is None:
        if assert_exists:
            raise ValueError("pin {} was not setup".format(pin))
        return
    state.value.close()
    state.direction.close()
    state.active_low.close()
    if os.path.exists(gpiopath(pin)):
        log.debug("Unexporting pin {0}".format(pin))
        with _export_lock:
            with open(pjoin(gpio_root, 'unexport'), 'w') as f:
                _write(f, pin)

    del _open[pin]


@_verify
def setup(pin, mode, pullup=None, initial=False, active_low=None):
    '''Setup pin with mode IN or OUT.
    Args:
        pin (int):
        mode (str): use either gpio.OUT or gpio.IN
        pullup (None): rpio compatibility. If anything but None, raises
            value Error
        initial (bool, optional): Initial pin value. Default is False
        active_low (bool, optional): Set the pin to active low. Default
            is None which leaves things as configured in sysfs
    '''
    if pullup is not None:
        raise ValueError("sysfs does not support pullups")

    if mode not in (IN, OUT, LOW, HIGH):
        raise ValueError(mode)

    if active_low is not None:
        if not isinstance(active_low, bool):
            raise ValueError("active_low argument must be True or False")
        log.debug("Set active_low {0}: {1}".format(pin, active_low))
        f_active_low = _open[pin].active_low
        _write(f_active_low, int(active_low))

    log.debug("Setup {0}: {1}".format(pin, mode))
    f_direction = _open[pin].direction
    _write(f_direction, mode)
    if mode == OUT:
        if initial:
            set(pin, 1)
        else:
            set(pin, 0)


@_verify
def mode(pin):
    '''get the pin mode
    Returns:
        str: "in" or "out"
    '''
    f = _open[pin].direction
    return _read(f)


@_verify
def read(pin):
    '''read the pin value
    Returns:
        bool: 0 or 1
    '''
    f = _open[pin].value
    out = int(_read(f))
    log.debug("Read {0}: {1}".format(pin, out))
    return out


@_verify
def set(pin, value):
    '''set the pin value to 0 or 1'''
    if value is LOW:
        value = 0
    value = int(bool(value))
    log.debug("Write {0}: {1}".format(pin, value))
    f = _open[pin].value
    _write(f, value)


@_verify
def input(pin):
    '''read the pin. Same as read'''
    return read(pin)


@_verify
def output(pin, value):
    '''set the pin. Same as set'''
    return set(pin, value)


def setwarnings(value):
    '''exists for rpio compatibility'''
    pass


def setmode(value):
    '''exists for rpio compatibility'''
    pass

BCM = None  # rpio compatibility
















cleanup()
Data = setup(45,OUT,None,False,None)
Clk = setup(46,OUT,None,False,None)


def clkbegin():
    clkstate = LOW
    count = 0
    for i in range(64):
        count = (count+1) % 2
        print(count)
        if count == 1:
            clkstate = HIGH
        else:
            clkstate = LOW
        set(45,clkstate)
        sleep(.1)

green = ["00000000","00000000","00000000","00000000",
        "10010000","00000000","01110000","00000000",
        "11111111","11111111","11111111","11111111"]

red = ["00000000","00000000","00000000","00000000",
        "10010000","00000000","00000000","01110000",
        "11111111","11111111","11111111","11111111"]

blue = ["00000000","00000000","00000000","00000000",
        "10010000","01110000","00000000","00000000",
        "11111111","11111111","11111111","11111111"]

purple = ["00000000","00000000","00000000","00000000",
        "10010000","01110000","00000000","00110000",
        "11111111","11111111","11111111","11111111"]

cyan = ["00000000","00000000","00000000","00000000",
        "10010000","00110000","00110000","00000000",
        "11111111","11111111","11111111","11111111"]

def defaultcolor(data):
    
    data = ["00000000","00000000","00000000","00000000",
            "10010000","00000000","01110000","00000000",
            "11111111","11111111","11111111","11111111"]

    datastate = LOW
    clkstate = LOW

    for i in range(8):
        for j in range(8):

            set(45,HIGH)
            if data[i][j] == "1":
                datastate = HIGH
                set(46,datastate)
                
                
            else:
                datastate = LOW
                set(46,datastate)
            
            set(45,LOW)
    set(46,LOW)
    set(45,LOW)

def scanningcolor():
    
    data = ["00000000","00000000","00000000","00000000",
            "10010000","01000000","01100000","00000000",
            "11111111","11111111","11111111","11111111"]

    datastate = LOW
    clkstate = LOW
    for z in range(2):
        for i in range(8):
            for j in range(8):

                set(45,HIGH)
                if data[i][j] == "1":
                    datastate = HIGH
                    set(46,datastate)
                    
                    
                else:
                    datastate = LOW
                    set(46,datastate)
                
                set(45,LOW)
    set(46,LOW)
    set(45,LOW)

def disconnectedcolor():
    
    data = ["00000000","00000000","00000000","00000000",
            "10010000","01100000","00000000","00000000",
            "11111111","11111111","11111111","11111111"]

    datastate = LOW
    clkstate = LOW
    for z in range(2):
        for i in range(8):
            for j in range(8):

                set(45,HIGH)
                if data[i][j] == "1":
                    datastate = HIGH
                    set(46,datastate)
                    
                    
                else:
                    datastate = LOW
                    set(46,datastate)
                
                set(45,LOW)
    set(46,LOW)
    set(45,LOW)

def pushbuttonkeepcolor():
    
    data = ["00000000","00000000","00000000","00000000",
            "10010000","00110000","11000000","00000000",
            "11111111","11111111","11111111","11111111"]

    datastate = LOW
    clkstate = LOW
    for z in range(2):
        for i in range(8):
            for j in range(8):

                set(45,HIGH)
                if data[i][j] == "1":
                    datastate = HIGH
                    set(46,datastate)
                    
                    
                else:
                    datastate = LOW
                    set(46,datastate)
                
                set(45,LOW)
    set(46,LOW)
    set(45,LOW)

def bullseyecolor():
    
    data = ["00000000","00000000","00000000","00000000",
            "10010000","00000000","11111111","00001000",
            "11111111","11111111","11111111","11111111"]

    datastate = LOW
    clkstate = LOW
    for z in range(2):
        for i in range(8):
            for j in range(8):

                set(45,HIGH)
                if data[i][j] == "1":
                    datastate = HIGH
                    set(46,datastate)
                    
                    
                else:
                    datastate = LOW
                    set(46,datastate)
                
                set(45,LOW)
    set(46,LOW)
    set(45,LOW)

def bullseyecolorfade():
    
    data = ["00000000","00000000","00000000","00000000",
            "10010000","00000000","11111100","00111000",
            "11111111","11111111","11111111","11111111"]

    datastate = LOW
    clkstate = LOW
    for z in range(2):
        for i in range(8):
            for j in range(8):

                set(45,HIGH)
                if data[i][j] == "1":
                    datastate = HIGH
                    set(46,datastate)
                    
                    
                else:
                    datastate = LOW
                    set(46,datastate)
                
                set(45,LOW)
    set(46,LOW)
    set(45,LOW)

def disconnectedWAcolor():
    print("Disconnected WA Color")
    data = ["00000000","00000000","00000000","00000000",
            "10010000","00100101","00000000","00010001",
            "11111111","11111111","11111111","11111111"]

    for x in range(32):

        datastate = LOW
        clkstate = LOW
        for z in range(2):
             for i in range(8):
                 for j in range(8):

                    set(45,HIGH)

                    if data[i][j] == "1":
                        datastate = HIGH
                        set(46,datastate)
                            
                            
                    else:
                        datastate = LOW
                        set(46,datastate)

                    set(45,LOW)

        redshift = int(data[5],2) + 5
        greenshift = int(data[7],2) - 1 

        redshiftedformat = format(redshift,"08b")
        greenshiftedformat = format(greenshift,"08b")
        data[5] = redshiftedformat
        if greenshift > 0:
            data[7] = greenshiftedformat

def disconnectedPBcolor():
    print("Disconnected PB Color")
    data = ["00000000","00000000","00000000","00000000",
            "10010000","00010001","00100101","00000000",
            "11111111","11111111","11111111","11111111"]

    for x in range(32):
        datastate = LOW
        clkstate = LOW
        for z in range(2):
             for i in range(8):
                 for j in range(8):

                    set(45,HIGH)

                    if data[i][j] == "1":
                        datastate = HIGH
                        set(46,datastate)
                            
                            
                    else:
                        datastate = LOW
                        set(46,datastate)

                    set(45,LOW)

        redshift = int(data[5],2) + 6
        blueshift = int(data[6],2) - 1 

        redshiftedformat = format(redshift,"08b")
        blueshiftedformat = format(blueshift,"08b")
        data[6] = blueshiftedformat
        if redshift > 0:
            data[5] = redshiftedformat

def webunavailablecolor():
    print("Web Unavailable Color")
    data = ["00000000","00000000","00000000","00000000",
            "10010000","11000000","00000000","00110000",
            "11111111","11111111","11111111","11111111"]
    for y in range (3):
        for x in range(32):
            datastate = LOW
            clkstate = LOW
            for z in range(2):
                for i in range(8):
                    for j in range(8):

                        set(45,HIGH)
                        if data[i][j] == "1":
                            datastate = HIGH
                            set(46,datastate)
                            
                            
                        else:
                            datastate = LOW
                            set(46,datastate)
                        
                        set(45,LOW)

            if y == 1 or y ==3:
                redshift = int(data[5],2) + 5
                greenshift = int(data[7],2) + 1 
            else:
                redshift = int(data[5],2) - 5
                greenshift = int(data[7],2) - 1 

            redshiftedformat = format(redshift,"08b")
            greenshiftedformat = format(greenshift,"08b")
            data[5] = redshiftedformat
            data[7] = greenshiftedformat
                
        set(46,LOW)
        set(45,LOW)

def pushbuttoncolor():
    print("PushButtonColor")
    data = ["00000000","00000000","00000000","00000000",
            "10010000","00110000","11000000","00000000",
            "11111111","11111111","11111111","11111111"]
    for y in range (3):
        for x in range(32):
            datastate = LOW
            clkstate = LOW
            for z in range(2):
                for i in range(8):
                    for j in range(8):

                        set(45,HIGH)
                        if data[i][j] == "1":
                            datastate = HIGH
                            set(46,datastate)
                            
                            
                        else:
                            datastate = LOW
                            set(46,datastate)
                        
                        set(45,LOW)

            if y == 1 or y ==3:
                redshift = int(data[5],2) + 1
                blueshift = int(data[6],2) + 5 
            else:
                redshift = int(data[5],2) - 1
                blueshift = int(data[6],2) - 5 
            redshiftedformat = format(redshift,"08b")
            blueshiftedformat = format(blueshift,"08b")
            data[5] = redshiftedformat
            data[6] = blueshiftedformat
                
        set(46,LOW)
        set(45,LOW)






def connectedcolor():
    
    data = ["00000000","00000000","00000000","00000000",
            "10010000","00000000","00000000","11001011",
            "11111111","11111111","11111111","11111111"]
  
    datastate = LOW
    clkstate = LOW

    for z in range(2):
        for i in range(8):
            for j in range(8):

                set(45,HIGH)
                if data[i][j] == "1":
                    datastate = HIGH
                    set(46,datastate)
                    
                    
                else:
                    datastate = LOW
                    set(46,datastate)
                
                set(45,LOW)
    set(46,LOW)
    set(45,LOW)

def connectedWAcolor():
    print("Connected WA Color")
    data = ["00000000","00000000","00000000","00000000",
            "10010000","00100101","00000000","00010001",
            "11111111","11111111","11111111","11111111"]

    for x in range(32):
        datastate = LOW
        clkstate = LOW
        for z in range(2):
             for i in range(8):
                 for j in range(8):

                    set(45,HIGH)

                    if data[i][j] == "1":
                        datastate = HIGH
                        set(46,datastate)
                            
                            
                    else:
                        datastate = LOW
                        set(46,datastate)

                    set(45,LOW)

        redshift = int(data[5],2) -2
        greenshift = int(data[7],2) + 6 
        redshiftedformat = format(redshift,"08b")
        greenshiftedformat = format(greenshift,"08b")
        data[7] = greenshiftedformat
        if redshift > 0:
            data[5] = redshiftedformat


def connectedPBcolor():
    print("Connected PB Color")
    data = ["00000000","00000000","00000000","00000000",
            "10010000","00010000","00100000","00000000",
            "11111111","11111111","11111111","11111111"]

    for x in range(36):
        datastate = LOW
        clkstate = LOW
        for z in range(2):
             for i in range(8):
                 for j in range(8):

                    set(45,HIGH)

                    if data[i][j] == "1":
                        datastate = HIGH
                        set(46,datastate)
                            
                            
                    else:
                        datastate = LOW
                        set(46,datastate)

                    set(45,LOW)

        redshift = int(data[5],2) -4
        blueshift = int(data[6],2) -4
        redshiftedformat = format(redshift,"08b")
        blueshiftedformat = format(blueshift,"08b")

        if blueshift > 0:
            data[6] = blueshiftedformat
        if redshift > 0:
            data[5] = redshiftedformat
        if redshift == 0:
            greenshift = int(data[7],2) + 6 
            greenshiftedformat = format(greenshift,"08b")
            data[7] = greenshiftedformat


def changecolor(data):

    datastate = LOW
    clkstate = LOW

    for i in range(8):
        for j in range(8):

            set(45,HIGH)
            if data[i][j] == "1":
                datastate = HIGH
                set(46,datastate)
                
                
            else:
                datastate = LOW
                set(46,datastate)
            
            set(45,LOW)
            

# sleep(.25)
# datagreen(purple)
# datagreen(purple)
# sleep(.25)
# datagreen(blue)
# datagreen(blue)
# sleep(.25)
# datagreen(cyan)
# datagreen(cyan)
# sleep(.25)
# datagreen(green)
# datagreen(green)
# sleep(.25)
# disconnectedcolor()

# sleep(2)
# webunavailablecolor()
# connectedWAcolor()
# sleep(2)
# connectedcolor()

# sleep(2)
# pushbuttoncolor()
# connectedPBcolor()
# connectedcolor()
# set(46,LOW)
# set(45,LOW)


#set(150,LOW)

# t1 = Thread(target=clkbegin)
# threads = [t1]
# t2 = Thread(target=datagreen)
# threads += [t2]


# t1.start()
# t2.start()

