

class world:
    
    def __init__(self):
        self.raw_blocks = {}
        self.blocks = {}
        self.block_light = {}
        self.sky_light = {}
        
        
    def addSection(self,x,z,y,section):
        self.raw_blocks[str(x)+","+str(z)+","+str(y)] = section[0]
        
    def process(self):
        for x in self.raw_blocks.keys():
            self.blocks[x] = self.raw_blocks[x][0:4096]
        
    def getBlock(self,blockX,blockZ,blockY):
        chunkX = int(blockX//16)
        chunkZ = int(blockZ//16)
        chunkY = int(blockY//16)
        blockX = abs(blockX - (chunkX*16))
        blockY = abs(blockY - (chunkY*16))
        blockZ = abs(blockZ - (chunkZ*16))
        try:
            return self.blocks[str(chunkX)+","+str(chunkZ)+","+str(chunkY)][int((((blockY * 16) + blockZ) * 16) + blockX)];
        except Exception as e:
            print(e)
            return {"name":"minecraft:air"}
        
    def updateBlock(self,blockX,blockZ,blockY):
        pass
