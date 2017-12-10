import Pyro4
import hashlib
import random
import sys
import time
import requests
import json
from threading import Thread

from messenger import register

def hashcash(msg):
    m = hashlib.sha256()
    m.update(msg.encode('ascii'))
    return hashlib.sha256(m.digest()).hexdigest()


@Pyro4.expose
class Miner(object):
    _MAX_INT = 9999999
    _GAME = 'testnet3'
    _ENDPOINT = 'https://gameathon.mifiel.com/api/v1/games/{}/block_found' \
                .format(_GAME)
    _ENDPOINT_TARGET = 'https://gameathon.mifiel.com/api/v1/games/{}/target' \
                .format(_GAME)

    def init(self):
        self.target_raw = b'0'
        self.target = 0
        self.stop_ = True
        self.worker = None
        response = requests.get(self._ENDPOINT_TARGET)
        target = json.loads(response.content)['target']
        self.target_changed(target)

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
        if self.worker:
            self.worker.stop()
        target_ = self.target_raw
        worker = Thread(target=Miner._do_mine_block, args = (0, self._MAX_INT, target_, block))
        self._worker = worker
        self._worker.start()


    def _do_mine_block(min_int, max_int, target, block):
        partial_header = block['version_'] + '|' + \
                         block['prev_block_hash'] + '|' + \
                         block['merkle_hash'] + '|' + \
                         target + '|' + \
                         block['message'] + '|'
        stop_ = False
        while not stop_:
            nonce = random.randint(min_int, max_int)
            block_header = partial_header + str(nonce)
            hash_ = hashcash(block_header)
            if hash_ < target:
                print('block_found!!! :')
                print(block_header)
                block['nonce'] = nonce
                block['created_at'] = time.time()
                block['target'] = target
                Miner._report_found(block)
                stop_ = True



    def target_changed(self, new_target):
        self.target_raw = new_target
        self.target = int(new_target, 16)


if __name__ == '__main__':
    miner = register(Miner, 'miner')

    print("Miner: {}".format(miner))
    miner.requestLoop()
