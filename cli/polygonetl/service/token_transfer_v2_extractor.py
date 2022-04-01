
# https://ethereum.stackexchange.com/questions/12553/understanding-logs-and-log-blooms
import logging
from builtins import map

from polygonetl.domain.token_transfer_v2 import EthTokenTransferV2
from polygonetl.utils import chunk_string, hex_to_dec, to_normalized_address


# ERC721_ERC_20_TRANSFER_TOPIC is the event signature for a `Transfer(address,address,uint256)`. It is the same for ERC20 and ERC721 transfer.
ERC721_ERC_20_TRANSFER_TOPIC = "0xddf252ad1be2c89b69c2b068fc378daa952ba7f163c4a11628f55a4df523b3ef"
# ERC1155_TRANSFER_SINGLE_TOPIC is the event signature for `TransferSingle(address,address,address,uint256,uint256)`.
ERC1155_TRANSFER_SINGLE_TOPIC = "0xc3d58168c5ae7397731d063d5bbf3d657854427343f4c083240f7aacaa2d0f62"
# ERC1155_TRANSFER_BATCH_TOPIC is the event signature for a `TransferBatch(address,address,address,uint256[],uint256[])`.
ERC1155_TRANSFER_BATCH_TOPIC = "0x4a39dc06d4c0dbc64b70af90fd698a233a518aa5d07e595d983b8c0526c8f7fb"

TRANSFER_EVENT_TOPICS = [ERC721_ERC_20_TRANSFER_TOPIC, ERC1155_TRANSFER_SINGLE_TOPIC, ERC1155_TRANSFER_BATCH_TOPIC]

logger = logging.getLogger(__name__)


class EthTokenTransferV2Extractor(object):
    def extract_transfer_from_log(self, receipt_log):
        topics = receipt_log.topics
        if topics is None or len(topics) < 1:
            # This is normal, topics can be empty for anonymous events
            return None
        
        # Handle un-indexed event fields
        topics_with_data = topics + split_to_words(receipt_log.data)

        if topics[0] == ERC721_ERC_20_TRANSFER_TOPIC:
            # if the number of topics and fields in data part != 4, then it's a weird event
            if len(topics_with_data) != 4:
                logger.warning("The number of topics and data parts is not equal to 4 in log {} of transaction {}"
                               .format(receipt_log.log_index, receipt_log.transaction_hash))
                return None
            
            #ERC20 only has three topics - 1) signature hash 2) from_address 3) to_address
            if len(topics) == 3:
                return [build_token_transfer(
                    receipt_log,
                    from_address=word_to_address(topics_with_data[1]),
                    to_address=word_to_address(topics_with_data[2]),
                    token_id="0x0000000000000000000000000000000000000000000000000000000000000001",
                    amount=topics_with_data[3],
                    token_type="ERC20")]
            else:
                return [build_token_transfer(
                    receipt_log,
                    from_address=word_to_address(topics_with_data[1]),
                    to_address=word_to_address(topics_with_data[2]),
                    token_id=topics_with_data[3],
                    amount="0x0000000000000000000000000000000000000000000000000000000000000001",
                    token_type="ERC721")]
           
        elif topics[0] == ERC1155_TRANSFER_SINGLE_TOPIC:
            if len(topics_with_data) != 6:
                logger.warning("The number of topics and data parts is not equal to 6 in log {} of transaction {}"
                               .format(receipt_log.log_index, receipt_log.transaction_hash))
                return None

            return [build_token_transfer(
                receipt_log,
                from_address=word_to_address(topics_with_data[2]),
                to_address=word_to_address(topics_with_data[3]),
                token_id=topics_with_data[4],
                amount=topics_with_data[5],
                token_type="ERC1155")]
        
        elif topics[0] == ERC1155_TRANSFER_BATCH_TOPIC:
            #todo cleanup
            if len(topics_with_data) <= 10:
                logger.warning("The number of topics and data parts is not equal to or greater than 10 in log {} of transaction {}"
                               .format(receipt_log.log_index, receipt_log.transaction_hash))
                return None

            #todo: write it properly
            size = hex_to_dec(topics_with_data[6])
            token_ids = topics_with_data[7: 7 + size]
            amounts = topics_with_data[1 + 7 + size:]

            token_transfers = []
            for token_id, amount in zip(token_ids, amounts):
                token_transfers.append(build_token_transfer(
                    receipt_log,
                    from_address=word_to_address(topics_with_data[2]),
                    to_address=word_to_address(topics_with_data[3]),
                    token_id=token_id,
                    amount=amount,
                    token_type="ERC1155"))
            return token_transfers
        else:
            return None

def build_token_transfer(receipt_log, from_address, to_address, token_id, amount, token_type):
    token_transfer = EthTokenTransferV2()
    token_transfer.contract_address = to_normalized_address(receipt_log.address)
    token_transfer.transaction_hash = receipt_log.transaction_hash
    token_transfer.log_index = receipt_log.log_index
    token_transfer.block_number = receipt_log.block_number
    token_transfer.from_address = from_address
    token_transfer.to_address = to_address
    token_transfer.token_id = token_id
    token_transfer.amount = amount
    token_transfer.token_type = token_type
    
    return token_transfer

def split_to_words(data):
    if data and len(data) > 2:
        data_without_0x = data[2:]
        words = list(chunk_string(data_without_0x, 64))
        words_with_0x = list(map(lambda word: '0x' + word, words))
        return words_with_0x
    return []


def word_to_address(param):
    if param is None:
        return None
    elif len(param) >= 40:
        return to_normalized_address('0x' + param[-40:])
    else:
        return to_normalized_address(param)
