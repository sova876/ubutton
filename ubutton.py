import time

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

        #Set up callbacks and callback arguments.
        self.callbacks = kwargs['cbs']
        self.cbs_args = kwargs["cb_args"]

        keys = self.callbacks.keys() #Keys for all defined callbacks
        max_clicks = max([key for key in keys if type(key) is int]) + 1 #Max click counts

        #Set defaults. 
        #This is necessary, for example, if the callback for 1 and 3 clicks is defined, 
        #but not for 2 clicks. In this case, the specified callbacks will be called for 1 and 3 clicks, 
        #and nothing will happen for 2 clicks.
        [self.callbacks.setdefault(key, lambda *a, **k: None) for key in range(1, max_clicks)] #Set default callback to empty callable.
        [self.cbs_args.setdefault(key, []) for key in range(1, max_clicks)] #Set default callback arguments to empty list

        #Verify that all callbacks are callables
        if False in [callable(val) for val in self.callbacks.values()]:  
            raise TypeError("All callbacks must be a callable")     

        #Setup interrupt
        if irq:
            self.pin.irq(handler=self.cb_interrupt, trigger=irq)
    
    def handler(self):

        btn_state = self.pin.value() #read pin state
        cur_ticks = time.ticks_ms() #remember current tick
        ticks_diff = time.ticks_diff(cur_ticks, self.btn_tmr) #find time diff with last interrupt

        if btn_state and not self.btn_flag and ticks_diff > self.bounce_time:
            #Press detector with debouncing option
            self.btn_flag = 1
            print("Pressed!")
            self.btn_tmr = cur_ticks           
        elif not btn_state and self.btn_flag and ticks_diff > self.bounce_time:
            #Release detector with debouncing option and clicks counting
            self.btn_flag = 0
            self.counter += 1
            self.btn_tmr = cur_ticks
            print("Released!")
        elif btn_state and self.btn_flag and ticks_diff > self.long_time:
            #Hold detector with debouncing option and clicks counting
            self.hold_flag = True
            self.btn_tmr = cur_ticks
            print("Hold!")
        
        if not btn_state and not self.btn_flag and ticks_diff > self.click_timeout and self.counter != 0:
            #If nothing happened after timeout time then the interrupt was handled.
            print("Counter:", self.counter)
            self.handled = True

        if not self.hold_flag and self.handled:
            #If not a long press and interrupt was handled then callback.
            self.callbacks[self.counter](*self.cbs_args[self.counter])
        elif self.hold_flag and self.handled:
            #Long press callback.
            print("Long press")
            self.callbacks['long'](*self.cbs_args['long'])            

    def cb_interrupt(self, pin):
        #A function called on each pin interrupt detection.

        if self.pin.value():
            #If button is really pressed then call a handler method.
            self.handled = False
        else: self.handled = True #Else it was a fake

        self.btn_tmr = time.ticks_ms()
        self.btn_flag = 0
        self.hold_flag = False
        self.counter = 0

        while not self.handled:
            #Call a handler method utill it is not handled
            self.handler()