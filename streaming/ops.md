## Operations

To upgrade Helm release named `polygon-etl`:

```bash
helm upgrade polygon-etl charts/polygon-etl-streaming --values values.yaml
```

To delete a helm release run:

```
helm delete --purge polygon-etl
```