
from polygonetl.executors.batch_work_executor import BatchWorkExecutor
from polygonetl.blockchainetl.jobs.base_job import BaseJob
from polygonetl.mappers.token_transfer_v2_mapper import EthTokenTransferV2Mapper
from polygonetl.mappers.receipt_log_mapper import EthReceiptLogMapper
from polygonetl.service.token_transfer_v2_extractor import EthTokenTransferV2Extractor

class ExtractTokenTransfersV2Job(BaseJob):
    def __init__(
            self,
            logs_iterable,
            batch_size,
            max_workers,
            item_exporter):
        self.logs_iterable = logs_iterable

        self.batch_work_executor = BatchWorkExecutor(batch_size, max_workers)
        self.item_exporter = item_exporter
        self.receipt_log_mapper = EthReceiptLogMapper()
        self.token_transfer_v2_mapper = EthTokenTransferV2Mapper()
        self.token_transfer_v2_extractor = EthTokenTransferV2Extractor()

    def _start(self):
        self.item_exporter.open()
      
    def _export(self):
        self.batch_work_executor.execute(self.logs_iterable, self._extract_transfers)

    def _extract_transfers(self, log_dicts):
        for log_dict in log_dicts:
            self._extract_transfer(log_dict)

    def _extract_transfer(self, log_dict):
        log = self.receipt_log_mapper.dict_to_receipt_log(log_dict)
        token_transfers_v2 = self.token_transfer_v2_extractor.extract_transfer_from_log(log)
        if token_transfers_v2 is not None:
            for token_transfer_v2 in token_transfers_v2:
                self.item_exporter.export_item(self.token_transfer_v2_mapper.token_transfer_to_dict(token_transfer_v2))

    def _end(self):
        self.batch_work_executor.shutdown()
        self.item_exporter.close()