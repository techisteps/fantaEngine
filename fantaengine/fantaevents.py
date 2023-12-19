"""`fantaEvents` is a singleton class to handle events in FantaEngine.
`__new__()` method creates a singleton object and returns.
Two class attributes `__instance` and `__events` are defined.
Attributes `__instance` holds the reference of singleton object and
attributes `__events` holds Dictionary of events and mapped callback functions in below form.
```py
__events = {
"TestEvent1", ["fuction1", "function2"]
"TestEvent2", ["fuction3", "function4"]
}
```

Example Code:
```py

def testFunc1(data):
    print("called from testFunc1 ", data)

def testFunc2(data):
    print("called from testFunc2 ", data)    

fe = fantaEvents()

fe.register_event("test", testFunc1)
fe.register_event("test", testFunc2)
fe.register_event("newtest", testFunc1)

fe.dispatch_event("test", "test1data")
fe.dispatch_event("test", "test2data")
fe.dispatch_event("newtest", "newtestdata")

fe.unregister_event("newtest")

fe.print_events()
fe.print_events(list=True)
```


"""

class fantaEvents:

    __instance = None
    __events = {}

    def __new__(cls):
        if cls.__instance is None:
            cls.__instance = super().__new__(cls)
            return cls.__instance
        else:
            return cls.__instance

    def register_event(self, eventname: str, function: callable):
        """Registers a function to be called when event specified by eventname is dispatched.

        Args:
            eventname (str): Eventname for which function will be called.
            function (callable): Function name which will be called for specified event.
        """
        
        handlers = self.__events.get(eventname)

        if handlers is None:
            self.__events[eventname] = [function]
        else:
            handlers.append(function)

    def unregister_event(self, eventname : str):
        """Unregisters an event.

        Args:
            eventname (str): Eventname which should be unregistered.

        Raises:
            KeyError: Raised KeyError if given `eventname` not registered before. Prints in console.
        """
        try:
            val = self.__events.pop(eventname)
        except KeyError:
            print(f"Event {eventname} not defined.")            
        except:
            print(f"Event {eventname} not defined.")            


    def dispatch_event(self, eventname: str, data: any):
        """
        Fires the event mentioned by `eventname`. `data` will be passed to registered callback functions.
        Internally calls all registered call back functions.

        Args:
            eventname (str): Fires the event by this name
            data (any): Data which will be passed to registered callback functions.

        Raises:
            ValueError: Raised ValueError if given `eventname` not registered before.
        """

        if eventname is None:
            raise ValueError(f"Event {eventname} not defined.")
        
        handlers = self.__events.get(eventname)
        if handlers is None:
            print(f"event handler for {eventname} not defined.")
        else:
            for handler in handlers:
                handler(data)


    def print_events(self, list: bool = False):
        """
        print_events prints all events in console. This is only for debugging purpose.

        Args:
            list (bool, optional): If true output will be in key/calue pair. Defaults to False.
        """
        if list:
            for key, value in self.__events.items():
                print(key, " -> ", value)
        else:
            print(self.__events)


def testFunc1(data):
    print("called from testFunc1 ", data)

def testFunc2(data):
    print("called from testFunc2 ", data)    


if __name__ == "__main__":
    print("called in main")

    fe = fantaEvents()

    fe.register_event("test", testFunc1)
    fe.register_event("test", testFunc2)
    fe.register_event("newtest", testFunc1)

    fe.dispatch_event("", "newtestdata")
    fe.dispatch_event("test", "test1data")
    fe.dispatch_event("test", "test2data")
    fe.dispatch_event("newtest", "newtestdata")

    fe.unregister_event("newtest")
    fe.unregister_event("newtest1")

    fe.print_events()
    fe.print_events(list=True)
    # testFunc("sentdata")    
