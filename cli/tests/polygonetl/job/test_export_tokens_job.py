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
from polygonetl.jobs.export_tokens_job import ExportTokensJob
from polygonetl.jobs.exporters.tokens_item_exporter import tokens_item_exporter
from polygonetl.thread_local_proxy import ThreadLocalProxy
from polygonetl.web3_utils import build_web3
from tests.helpers import (
    compare_lines_ignore_order,
    read_file,
    skip_if_slow_tests_disabled,
)
from tests.polygonetl.job.helpers import get_web3_provider

RESOURCE_GROUP = "test_export_tokens_job"


def read_resource(resource_group, file_name):
    return tests.resources.read_resource([RESOURCE_GROUP, resource_group], file_name)


@pytest.mark.parametrize(
    "token_addresses,resource_group,web3_provider_type",
    [
        (["0xb0897686c545045afc77cf20ec7a532e3120e0f1"], "token_erc20", "mock"),
        (
            ["0x7d1afa7b718fb893db30a3abc0cfc608aacfebb0"],
            "token_invalid",
            "mock",
        ),
        skip_if_slow_tests_disabled(
            (
                ["0xb0897686c545045afc77cf20ec7a532e3120e0f1"],
                "token_erc20",
                "online",
            )
        ),
        skip_if_slow_tests_disabled(
            (
                ["0x7d1afa7b718fb893db30a3abc0cfc608aacfebb0"],
                "token_invalid",
                "online",
            )
        ),
    ],
)
def test_export_tokens_job(tmpdir, token_addresses, resource_group, web3_provider_type):
    output_file = str(tmpdir.join("tokens.csv"))

    job = ExportTokensJob(
        token_addresses_iterable=token_addresses,
        web3=ThreadLocalProxy(
            lambda: build_web3(
                get_web3_provider(
                    web3_provider_type, lambda file: read_resource(resource_group, file)
                )
            )
        ),
        item_exporter=tokens_item_exporter(output_file),
        max_workers=5,
    )
    job.run()

    compare_lines_ignore_order(
        read_resource(resource_group, "expected_tokens.csv"), read_file(output_file)
    )
