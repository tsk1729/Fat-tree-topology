from abc import ABC,abstractmethod
import sys
from nest.experiment import *
from nest.topology import *
 
 
class topo_helper(ABC):
    def __init__(self,bw,delay):
        self.bandwidth=bw
        self.delay=delay
        self.hosts_cnt=0
        self.switch_cnt=0
        self.router_cnt=0
        self.hosts_list=[]
        self.switch_list=[]
        self.router_list=[]
    
    
    def set_delay(self,delay):
        self.delay=delay
 
    def get_delay(self):
        return self.delay
 
    def set_bandwidth(self,bw):
        self.bandwidth=bw
 
    def get_bandwidth(self):
        return self.bandwidth
           
    
    def __str__(self):
        return "This is topology helper class"
