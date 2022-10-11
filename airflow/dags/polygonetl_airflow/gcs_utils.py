MEGABYTE = 1024 * 1024


def upload_to_gcs(gcs_hook, bucket, object, filename):
    """Upload a file to GCS."""
    service = gcs_hook.get_conn()
    bucket = service.get_bucket(bucket)
    blob = bucket.blob(object, chunk_size=10 * MEGABYTE)
    blob.upload_from_filename(filename)


def download_from_gcs(bucket, object, filename):
    """Download a file from GCS. Can download big files unlike gcs_hook.download which saves files in memory first"""
    from google.cloud import storage

    storage_client = storage.Client()

    bucket = storage_client.get_bucket(bucket)
    blob_meta = bucket.get_blob(object)

    if blob_meta.size > 10 * MEGABYTE:
        blob = bucket.blob(object, chunk_size=10 * MEGABYTE)
    else:
        blob = bucket.blob(object)

    blob.download_to_filename(filename)
