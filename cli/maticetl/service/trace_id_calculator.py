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

from collections import defaultdict


def calculate_trace_ids(traces):
    # group by block
    traces_grouped_by_block = defaultdict(list)
    for trace in traces:
        traces_grouped_by_block[trace.block_number].append(trace)

    # calculate ids for each block number
    for block_traces in traces_grouped_by_block.values():
        calculate_transaction_scoped_trace_ids(block_traces)

    return traces


def calculate_transaction_scoped_trace_ids(traces):
    for trace in traces:
        trace.trace_id = concat(trace.trace_type, trace.block_number, trace.transaction_index, trace_address_to_str(trace.trace_address))


def trace_address_to_str(trace_address):
    if trace_address is None or len(trace_address) == 0:
        return ''

    return '_'.join([str(address_point) for address_point in trace_address])


def concat(*elements):
    return '_'.join([str(elem) for elem in elements])
