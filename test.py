import logging

from opcua import Client
from opcua import uaprotocol as ua


if __name__ == "__main__": 
    from IPython import embed
    logging.basicConfig(level=logging.DEBUG)
    client = Client("opc.tcp://localhost:4841/freeopcua/server/")
    try:
        client.connect()
        root = client.get_root_node()
        print(root)
        print(root.get_children())
        print(root.get_name())
        var = client.get_node(ua.NodeId(1002, 2))
        print(var)
        print(var.get_value())
        var.set_value(ua.Variant([23], ua.VariantType.Int64))
        embed()
        client.close_session()
    finally:
        client.disconnect()