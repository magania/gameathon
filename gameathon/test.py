from messenger import connect

miner = connect('miner')
print(miner.mine_block('mine_block'))
