import io
import logging
import requests
import gzip
import google.cloud.storage as storage

def upload_file(source_file, destination_name):

    gcloud_bucket_name = "upload_covid_data_kabum-case-project"

    storage_client = storage.Client()

    bucket = storage_client.get_bucket(bucket_or_name=gcloud_bucket_name)

    blob = bucket.blob(destination_name)

    blob.upload_from_string(source_file)

    return print(f"file sent to {destination_name}")

def setup_upload(request):
    
    url_casos_file = "https://data.brasil.io/dataset/covid19/caso.csv.gz"

    casos_file = requests.get(url=url_casos_file, stream=True)

    decompress_casos = gzip.decompress(casos_file.content)

    try:
        upload_file(decompress_casos.decode("utf-8"), "caso.csv")

    except Exception as e:
        logging.error(f'Falha em carregar arquivo casos: {e}')
    
    url_obitos_file = "https://data.brasil.io/dataset/covid19/obito_cartorio.csv.gz"

    obitos_file = requests.get(url=url_obitos_file, stream=True)

    decompress_obitos = gzip.decompress(obitos_file.content)

    try:
        upload_file(decompress_obitos.decode("utf-8"), "obito_cartorio.csv")
        return print("Arquivos carregados no Bucket")
    
    except Exception as e:
        logging.error(f'Falha em carregar arquivo obitos: {e}')
