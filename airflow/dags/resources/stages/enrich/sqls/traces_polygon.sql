with traces as (
    select *
    from nansen-dev.adhoc.polygon_traces_new_2020
    union all
    select *
    from nansen-dev.adhoc.polygon_traces_new_2021
    union all
    select *
    from nansen-dev.adhoc.polygon_traces_new_2022
    union all
    select *
    from nansen-dev.adhoc.polygon_traces_new_2023
)

SELECT
    transactions.`hash` as transaction_hash,
    traces.transaction_index,
    traces.from_address,
    traces.to_address,
    traces.value,
    traces.input,
    traces.output,
    traces.trace_type,
    traces.call_type,
    traces.reward_type,
    traces.gas,
    traces.gas_used,
    traces.subtraces,
    traces.trace_address,
    traces.error,
    traces.status,
    traces.trace_id,
    blocks.timestamp AS block_timestamp,
    blocks.number AS block_number,
    blocks.hash AS block_hash
FROM public-data-finance.crypto_polygon.blocks AS blocks
    JOIN traces ON blocks.number = traces.block_number
    JOIN public-data-finance.crypto_polygon.transactions AS transactions
        ON traces.transaction_index = transactions.transaction_index
            and traces.block_number = transactions.block_number



