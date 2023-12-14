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
        
        handlers = self.__events.get(eventname)

        if handlers is None:
            self.__events[eventname] = [function]
        else:
            handlers.append(function)

    def unregister_event(self, eventname : str):
        try:
            val = self.__events.pop(eventname)
        except KeyError:
            print(f"Event {eventname} not defined.")            
        except:
            print(f"Event {eventname} not defined.")            


    def dispatch_event(self, eventname: str, data: any):

        if eventname is None:
            raise ValueError(f"Event {eventname} not defined.")
        
        handlers = self.__events.get(eventname)
        if handlers is None:
            print(f"event handler for {eventname} not defined.")
        else:
            for handler in handlers:
                handler(data)


    def print_events(self, list: bool = False):
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
