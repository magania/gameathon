import asyncio
import json
import Pyro4
import sys
import websockets

_ENDPOINT = 'wss://gameathon.mifiel.com/cable'
_PARAMS = {
    'channel': 'MiniBlockchainChannel',
    'nickname': 'TeamZero',
    'uuid': '5dc8ce27-697e-4294-bb7e-46523a0c4f25',
#    'game': 'testnet'
    'game': 'first-brightness'
    }
_SUBSCRIPTION = {
    'command': 'subscribe',
    'identifier': json.dumps(_PARAMS)
    }
_TIMEOUT = 60

def _process_event(event):
    event_type = event.get('type')
    if event_type == 'welcome':
        print('Connected :)')
    elif event_type == 'ping':
        print('ping:')
    else:
        print('UNPROCESSED:')
        print(event)
        print('---')


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
    orchestrator_ = asyncio.ensure_future(orchestrator())
    loop = asyncio.get_event_loop()
    loop.run_forever()
