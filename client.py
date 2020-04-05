
from twisted.internet import reactor, defer
from quarry.net.client import ClientFactory, ClientProtocol
from quarry.types.registry import LookupRegistry
from quarry.net.auth import ProfileCLI
from world import world


class BotProtocol(ClientProtocol):
    spawned = False

    def __init__(self, factory, remote_addr):
        # x, y, z, yaw, pitch
        self.pos_look = [0, 0, 0, 0, 0]
        self.registry = LookupRegistry.from_json(".")
        self.world = world()

        super(BotProtocol, self).__init__(factory, remote_addr)

    # Send a 'player' packet every tick
    def update_player_inc(self):
        self.send_packet("player", self.buff_type.pack('?', True))

    # Sent a 'player position and look' packet every 20 ticks
    def update_player_full(self):
        self.send_packet(
            "player_position_and_look",
            self.buff_type.pack(
                'dddff?',
                self.pos_look[0],
                self.pos_look[1],
                self.pos_look[2],
                self.pos_look[3],
                self.pos_look[4],
                True))

    def packet_player_position_and_look(self, buff):
        p_pos_look = buff.unpack('dddff')

        p_flags = buff.unpack('B')

        for i in range(5):
            if p_flags & (1 << i):
                self.pos_look[i] += p_pos_look[i]
            else:
                self.pos_look[i] = p_pos_look[i]

        teleport_id = buff.unpack_varint()

        self.send_packet("teleport_confirm", self.buff_type.pack_varint(teleport_id))

        if not self.spawned:
            self.spawn()

    def spawn(self):
        self.ticker.add_loop(1, self.update_player_inc)
        self.ticker.add_loop(20, self.update_player_full)
        self.spawned = True

    def packet_keep_alive(self, buff):
        self.send_packet('keep_alive', buff.read())

    
    def packet_chat_message(self, buff):
        p_text = buff.unpack_chat()

        p_position = buff.unpack('B')

        self.logger.info(":: %s" % p_text)
        
        
    def packet_chunk_data(self, buff):
        x, z, full = buff.unpack('ii?')
        bitmask = buff.unpack_varint()
        heightmap = buff.unpack_nbt()  # added in 1.14
        biomes = buff.unpack_array('I', 1024) if full else None  # changed in 1.15
        sections_length = buff.unpack_varint()
        sections = buff.unpack_chunk(bitmask)
        block_entities = [buff.unpack_nbt() for _ in range(buff.unpack_varint())]
        if full:
            y = 0
            for x1 in sections:
                if x1:
                    x1[0].registry = self.registry
                    self.world.addSection(x,z,y,x1)
                y+=1
           
    

class BotFactory(ClientFactory):
    protocol = BotProtocol


@defer.inlineCallbacks
def run(args):
    # Log in
    profile = yield ProfileCLI.make_profile(args)

    # Create factory
    factory = BotFactory(profile)

    # Connect!
    factory.connect(args.host, args.port)


def main(argv):
    parser = ProfileCLI.make_parser()
    parser.add_argument("host")
    parser.add_argument("-p", "--port", default=25565, type=int)
    args = parser.parse_args(argv)

    run(args)
    reactor.run()

if __name__ == "__main__":
    import sys
    main(sys.argv[1:])