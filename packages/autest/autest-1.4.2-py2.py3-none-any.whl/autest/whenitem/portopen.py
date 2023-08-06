import socket
from autest.api import AddWhenFunction
import hosts.output as host
import psutil


def PortOpen(port, address=None, timeout=None):
    netstate = psutil.net_connections('inet4')
    ret = False
    # if no port are being read.. we probally have some system issue with the library
    # and should fall back to older logic
    if netstate:
        connections = [i.laddr for i in netstate]
        ports = [i.port for i in connections if i.ip == address or address is None]
        if port in ports:
            ret = True

    else:
        if address is None:
            address = "localhost"
        if timeout is None:
            timeout = .5
        address = (address, port)
        try:
            s = socket.create_connection(address, timeout=timeout)
            s.close()
            ret = True
        except socket.error:
            s = None
            ret = False
        except socket.timeout:
            s = None
        host.WriteDebug(["portopen", "when"],
                        "checking port {0} = {1}".format(port, ret))

    return ret


AddWhenFunction(PortOpen)
