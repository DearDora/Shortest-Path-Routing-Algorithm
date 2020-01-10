import struct

# For simplicity we consider only 5 routers
NBR_ROUTER = 5


# Define packet structures
class pkt_HELLO:
    def __init__(self,router_id,link_id):
        # id of the router who sends the HELLO PDU       
        self.router_id = router_id
        # id of the link through which it is sent
        self.link_id = link_id
    
    def toBytes(self):
        return struct.pack("<II",self.router_id,self.link_id)
    
    def message(self,direction,router_id):
        result = ""
        if direction == "out":
            result = "R"+str(router_id)+" sends a HELLO_PDU: router_id "+str(self.router_id)+", link_id "+str(self.link_id)
        else:
            result = "R"+str(router_id)+" receives a HELLO_PDU: router_id "+str(self.router_id)+", link_id "+str(self.link_id)
        return result

class pkt_LSPDU:
    def __init__(self, sender, router_id, link_id, cost, via):
        # sender of the LS PDU
        self.sender = sender
        # router id
        self.router_id = router_id
        # link id
        self.link_id = link_id
        # cost of the link
        self.cost = cost
        # id of the link through which the LS PDU is sent
        self.via = via
        
    def toBytes(self):
        return struct.pack("<IIIII",self.sender,self.router_id,self.link_id,self.cost,self.via)
    
    def message(self, direction, router_id):
        result = ""
        if direction == "out":
            result = "R"+str(router_id)+" sends a LS_PDU: sender "+str(self.sender)+", router_id "+str(self.router_id)+", link_id "+str(self.link_id)+", cost"+str(self.cost)+", via"+str(self.via)
        else:
            result = "R"+str(router_id)+" receives a LS_PDU: sender "+str(self.sender)+", router_id "+str(self.router_id)+", link_id "+str(self.link_id)+", cost"+str(self.cost)+", via"+str(self.via)
        return result

class pkt_INIT:
    def __init__(self, router_id):
        # router id
        self.router_id = router_id
    
    def toBytes(self):
        return struct.pack("<I", self.router_id)
    
    def message(self, direction, router_id):
        result = ""
        if direction == "out":
            result = "R"+str(router_id)+" sends an INIT_PDU: router_id "+str(self.router_id)
        else:
            result = "R"+str(router_id)+" receives an INIT_PDU: router_id "+str(self.router_id)
        return result
            
class link_cost:
    def __init__(self, link, cost):
        # link id
        self.link = link
        # associated cost
        self.cost = cost
        
    def toBytes(self):
        return struct.pack("<II",self.link,self.cost)
    
    def __str__(self):
        return "link "+str(self.link)+", cost "+str(self.cost)+"\n"

class circuit_DB:
    def __init__(self, nbr_link, linkcost):
        # number of links attached to a router
        self.nbr_link = nbr_link
        # we assume that at most NBR_ROUTER links are attached to each router
        self.linkcost = linkcost
        
    def toBytes(self):
        result = struct.pack("<I",self.nbr_link)
        for item in self.linkcost:
            result += item.toBytes()
        return result
        
    def message(self, direction, router_id):
        result = ""
        links = ""
        for item in self.linkcost:
            links += "    link "+str(item)
        if direction == "out":
            result = "R"+str(router_id)+" sends a CIRCUIT_DB: nbr_link "+str(self.nbr_link)+" with links:\n"+links
            
        else:
            result = "R"+str(router_id)+" receives a CIRCUIT_DB: nbr_link "+str(self.nbr_link)+" with links:\n"+links
        return result

# Unpack the bytes and transfer into a packet
def upPack(bytes, database = False):
    data_length = len(bytes)
    if database == True:
        linkcost = []
        nbr_link = struct.unpack_from("<I", bytes, 0)[0]
        for i in range(nbr_link):
            data = struct.unpack_from("<II", bytes, 4+(i*8))
            linkcost.append(link_cost(data[0],data[1]))
	return ("CIRCUIT_DB", circuit_DB(nbr_link,linkcost))
    else:
        if data_length == 8:
            data = struct.unpack("<II", bytes)
	    return ("HELLO_PDU",pkt_HELLO(data[0], data[1]))
	if data_length == 20:		
	    data = struct.unpack("<IIIII", bytes)
	    return ("LS_PDU",pkt_LSPDU(data[0], data[1], data[2], data[3], data[4]))
	if data_length == 4:
	    data = struct.unpack("<I", bytes)
	    return ("INIT_PDU",pkt_INIT(data[0]))	
	
	print("Not a packet")