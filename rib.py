NBR_ROUTER = 5

class RIB:
    def __init__(self, router_id):
        self.router_id = router_id
        self.dictionary = dict()
        for i in range(1,NBR_ROUTER+1):
            if i == router_id:
                self.dictionary[i] = ("Local", 0)
            else:
                self.dictionary[i] = ("INF", float("inf"))
    
    def addRouter(self, router, path, cost):
        if router in self.dictionary:
            if cost < self.dictionary[router][1]:
                self.dictionary[router] = (path,cost)
        else:
            self.dictionary[router] = (path,cost)
            
    def __str__(self):
        result = "\n# RIB:\n"
        for router,entry in self.dictionary.items():
            result += ("R"+str(self.router_id)+" -> "+"R"+str(router)+" -> ")
            if (str(entry[0]) != "INF") and (str(entry[0]) != "Local"):
                result += "R"
            result += (str(entry[0])+","+str(entry[1])+"\n")
        return result