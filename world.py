import json

class world:
    
    def __init__(self):
        self.blocks = {}
        self.block_light = {}
        self.sky_light = {}
        
        
    def addSection(self,x,z,y,section):
        self.blocks[str(x)+","+str(z)+","+str(y)] = section[0]
        
    def save(self):
        t = open("test.json","w+")
        json.dump(self.blocks,t)
        t.close()
        
    def getBlock(self,blockX,blockZ,blockY):
        chunkX = blockX//16
        chunkZ = blockZ//16
        chunkY = blockY//16
        try:
            return self.blocks[str(chunkX)+","+str(chunkZ)+","+str(chunkY)][(((blockY * 16) + blockZ) * 16) + blockX];
        except:
            return {"name":"minecraft:air"}
        
        