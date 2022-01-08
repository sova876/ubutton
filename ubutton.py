import time
import machine

class ubutton(object):
    def __init__(self, pin, cb_short=None, shrt_args=None, cb_long=None, lng_args=None, irq = None,
                       bounce_time=50, long_time=500, click_timeout = 500, downtime = 2000):
        
        self.pin = pin
        self.bounce_time = bounce_time
        self.long_time = long_time
        self.click_timeout = click_timeout
        self.downtime = downtime

        self.handled = False
        self.btn_tmr = 0
        self.btn_flag = 0
        self.hold_flag = False
        self.counter = 0

        # if counting:
        #     self.cbs_args = kwargs

        if cb_short:
            if not callable(cb_short):
                raise TypeError("'cb_short' must be a callable")
            else: 
                self.cb_short = cb_short
                self.short_args=shrt_args
        
        if cb_long:
            if not callable(cb_long):
                raise TypeError("'cb_long' must be a callable")
            else: 
                self.cb_long = cb_long
                self.long_args = lng_args

        if irq:
            self.pin.irq(handler=self.cb_interrupt, trigger=irq)
    
    # def _cb_short(self):
    #     self.cb_short(*self.short_args)
    
    # def _cb_long(self):
    #     self.cb_long(*self.long_args)

    def handler(self):

        btn_state = self.pin.value()
        cur_ticks = time.ticks_ms()
        ticks_diff = time.ticks_diff(cur_ticks, self.btn_tmr)

        if btn_state and not self.btn_flag and ticks_diff > self.bounce_time:
            self.btn_flag = 1
            print("Pressed!")
            self.btn_tmr = cur_ticks           
        elif not btn_state and self.btn_flag and ticks_diff > self.bounce_time:
            self.btn_flag = 0
            self.counter += 1
            self.btn_tmr = cur_ticks
            print("Released!")
        elif btn_state and self.btn_flag and ticks_diff > self.long_time:
            self.hold_flag = True
            self.btn_tmr = cur_ticks
            print("Hold!")
        
        if not btn_state and not self.btn_flag and ticks_diff > self.click_timeout and self.counter != 0:
            print("Counter:", self.counter)
            self.counter = 0
            if self.hold_flag:
                print("Long press")
            else: 
                print("Short press")
                # self._cb_short()
                self.cb_short(*self.short_args)
            self.handled = True
        elif ticks_diff > self.downtime:
            print("Downtime!")
            self.handled = True

    def cb_interrupt(self, pin):

        if self.pin.value():
            self.handled = False
        else: self.handled = True
        self.btn_tmr = time.ticks_ms()
        self.btn_flag = 0
        self.hold_flag = False
        self.counter = 0

        while not self.handled:
            self.handler()
            # print("Handled: ", self.handled)