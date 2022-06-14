from web3 import Web3
import json
import os
ganache_url = "http://127.0.0.1:7545"
web3 = Web3(Web3.HTTPProvider(ganache_url))

abiFile = open(os.path.dirname(__file__).replace("\\","/")+"/bin/CryptoRide.abi","r")
abi = json.loads(abiFile.read())
abiFile.close()
addressFile = open(os.path.dirname(__file__).replace("\\","/")+"/contractAddress.txt","r")
address = web3.toChecksumAddress(addressFile.read())

contract = web3.eth.contract(address = address, abi= abi)

print("Account:")
account = int(input())
print("ID:")
_id = int(input())
print('Base cost: {}'.format(
    contract.functions.getBaseCost(_id).call()
))
highestBidder = contract.functions.getHighestBidder(_id).call()
print('Highest Bid: {}'.format(web3.fromWei(contract.functions.getBid(_id,highestBidder).call(),"ether")))
print("Bid:")
bid = int(input()) 

tx_hash = contract.functions.bidForRide(_id).transact({'from':web3.eth.accounts[account],'value':web3.toWei(bid,"ether")})
web3.eth.waitForTransactionReceipt(tx_hash)
print("Successful biddding!")