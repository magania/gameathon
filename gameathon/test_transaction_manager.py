from transaction_manager import TransactionManager

tm = TransactionManager()
tm.init()
block = {"prev_block_hash": 'aoeuoae' ,"hash":"0000000000000000000000000000000000000000000000000000000000000000","height":0,"message":"The very first block","merkle_hash":"dcc7d4fd08cbc0484f3f2eda3cc20f2b2d1b4e5eebfaafc82d5526d73637ff49","reward": 0,"nonce":"0","user":"satoshi","target":"00000fffffffffffffffffffffffffffffffffffffffffffffffffffffffffff","created_at":"2017-12-08T06:56:26.205Z","size":233,"transactions":[{"hash":"dcc7d4fd08cbc0484f3f2eda3cc20f2b2d1b4e5eebfaafc82d5526d73637ff49","inputs":[{"prev_hash":"0000000000000000000000000000000000000000000000000000000000000000","vout":-1,"script_sig":"5468652076657279206669727374207472616e73616374696f6e","amount":5000000000}],"outputs":[{"value":5000000000,"script":"99f8d0011651234b9478b3a2699a3f8f286404da"}],"size":128,"confirmations":0}]}
print("BLOCK")
print(tm.build_block(block))
