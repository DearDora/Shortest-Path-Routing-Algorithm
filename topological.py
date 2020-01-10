class topological_Entry:
    def __init__(self, number, link, cost, end):
        self.number = number
        self.linkcost = [(link,cost,end)]
    
    def changeData(self, link, cost, end):
        for i in range(len(self.linkcost)):
            if self.linkcost[i][1] == cost and self.linkcost[i][0] == link:
                if self.linkcost[i][2] != end:
                    self.linkcost[i] = (link,cost,end)
                    return True
        if (link,cost,end) not in self.linkcost:
            self.number += 1
            self.linkcost.append((link,cost,end))
            return True
        return False   

# Topological database
class topological_DB:
    def __init__(self, router_id):
        self.router_id = router_id
        self.link_dictionary = dict()
    
    # Return the neighbours of router   
    def neighbours(self, router):
        result = []
        if router in self.link_dictionary:
            for item in self.link_dictionary[router].linkcost:
                if item[2] != None:
                    result.append(item[2])
        return result
    
    # Find the destination of the router
    def findEnd(self, router, link):
        for item in self.link_dictionary:
            if router != item:
                for lc in self.link_dictionary[item].linkcost:
                    if lc[0] == link:
                        return item
        return None
    
    # Determine the cost to router
    def cost(self, router, end):
        result = float("inf")
        if router in self.link_dictionary:
            for item in self.link_dictionary[router].linkcost:
                if item[2] == end:
                    result = item[1]
            return result
            
    # Determine the link of two routers
    def link(self, router1, router2):
        result = None
        for item in self.link_dictionary[router1].linkcost:
            if item[2] == router2:
                result = item[0]
        return result
    
    # Add link
    def addLink(self, router, link, cost):
        end = None
        isChange = False
        if router not in self.link_dictionary:
            end = self.findEnd(router,link)
            self.link_dictionary[router] = topological_Entry(1,link,cost,end)
            isChange = True
        else:
            end = self.findEnd(router,link)
            isChange = self.link_dictionary[router].changeData(link,cost,end)
        
        if (end != None) and isChange:
            self.link_dictionary[end].changeData(link, cost, router)
        return isChange
    
    # Update link
    def update(self, router, link):
        cost = None
        for item in self.link_dictionary[self.router_id].linkcost:
            if item[0] == link:
                cost = item[1]
        self.link_dictionary[self.router_id].changeData(link,cost,router)
        
    def __str__(self):
        result = "\n# Topology Database:\n"
        for router,entry in self.link_dictionary.items():
            result += ("R"+str(self.router_id)+" -> R"+str(router)+" nbr link "+str(entry.number)+"\n")
            for item in entry.linkcost:
                result += ("R"+str(self.router_id)+" -> R"+str(router)+" link "+str(item[0])+" cost "+str(item[1])+"\n")
        return result