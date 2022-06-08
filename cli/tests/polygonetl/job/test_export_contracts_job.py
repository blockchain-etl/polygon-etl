# MIT License
#
# Copyright (c) 2018 Evgeny Medvedev, evge.medvedev@gmail.com
#
# Permission is hereby granted, free of charge, to any person obtaining a copy
# of this software and associated documentation files (the "Software"), to deal
# in the Software without restriction, including without limitation the rights
# to use, copy, modify, merge, publish, distribute, sublicense, and/or sell
# copies of the Software, and to permit persons to whom the Software is
# furnished to do so, subject to the following conditions:
#
# The above copyright notice and this permission notice shall be included in all
# copies or substantial portions of the Software.
#
# THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR
# IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY,
# FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE
# AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER
# LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM,
# OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN THE
# SOFTWARE.


import pytest

import tests.resources
from polygonetl.jobs.export_contracts_job import ExportContractsJob
from polygonetl.jobs.exporters.contracts_item_exporter import contracts_item_exporter
from polygonetl.thread_local_proxy import ThreadLocalProxy
from tests.helpers import (
    compare_lines_ignore_order,
    read_file,
    skip_if_slow_tests_disabled,
)
from tests.polygonetl.job.helpers import get_web3_provider

RESOURCE_GROUP = "test_export_contracts_job"


def read_resource(resource_group, file_name):
    return tests.resources.read_resource([RESOURCE_GROUP, resource_group], file_name)


@pytest.mark.parametrize(
    "batch_size,contract_addresses,output_format,resource_group,web3_provider_type",
    [
        (
            1,
            ["0x5d71998541ae48387f3664768deaf7d74898b75b"],
            "json",
            "erc20_contract",
            "mock",
        ),
        (
            1,
            ["0x1312dd389b08a8a5a60b0b058921386a13699267"],
            "json",
            "erc721_contract",
            "mock",
        ),
        (
            1,
            ["0x3afd673cd8406ef33812abd669b6f7d0f9ba2957"],
            "json",
            "non_token_contract",
            "mock",
        ),
        skip_if_slow_tests_disabled(
            (
                1,
                ["0x5d71998541ae48387f3664768deaf7d74898b75b"],
                "json",
                "erc20_contract",
                "online",
            )
        ),
        skip_if_slow_tests_disabled(
            (
                1,
                ["0x1312dd389b08a8a5a60b0b058921386a13699267"],
                "json",
                "erc721_contract",
                "online",
            )
        ),
        skip_if_slow_tests_disabled(
            (
                1,
                ["0x3afd673cd8406ef33812abd669b6f7d0f9ba2957"],
                "json",
                "non_token_contract",
                "online",
            )
        ),
    ],
)
def test_export_contracts_job(
    tmpdir,
    batch_size,
    contract_addresses,
    output_format,
    resource_group,
    web3_provider_type,
):
    contracts_output_file = str(tmpdir.join("actual_contracts." + output_format))

    job = ExportContractsJob(
        contract_addresses_iterable=contract_addresses,
        batch_size=batch_size,
        batch_web3_provider=ThreadLocalProxy(
            lambda: get_web3_provider(
                web3_provider_type,
                lambda file: read_resource(resource_group, file),
                batch=True,
            )
        ),
        max_workers=5,
        item_exporter=contracts_item_exporter(contracts_output_file),
    )
    job.run()

    print("=====================")
    print(read_file(contracts_output_file))
    compare_lines_ignore_order(
        read_resource(resource_group, "expected_contracts." + output_format),
        read_file(contracts_output_file),
    )
