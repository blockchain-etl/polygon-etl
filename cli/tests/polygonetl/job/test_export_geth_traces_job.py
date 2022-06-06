# MIT License
#
# Copyright (c) 2018 Evgeniy Filatov, evgeniyfilatov@gmail.com
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
from polygonetl.jobs.export_geth_traces_job import ExportGethTracesJob
from polygonetl.jobs.exporters.geth_traces_item_exporter import (
    geth_traces_item_exporter,
)
from polygonetl.thread_local_proxy import ThreadLocalProxy

import tests.resources
from tests.helpers import (
    compare_lines_ignore_order,
    read_file,
    skip_if_slow_tests_disabled,
)
from tests.polygonetl.job.helpers import get_web3_provider

# use same resources for testing export/extract jobs
RESOURCE_GROUP = "test_extract_geth_traces_job"


def read_resource(resource_group, file_name):
    return tests.resources.read_resource([RESOURCE_GROUP, resource_group], file_name)


@pytest.mark.parametrize(
    "start_block,end_block,resource_group,web3_provider_type",
    [
        (1, 1, "block_without_transactions", "mock"),
        (1000690, 1000690, "block_with_create", "mock"),
        (1011973, 1011973, "block_with_suicide", "mock"),
        (1000000, 1000000, "block_with_subtraces", "mock"),
        (1000895, 1000895, "block_with_error", "mock"),
        # (829, 829, "block_with_create_online", "mock"),
        # skip_if_slow_tests_disabled((829, 829, "block_with_create_online", "online")),
    ],
)
def test_export_geth_traces_job(
    tmpdir, start_block, end_block, resource_group, web3_provider_type
):
    traces_output_file = str(tmpdir.join("actual_geth_traces.json"))

    job = ExportGethTracesJob(
        start_block=start_block,
        end_block=end_block,
        batch_size=1,
        batch_web3_provider=ThreadLocalProxy(
            lambda: get_web3_provider(
                web3_provider_type,
                lambda file: read_resource(resource_group, file),
                batch=True,
            )
        ),
        max_workers=5,
        item_exporter=geth_traces_item_exporter(traces_output_file),
    )
    job.run()

    compare_lines_ignore_order(
        read_resource(resource_group, "geth_traces.json"), read_file(traces_output_file)
    )