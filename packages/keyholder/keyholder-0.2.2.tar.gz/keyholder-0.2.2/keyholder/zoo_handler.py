from kazoo.client import KazooClient
from kazoo.client import KazooState
from kazoo.exceptions import KazooException
from kazoo.handlers.threading import KazooTimeoutError

import logging

class zoo_handler:
    zk = None
    host = ""
    port = 0
    logging = None
    state = ""

    def __init__(self,host,port):
        def conn_listener(state):
            if (state == KazooState.LOST):
                self.state = "LOST"
            elif state == KazooState.SUSPENDED:
                self.state = "SUSPENDED"
            else:
                self.state = "CONNECTED"
        self.host = host
        self.port = port
        self.zk = KazooClient(host+":"+str(port))
        try:
            self.zk.start()
            self.logging = logging.basicConfig()
            self.zk.add_listener(conn_listener)
        except Exception:
            self.state="LOST"
            self.zk=None

    def ensure_path(self,path):
        if (self.zk.state == "CONNECTED"):
            self.zk.ensure_path(path)
        self.state = self.zk.state

    def create(self,path):
        if (self.zk.state == "CONNECTED"):
            self.zk.create(path)
        self.state = self.zk.state

    def exists(self,node):
        self.state = self.zk.state
        if (self.zk.state == "CONNECTED"):
            return self.zk.exists(node)
        return None

    def get_node_data(self,node):
        self.state = self.zk.state
        if (self.zk.state == "CONNECTED"):
            return self.zk.get(node)
        return None

    def get_children(self,path):
        self.state = self.zk.state
        if (self.zk.state == "CONNECTED"):
            return self.zk.get_children(path)
        return None

    def set_node_data(self,node,data):
        self.state = self.zk.state
        if (self.zk.state == "CONNECTED"):
            self.zk.set(node,data)

    def delete_node(self,node,isrecursive):
        self.state = self.zk.state
        if (self.zk.state == "CONNECTED"):
            self.zk.delete(node,recursive=isrecursive)