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
    m.update(msg.encode('ascii'))
    return hashlib.sha256(m.digest()).hexdigest()


@Pyro4.expose
class Miner(object):
    _MAX_INT = 9999999
    _GAME = 'testnet'
    _ENDPOINT = 'https://gameathon.mifiel.com/api/v1/games/{}/block_found' \
                .format(_GAME)
    _ENDPOINT_TARGET = 'https://gameathon.mifiel.com/api/v1/games/{}/target' \
                .format(_GAME)

    def init(self):
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
              'prev_block_hash': block['prev_block_hash'],
              'message': '5465616d5a65726f2052756c657321',
              'nonce': block['nonce'],
              'nickname': 'TeamZero',
              'merkle_root': block['merkle_hash'],
              'used_target': block['target'],
              'transactions': block['transactions'],
              'height': block['height']
            }
        r = requests.post(self._ENDPOINT, json=report)
        print("POST block response: " + r.text[:300] + '...')


    def mine_block(self, block):
        partial_header = block['version_'] + '|' + \
                         block['prev_block_hash'] + '|' + \
                         block['merkle_hash'] + '|' + \
                         self.target_raw + '|' + \
                         block['message'] + '|'
        self.stop_ = False
        while not self.stop_:
            nonce = random.randint(0, self._MAX_INT)
            block_header = partial_header + str(nonce)
            hash_ = hashcash(block_header)
            if hash_ < self.target_raw:
                print(hash_)
                print('block_found!!! :')
                print(block_header)
                block['nonce'] = nonce
                block['created_at'] = time.time()
                block['target'] = self.target_raw
                self._report_found(block)
                self.stop_ = True



    def target_changed(self, new_target):
        self.target_raw = new_target
        self.target = int(new_target, 16)


if __name__ == '__main__':
    miner = register(Miner, 'miner')

    print("Miner: {}".format(miner))
    miner.requestLoop()
