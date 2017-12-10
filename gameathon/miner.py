import Pyro4
import hashlib
import random
import sys
import time
import requests
import json
import sys
from threading import Thread
from multiprocessing import Process

from messenger import register

def hashcash(msg):
    m = hashlib.sha256()
    m.update(msg.encode('ascii'))
    return hashlib.sha256(m.digest()).hexdigest()


@Pyro4.expose
class Miner(object):
    _MAX_INT = 999999999999999
    _GAME = 'testnet4'
    _ENDPOINT = 'https://gameathon.mifiel.com/api/v1/games/{}/block_found' \
                .format(_GAME)
    _ENDPOINT_TARGET = 'https://gameathon.mifiel.com/api/v1/games/{}/target' \
                .format(_GAME)

    def init(self, value):
        self.target_raw = b'0'
        self.target = 0
        self.stop_ = True
        self._worker = None
        response = requests.get(self._ENDPOINT_TARGET)
        target = json.loads(response.content)['target']
        self.target_changed(target)
        self.value = value

    def stop(self):
        pass

    def _report_found(block):
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
        r = requests.post(Miner._ENDPOINT, json=report)
        print("POST block response: " + r.text[:300] + '...')


    def mine_block(self, block):
        print('stop')
        self.stop_ = True
        if self._worker:
            self._worker.terminate()

        target_ = self.target_raw
        value = self.value
        worker = Process(target=self.do_mine_block, args = (0, self._MAX_INT, target_, block, value))
        self._worker = worker
        self._worker.start()


    def do_mine_block(self,min_int, max_int, target, block, value):
        partial_header = block['version_'] + '|' + \
                         block['prev_block_hash'] + '|' + \
                         block['merkle_hash'] + '|' + \
                         target + '|' + \
                         block['message'] + '|'
        self.stop_ = False
        nonce = value + 1000000000
        n_nonces = 0
        while not self.stop_:
            n_nonces += 1
            if n_nonces%100000==0:
                print('n_nonces',n_nonces) 
            nonce +=  3
            block_header = partial_header + str(nonce)
            hash_ = hashcash(block_header)
            if hash_ < target:
                print('block_found!!! :')
                print(block_header)
                block['nonce'] = nonce
                block['created_at'] = time.time()
                block['target'] = target
                Miner._report_found(block)
                self.stop_ = True



    def target_changed(self, new_target):
        self.target_raw = new_target
        self.target = int(new_target, 16)


if __name__ == '__main__':
    print('miner' + sys.argv[1])
    miner = register(Miner, 'miner' + sys.argv[1])

    print("Miner: {}".format(miner))
    miner.requestLoop()
