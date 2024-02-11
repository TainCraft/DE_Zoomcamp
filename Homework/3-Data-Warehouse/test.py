import os
import requests
from google.cloud import storage

BUCKET = os.environ.get("GCP_GCS_BUCKET", "mage-zoomcamp-sl2")
INIT_URL = 'https://d37ci6vzurychx.cloudfront.net/trip-data/'

def upload_to_gcs(bucket, object_name, local_file):
    client = storage.Client()
    bucket = client.bucket(bucket)
    blob = bucket.blob(object_name)
    blob.upload_from_filename(local_file)

def web_to_gcs(year, service):
    for i in range(12):
        month = str(i+1).zfill(2)  # Ensure two digits for month
        file_name = f"{service}_tripdata_{year}-{month}.parquet"

        request_url = f"{INIT_URL}{file_name}"
        r = requests.get(request_url)

        if r.status_code == 200:
            with open(file_name, 'wb') as f:
                f.write(r.content)
            print(f"Local: {file_name}")
            upload_to_gcs(BUCKET, f"{service}/{file_name}", file_name)
            print(f"GCS: {service}/{file_name}")
        else:
            print(f"Failed to download {file_name}")

web_to_gcs('2022', 'green')
