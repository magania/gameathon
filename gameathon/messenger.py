import Pyro4


def register(class_, name):
    daemon = Pyro4.Daemon()
    ns = Pyro4.locateNS()
    uri = daemon.register(class_)
    ns.register(name, uri)
    return daemon

def connect(name):
    messenger = Pyro4.Proxy('PYRONAME:{}'.format(name))
    return messenger
