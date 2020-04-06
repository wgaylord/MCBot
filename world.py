import json

class world:
    
    def __init__(self):
        self.blocks = {}
        self.block_light = {}
        self.sky_light = {}
        
        
    def addSection(self,x,z,y,section):
        self.blocks[str(x)+","+str(z)+","+str(y)] = section[0]
        if x == 41 and z == 4:
            print(str(x)+","+str(z)+","+str(y))
    def save(self):
        t = open("test.json","w+")
        json.dump(self.blocks,t)
        t.close()
        
    def getBlock(self,blockX,blockZ,blockY):
        chunkX = int(blockX//16)
        chunkZ = int(blockZ//16)
        chunkY = int(blockY//16)
        blockX = abs(blockX - (chunkX*16))
        blockY = abs(blockY - (chunkY*16))
        blockZ = abs(blockZ - (chunkZ*16))
        try:
            return self.blocks[str(chunkX)+","+str(chunkZ)+","+str(chunkY)][0:4096][int((((blockY * 16) + blockZ) * 16) + blockX)];
        except Exception as e:
            print(e)
            return {"name":"minecraft:air"}
        
        
