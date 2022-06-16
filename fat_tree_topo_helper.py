import sys
from nest.experiment import *
from nest.topology import *
from nest.topology.topo_helper import topo_helper
from nest.topology.network import Network
from nest.topology.address_helper import AddressHelper

class PodError(Exception):
    """
    Exception handling
    """

    def __init__(self, message):
        self.message = message


class Pod:
    """
    Abstraction of edge switches, aggregate switches and hosts with interconnection links between them
    """

    def __init__(self, k, net, bw, delay, w):
        '''
        Creates links between aggregate switches, edge switches and hosts in a pod

        Parameters
        ----------
        param: k
            number of pods to be created

        param: nid
            network id for this topology

        param: bw
            bandwidth for all the links present

        param: delay
            delay for all the links present

        param: w
            Pod number(or index number of pod from 0 to k - 1)

        Returns
        -------
        Object of pod class
        '''
        
        self.agg_switches=[Switch('p' + str(w + 1) + 'as' + str(i + 1)) for i in range(k // 2)]
        self.edge_switches=[Switch('p' + str(w + 1) + 'es' + str(i + 1)) for i in range(k // 2)]
        
        t = k**2 // 4

        self.hosts=[Node('p' + str(w + 1) + 'h' + str(i + 1)) for i in range(t)]
       
        '''
        Connections between host to Edge switch
        '''
       
        for i,switch in enumerate(self.edge_switches):
            start = i * (k // 2)
            for j in range(start, start + k // 2):
                with net:
                    (i1, i2) = connect(switch, self.hosts[j])
                    i1.set_attributes(bw, delay)
                    i2.set_attributes(bw, delay)

        '''
        Connections between edge switch to agg switch
        '''

        for p,a_switch in enumerate(self.agg_switches):
            for q,e_switch in enumerate(self.edge_switches):
                with net:
                    (i1, i2) = connect(a_switch, e_switch)
                    i1.set_attributes(bw, delay)
                    i2.set_attributes(bw, delay)


class Fat_tree_helper(topo_helper):
    """
    Abstraction for different pods and their connections with the core switches
    """

    def __init__(self, k, nid, bw = "100mbit", delay = "1ms"):
        '''
        Constructor for initializing different variables and creates links between core switches and pods

        Parameters
        ----------
        param: k
            number of pods to be created

        param: nid
            network id for this topology

        param: bw
            default bandwidth for all the links present

        param: delay
            default delay for all the links present
            
        '''
        super().__init__(bw, delay)

        if k < 0:
            raise PodError("Negative pod count")
        elif k % 2 == 1:
            raise PodError("Odd pod count")

        self.pod_cnt = k
        self.core_cnt = (k // 2)**2
        self.core_switches = [Switch('cs' + str(i + 1)) for i in range(self.core_cnt)]

        self.nid = nid
        self.blocks = [Pod(k, nid, bw, delay, i) for i in range(k)]

        bw = super().get_bandwidth()
        delay = super().get_delay()

        '''
        Connections betwween core switch to agg switch
        '''

        for block in self.blocks:
            start = 0
            for s in block.agg_switches:
                for i in range(start, start + k // 2):
                    t = self.core_switches[i]
                    with self.nid:
                        (i1, i2) = connect(s, t)
                        i1.set_attributes(bw, delay)
                        i2.set_attributes(bw, delay)

                start += (k // 2)

        AddressHelper.assign_addresses()


    def get_core_switch(self, col):
        '''
        Returns a particular core switch

        Parameters
        ----------
        param: col
            column number of core switches

        Returns
        -------
        core switch
        '''
        return self.core_switches[col]
    
    def get_aggregate_switch(self, pod_no, col):
        '''
        Returns a particular aggregate switch

        Parameters
        ----------
        param: pod_no
            pod number of the aggregate switch to be returned

        param: col
            col number of the aggregate switch in the given pod

        Returns
        -------
        aggregate switch
        '''
        return self.blocks[pod_no].agg_switches[col]

    def get_edge_switch(self, pod_no, col):
        '''
        Returns a particular edge switch

        Parameters
        ----------
        param: pod_no
            pod number of the edge switch to be returned

        param: col
            col number of the edge switch in the given pod
            
        Returns
        -------
        edge switch
        '''
        return self.blocks[pod_no].edge_switches[col]

    def get_host(self, pod_no, col):
        '''
        Returns a particular host(or Node)

        Parameters
        ----------
        param: pod_no
            pod number of the host to be returned

        param: col
            col number of the host in the given pod
            
        Returns
        -------
        host(or Node)
        '''
        return self.blocks[pod_no].hosts[col]

    def get_host_address(self, pod_no, col):
        '''
        Returns the ipv4 address of a particular host(or Node)

        Parameters
        ----------
        param: pod_no
            pod number of the host whose address to be returned

        param: col
            col number of the host in the given pod
            
        Returns
        -------
        ipv4 address of a host(or Node)
        '''
        return self.blocks[pod_no].hosts[col]._interfaces[0].address    
    
    def __str__(self):
        return "This is Fat tree class"
