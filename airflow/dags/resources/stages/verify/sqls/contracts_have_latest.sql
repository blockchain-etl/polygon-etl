SELECT
    if(
        (
            SELECT
                timestamp_diff(CURRENT_TIMESTAMP(), (
            SELECT
                MAX(block_timestamp)
            FROM
                `{{params.destination_dataset_project_id}}.{{params.dataset_name}}.contracts` AS contracts
            WHERE
                DATE(block_timestamp) >= date_add('{{ds}}', INTERVAL -1 DAY)), MINUTE)
        ) < {{ params.max_lag_in_minutes }},
        1,
        CAST(
            (
                SELECT
                    'Contracts are lagging by more than {{params.max_lag_in_minutes}} minutes'
            ) AS int64
        )
    )
