from nodewire.nodewire import NodeWire
import json

class Node():
    def __init__(self, nw, name, gateway):
        self.name = name
        self.nw = nw
        self.gateway = gateway
        self.ports = {}

    def __iter__(self):
        self.iterobj = iter(self.ports)
        return self.iterobj

    def __next__(self):
        next(self.iterobj)

    def __unicode__(self):
        return self.name + str(self.ports)

    def __repr__(self):
        return self.name + str(self.ports)

    def __str__(self):
        return self.name + str(self.ports)

    def __contains__(self, item):
        return item in self.ports

    def __getitem__(self, item):
        if item in self.ports:
            return self.ports[item]
        elif item == 'name':
            return self.name
        else:
            return None

    def __setitem__(self, key, value):
        self.nw.send(self.gateway+':'+self.name, 'set', key, json.dumps(value))

    def set(self, key,value):
        self.ports[key] = value

    def __getattr__(self, item):
        return self.__getitem__(item)

    def __setattr__(self, key, value):
        if key.startsWith('on_'):
            if isinstance(value,  function):self.__setitem__(key, value)
        else:
            self.__setitem__(key, value)

class control:
    def __init__(self, nodename='control', inputs='', outputs=''):
        self.nw = NodeWire(nodename, process=self.process)
        self.nw.debug = True
        self.nodes = []
        self.inputs =  [{'port':i, 'value':0} for i in  inputs.split()]
        self.outputs = [{'port':o} for o in outputs.split()]

    def __getattr__(self, item):
        ports = [p for p in self.inputs if p['port']==item]
        if ports != []:
            port = ports[0]
            return port['value']
        else:
            ports = [p for p in self.outputs if p['port'] == item]
            if ports != []:
                port = ports[0]
                return  port['get']() if 'get' in port else None
            else:
                raise Exception('invalid port or attribute: {}'.format(item))

    def __setattr__(self, key, value):
        if key.startsWith('on_'):
            port = key[3:]
            ports = [p for p in self.inputs if p['port'] == port]
            if ports!=[]: ports[0]['on']=value
        elif key.startsWith('get_'):
            port = key[4:]
            ports = [p for p in self.outputs if p['port'] == port]
            if ports != []: ports[0]['get'] = value
        else:
            ports = [p for p in self.inputs if p['port'] == key]
            if ports!=[]:
                ports[0]['value'] = value
                if 'on' in ports[0]: ports[0]['on']()

    def create_node(self, nodename, instance=None):
        if instance==None: instance = self.nw.gateway
        n =  Node(self.nw, nodename, instance)
        self.nodes.append(n)
        #todo subscribe to node
        return n

    def process(self, msg):
        if msg.Command == 'get':
            self.nw.send(msg.Sender, 'portvalue', json.dumps(self[msg.Port]))
        elif msg.Command == 'set':
            self[msg.Port] = msg.Value
            self.nw.send(msg.Sender, 'portvalue', json.dumps(self[msg.Port]))
        elif msg.Command == 'portvalue':
            senders = [s for s in self.nodes if s.name==msg.Sender]
            if senders!=[]:
                senders[0].set(msg.Port, msg.Value)
                if 'on_' + msg.Port in senders[0]: senders[0]['on_' + msg.Port]()

if __name__ == '__main__':
    class Handler():
        def __init__(self):
            self.auto = False
            self.times = 0

        def lost_power(self):
            if sco.mains == 0 and self.auto: sco.ignition = 1
            self.times+=1

        def auto_switched(self):
            self.auto = ctrl.auto_switch

        def service_required(self):
            return self.times>10

    ## MAIN PROGRAM
    ctrl = control(inputs = 'auto_switch', outputs = 'service_required')

    handler = Handler()
    ctrl.on_auto_switch = handler.auto_switched
    ctrl.get_service_required = handler.service_required

    sco = ctrl.create_node('sco')
    sco.on_mains = handler.lost_power

    ctrl.nw.run()