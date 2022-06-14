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

import json

import pytest

import tests.resources
from polygonetl.jobs.exporters.tokens_item_exporter import tokens_item_exporter
from polygonetl.jobs.extract_tokens_job import ExtractTokensJob
from polygonetl.thread_local_proxy import ThreadLocalProxy
from polygonetl.web3_utils import build_web3
from tests.helpers import (
    compare_lines_ignore_order,
    read_file,
    skip_if_slow_tests_disabled,
)
from tests.polygonetl.job.helpers import get_web3_provider

RESOURCE_GROUP = "test_extract_tokens_job"


def read_resource(resource_group, file_name):
    return tests.resources.read_resource([RESOURCE_GROUP, resource_group], file_name)


@pytest.mark.parametrize(
    "resource_group,web3_provider_type",
    [
        ("erc20_and_non_token_contracts", "mock"),
        skip_if_slow_tests_disabled(("erc20_and_non_token_contracts", "online")),
    ],
)
def test_export_tokens_job(tmpdir, resource_group, web3_provider_type):
    output_file = str(tmpdir.join("actual_tokens.csv"))

    contracts_content = read_resource(resource_group, "contracts.json")
    contracts_iterable = (json.loads(line) for line in contracts_content.splitlines())

    job = ExtractTokensJob(
        contracts_iterable=contracts_iterable,
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
