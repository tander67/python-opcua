Pure Python OPC-UA Client and Server  
http://freeopcua.github.io/, https://github.com/FreeOpcUa/python-opcua

[![Build Status](https://travis-ci.org/FreeOpcUa/python-opcua.svg?branch=master)](https://travis-ci.org/FreeOpcUa/python-opcua)
[![Scrutinizer Code Quality](https://scrutinizer-ci.com/g/FreeOpcUa/python-opcua/badges/quality-score.png?b=master)](https://scrutinizer-ci.com/g/FreeOpcUa/python-opcua/?branch=master)

API is similar to the python bindings of freeopcua c++ client and servers. It offers both a low level interface to send and receive all UA defined structures and high level classes allowing to write a server or a client in a few lines.

Most code is autogenerated from xml specification using same code as the one that is used for freeopcua C++ client and server, thus adding missing functionnality to client and server shoud be trivial.

Using Python3.4 the server and client do not require any third party libraries. If using python2.7 or pypy you need to install enum34, trollius(asyncio), and futures(concurrent.futures), with pip for example. Server and client can be run with pypy.

coveryage.py reports a test coverage of over 90% of code, most of the rest is autogenerate code that is not used yet.


Client: what works:
* connection to server, opening channel, session
* browsing and reading attributes value
* gettings nodes by path and nodeids
* creating subscriptions
* subscribing to items for data change
* subscribing to events
* adding nodes
* method call

Tested servers: freeopcua C++, freeopcua Python, prosys


Client: what is not implemented yet 
* removing nodes 
* adding missing modify methods
* certificate handling
* user and password 

Server: what works:
* creating channel and sessions
* read/set attributes and browse
* gettings nodes by path and nodeids
* autogenerate addres space from spec
* adding nodes to address space
* datachange events
* events
* methods

Tested clients: freeopcua C++, freeopcua Python, uaexpert, prosys, quickopc

Server: what is not implemented
* security (users, certificates, etc)
* removing nodes 
* adding missing modify methods

Example client code:

```
from opcua import ua, Client

class SubHandler(object):
    def data_change(self, handle, node, val, attr):
        print("Python: New data change event", handle, node, val, attr)

    def event(self, handle, event):
        print("Python: New event", handle, event)

if __name__ == "__main__": 
    client = Client("opc.tcp://localhost:4841/freeopcua/server/")
    client.connect()
    
    root = client.get_root_node()

    #getting a variable by path and setting its value attribute
    myvar = root.get_child(["0:Objects", "2:NewObject", "2:MyVariable"])
    var.set_value(ua.Variant([23], ua.VariantType.Int64))
    
    #subscribing to data change event to our variable
    handler = SubHandler()
    sub = client.create_subscription(500, handler)
    sub.subscribe_data_change(myvar)
    
    time.sleep(100)

    client.disconnect()
```

Example server code:

```
    from opcua import ua, Server

    server = Server()
    
    server.set_endpoint("opc.tcp://localhost:4841/freeopcua/server/")
    server.set_server_name("FreeOpcUa Example Server")
    uri = "http://examples.freeopcua.github.io"
    idx = server.register_namespace(uri)
    objects = server.get_objects_node()
    myfolder = objects.add_folder(idx, "myfolder")
    myvar = myfolder.add_variable(idx, "myvar", 6.7)

    # creating an event object
    myevent = server.get_event_object(ObjectIds.BaseEventType)
    myevent.Message.Text = "This is my event"
    myevent.Severity = 300
    
    server.start()
    myevent.trigger()
    ...
```

# Development

Code follows PEP8 apart for line lengths and autogenerate class and enums that keep camel case from XML definition.

## Running tests:

python tests.py

## Coverage

coverage run tests.py  
coverage html  
firefox htmlcov/index.html  

