select if(
(
  select count(*) - (max(number) - min(number) + 1)
  from `{{params.destination_dataset_project_id}}.{{params.dataset_name}}.blocks` as blocks
  where date(timestamp) >= date_add('{{ds}}', INTERVAL -1 DAY)
) between -8 and 8, 1,
cast((select 'There are more than 8 missing or duplicate blocks') as INT64))