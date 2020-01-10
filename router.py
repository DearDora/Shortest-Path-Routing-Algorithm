import sys
import os
import logging
from socket import *
from rib import *
from topological import *
from packet import *

def Dijkstra(router_id,ib,top):
    N = [router_id]
    D = {router_id:0}
    P = {router_id: None}
    ib.addRouter(router_id,"Local",D[router_id])
    for i in range(1,1+NBR_ROUTER):
        if i != router_id:
            neighbours = top.neighbours(router_id)
            if i in neighbours:
                D[i] = top.cost(router_id,i)
                P[i] = i
                ib.addRouter(i,P[i],D[i])
            else:
                D[i] = float("inf")
    while(len(N)<NBR_ROUTER):
        weight = (None, float("inf"))
        for i in range(1,1+NBR_ROUTER):
            if (i not in N) and (weight[1]>D[i]):
                weight = (i,D[i])
        N.append(weight[0])
        for item in top.neighbours(weight[0]):
            if item not in N:
                D[item] = min(D[item],top.cost(weight[0],item)+D[weight[0]])
                P[item] = P[weight[0]]
                ib.addRouter(i, P[weight[0]], D[item])     
        
def main():
    # Check arguments
    arguments = sys.argv[1:]
    if len(arguments) != 4:
        print("ERROR: Four command line arguments required")
        exit(1)
    else:
        router_id = int(arguments[0])
        nse_host = arguments[1]
        nse_port = int(arguments[2])
        router_port = int(arguments[3])
    # Initialize sockets
    rSocket = socket(AF_INET,SOCK_DGRAM)
    rSocket.bind(("", router_port))
    IB = RIB(router_id)
    TOP = topological_DB(router_id)
    file = "router"+str(router_id)+".log"
    # Delete the file if it exists
    if os.path.isfile(file):
        os.remove(file)
    log_info = logging.getLogger(__name__)
    log_info.setLevel(logging.INFO)
    file_handler = logging.FileHandler(file)
    file_handler.setLevel(logging.INFO)
    log_info.addHandler(file_handler)
    
    init = pkt_INIT(router_id)
    rSocket.sendto(init.toBytes(),(nse_host,nse_port))
    log_info.info(init.message("out",router_id))
    
    data,client = rSocket.recvfrom(4096)
    circuit = upPack(data,True)[1]
    log_info.info(circuit.message("in",router_id))
    
    for nei in circuit.linkcost:
        hello = pkt_HELLO(router_id,nei.link)
        isChange = TOP.addLink(router_id,nei.link,nei.cost)
        rSocket.sendto(hello.toBytes(),(nse_host,nse_port))
        log_info.info(hello.message("out",router_id))
        
    knownNeighbour = []
    
    while(True):
        data, client = rSocket.recvfrom(4096)
        pkt = upPack(data)
        pkt_type = pkt[0]
        pkt_data = pkt[1]
        log_info.info(pkt_data.message("in",router_id))
        
        if pkt_type == "HELLO_PDU":
            knownNeighbour.append(pkt_data.router_id)
            isChange = TOP.update(pkt_data.router_id, pkt_data.link_id)
            log_info.info(str(TOP))
            log_info.info(str(IB))
            for item in circuit.linkcost:
                LSPDU_pkt = pkt_LSPDU(router_id,router_id,item.link,item.cost, pkt_data.link_id)
                rSocket.sendto(LSPDU_pkt.toBytes(),(nse_host,nse_port))
                log_info.info(LSPDU_pkt.message("out",router_id))  
        elif pkt_type == "LS_PDU":
            isChange = TOP.addLink(pkt_data.router_id, pkt_data.link_id, pkt_data.cost)
            
            if isChange:
                log_info.info(str(TOP))
                for item in knownNeighbour:
                    if pkt_data.sender != item:
                        lspdu = pkt_LSPDU(router_id,pkt_data.router_id,pkt_data.link_id,pkt_data.cost,TOP.link(router_id,item))
                        rSocket.sendto(lspdu.toBytes(),(nse_host,nse_port))
                        log_info.info(lspdu.message("out",router_id))
                Dijkstra(router_id,IB,TOP)
                log_info.info(str(IB))
        
if __name__ == "__main__":
    main()