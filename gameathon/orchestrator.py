import asyncio
import json
import Pyro4
import sys
import websockets
from messenger import connect
import requests

_GAME = 'testnet4'

_ENDPOINT = 'wss://gameathon.mifiel.com/cable'
_PARAMS = {
    'channel': 'MiniBlockchainChannel',
    'nickname': 'TeamZero',
    'uuid': '5dc8ce27-697e-4294-bb7e-46523a0c4f25',
#    'game': 'testnet'
    'game': _GAME
    }
_SUBSCRIPTION = {
    'command': 'subscribe',
    'identifier': json.dumps(_PARAMS)
    }
_TIMEOUT = 60


_ENDPOINT_BLOCKS = 'https://gameathon.mifiel.com/api/v1/games/{}/blocks' \
                .format(_GAME)

_transaction_manager = connect('transaction_manager')
_transaction_manager.init()
_miner1 = connect('miner1')
_miner1.init()
_miner2 = connect('miner2')
_miner2.init()
_miner3 = connect('miner3')
_miner3.init()

def start_mining():
    response = requests.get(_ENDPOINT_BLOCKS)
    blocks = json.loads(response.content)
    ob = blocks[-1]
    print(ob)
    new_block = _transaction_manager.build_block(ob)
    _miner1.mine_block(new_block)
    _miner2.mine_block(new_block)
    _miner3.mine_block(new_block)

def _process_event(event):
    #print(event)
    event_type = event.get('type')
    if event_type == 'ping':
        print('ping:')
        return
    if event_type == 'welcome':
        print('Connected :)')
        return
    if event_type == 'confirm_subscription':
        print('Confirm Subsciption')
        return

    event_message = event.get('message')
    event_type = event_message.get('type')
    event_data = event_message.get('data')
    if event_type == 'new_transaction':
        print("New transaction: ")
        print(event_data)
        _transaction_manager.new_transaction(event_data)
        return
    if event_type == 'block_found':
        print('Block found:')
        print(event_data)
        #_miner.stop()
        _transaction_manager.block_found(event_data)
        new_block = _transaction_manager.build_block(event_data)
        _miner1.mine_block(new_block)
        _miner2.mine_block(new_block)
        _miner3.mine_block(new_block)
        return
    if event_type == 'target_changed':
        print('Target changed:')
        print(event_data)
        _miner.target_changed(event_data)
        return
    print('UNPROCESSED:')
    print(event)

async def orchestrator():
    try:
        async with websockets.connect(_ENDPOINT) as websocket:
            await websocket.send(json.dumps(_SUBSCRIPTION))
            while True:
                event_json = await asyncio.wait_for(websocket.recv(),
                                                    timeout = _TIMEOUT)
                event = json.loads(event_json)
                _process_event(event)
    except Exception as ex:
        print(ex)
        sys.exit(1)

if __name__ == '__main__':
    print("Orchestrator running ...")
    start_mining()
    orchestrator_ = asyncio.ensure_future(orchestrator())
    loop = asyncio.get_event_loop()
    loop.run_forever()
