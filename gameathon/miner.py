import Pyro4
import hashlib
import random
import sys
import time
import requests
import json

from messenger import register

def hashcash(msg):
    m = hashlib.sha256()
    m.update(msg)
    return hashlib.sha256(m.digest()).digest()


@Pyro4.expose
class Miner(object):
    _MAX_INT = 99999999999999999
    _GAME = 'testnet'
    _ENDPOINT = 'https://gameathon.mifiel.com/api/v1/games/{}/block_found' \
                .format(_GAME)
    _ENDPOINT_TARGET = 'https://gameathon.mifiel.com/api/v1/games/{}/target' \
                .format(_GAME)

    def __init__(self):
        self.target_raw = b'0'
        self.target = 0
        self.stop_ = True
        response = requests.get(self._ENDPOINT_TARGET)
        target = json.loads(response.content)['target']
        self.target_changed(target)


    def stop(self):
        self.stop_ = True


    def _report_found(self, block):
        report = {
              'prev_block_hash': block['prev_block_hash'].decode(),
              'message': 'TeamZero Level Up!',
              'nonce': block['nonce'],
              'nickname': 'TeamZero',
              'merkle_root': block['merkle_hash'].decode(),
              'used_target': block['target'].decode(),
              'transactions': block['transactions']
            }
        r = requests.post(self._ENDPOINT, json=report)
        print("POST block response: " + r.text[:300] + '...')


    def mine_block(self, block):
        partial_header = block['version'] + b'|' + \
                         block['prev_block_hash'] + b'|' + \
                         block['merkle_hash'] + b'|' + \
                         self.target_raw + b'|' + \
                         block['message'] + b'|'
        self.stop_ = False
        while not self.stop_:
            nonce = random.randint(0, self._MAX_INT)
            block_header = partial_header + str(nonce).encode('ascii')
            hash_ = hashcash(block_header)
            if int.from_bytes(hash_, byteorder='big') < self.target:
                print('block_found!!! :')
                print(block_header)
                block['nonce'] = nonce
                block['created_at'] = time.time()
                block['target'] = self.target_raw
                self._report_found(block)
                self.stop_ = True



    def target_changed(self, new_target):
        self.target_raw = new_target.encode('ascii')
        self.target = int(new_target, 16)


if __name__ == '__main__':
    miner = register(Miner, 'miner')

    print("Miner: {}".format(miner))
    miner.requestLoop()
