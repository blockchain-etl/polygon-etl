
class EthTokenTransferV2Mapper(object):
    def token_transfer_to_dict(self, token_transfer_v2):
        return {
            'type': 'token_transfer_v2',
            'contract_address': token_transfer_v2.contract_address,
            'from_address': token_transfer_v2.from_address,
            'to_address': token_transfer_v2.to_address,
            'token_id': token_transfer_v2.token_id,
            'amount': token_transfer_v2.amount,
            'transaction_hash': token_transfer_v2.transaction_hash,
            'log_index': token_transfer_v2.log_index,
            'block_number': token_transfer_v2.block_number,
            'token_type' : token_transfer_v2.token_type,
            #todo: clean up the versioning logic
            'version': 'token_transfer_v2_0'
        }
