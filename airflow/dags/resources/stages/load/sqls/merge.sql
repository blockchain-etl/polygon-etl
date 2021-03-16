merge `{{destination_dataset_project_id}}.{{destination_dataset_name}}.{{table}}` dest
using {{dataset_name_temp}}.{{table}} source
on false
when not matched and date(timestamp) = '{{ds}}' then
insert (
    {% for column in table_schema %}
    {% if loop.index0 > 0 %},{% endif %}`{{ column.name }}`
    {% endfor %}
) values (
    {% for column in table_schema %}
    {% if loop.index0 > 0 %},{% endif %}`{{ column.name }}`
    {% endfor %}
)
when not matched by source and date(timestamp) = '{{ds}}' then
delete
