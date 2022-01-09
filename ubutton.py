import time
import machine

class ubutton(object):
    def __init__(self, pin, irq=None,
                       bounce_time=50, long_time=500, click_timeout = 500, downtime = 2000, **kwargs):
        
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

        self.callbacks = kwargs['cbs']
        self.cbs_args = kwargs["cb_args"]
        keys = self.callbacks.keys()
        max_clicks = max([key for key in keys if type(key) is int]) + 1
        [self.callbacks.setdefault(key, lambda *a, **k: None) for key in range(1, max_clicks)]
        [self.cbs_args.setdefault(key, []) for key in range(1, max_clicks)]
        
        # if cb_long:
        #     # self.callbacks[1] = cb_short
        #     # self.cbs_args[1] = kwargs["short_args"]
        
        #     self.callbacks[-1] = cb_long
        #     self.cbs_args[-1] = kwargs["long_args"]

        if False in [callable(val) for val in self.callbacks.values()]:  
            raise TypeError("All callbacks must be a callable")     

        if irq:
            self.pin.irq(handler=self.cb_interrupt, trigger=irq)
    
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
            self.handled = True

        # if not self.counting and not self.hold_flag and self.handled:
        #     print("Short press")
        #     self.callbacks[1](*self.cbs_args[1])
        # elif not self.counting and self.hold_flag and self.handled:
        #     print("Long press")
        #     self.callbacks[-1](*self.cbs_args[-1])
        # elif self.counting and self.handled:
        #     self.callbacks[self.counter](*self.cbs_args[self.counter])

        if not self.hold_flag and self.handled:
            self.callbacks[self.counter](*self.cbs_args[self.counter])
        elif self.hold_flag and self.handled:
            print("Long press")
            self.callbacks['long'](*self.cbs_args['long'])            

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