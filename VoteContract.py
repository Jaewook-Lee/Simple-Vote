import json
import time
from web3 import Web3, HTTPProvider
from web3.exceptions import ContractLogicError


# truffle ganache blockchain address
block_address = "http://127.0.0.1:7545"
# client instance to interact with the blockchain
web3 = Web3(HTTPProvider(block_address))
# set the default account
web3.eth.defaultAccount = web3.eth.accounts[1]
# path to the compiled contract JSON File
compiled_contract_path = "build/contracts/Vote.json"
# deployed contract address(see 'truffle migrate' command output: 'contract address')
deployed_contract_address = "0xb95AeC04A5727E9Ef08ed51078b7dbbA607bf45f"

with open(compiled_contract_path) as file:
    contract_json = json.load(file)
    contract_abi = contract_json['abi']    # fetch contract's abi -> necessary to call


class VoteContract:
    def __init__(self):
        # fetch deployed contract reference
        self.contract = web3.eth.contract(address=deployed_contract_address, abi=contract_abi)

    def do_vote(self, _idx):
        try:
            # If you want to update value, use 'transact'!
            self.contract.functions.vote(_idx, int(time.time())).transact({'from': web3.eth.defaultAccount})
        except ContractLogicError as cle:
            err_reason = cle.__str__().split(':')[-1].strip()
            if err_reason == "revert Time Over":
                print("투표 시간이 종료됐습니다.")
            elif err_reason == "revert Already Voted":
                print("이미 투표하셨습니다.")
            return False
        return True

    def get_winner_name(self):
        try:
            # If you want to read value, use 'call'! Return value will be bytecodes.
            winner_name = self.contract.functions.giveWinnerName(int(time.time())).call().replace(b'\x00', b'').decode()
        except ContractLogicError as cle:
            print("투표가 아직 끝나지 않았습니다.")
            return ""
        return winner_name
