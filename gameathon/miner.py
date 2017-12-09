import Pyro4
from messenger import register

@Pyro4.expose
class Miner(object):
    def __init__(self):
        self.target = None
        pass

    def stop(self):
        pass

    def mine_block(self, block):
        print('Mining {}'.format(block))
        pass

    def target_changed(self, new_target):
        self.target = new_target

    def listen(self):
        pass


if __name__ == '__main__':
    miner = register(Miner, 'miner')

    print("Miner: {}".format(miner))
    miner.requestLoop()
