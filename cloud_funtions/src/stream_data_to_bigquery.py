import google.cloud.storage as storage
import google.cloud.bigquery as bq
import os

def stream_data_to_bigquery(data, context):

    dataset = os.environ.get('DATASET', 'covid')
    bucket_name = data['bucket']
    file_name = data['name']
    table_name = str(data['name']).split(".")[0]
    storage_client = storage.Client()
    bucket = storage_client.get_bucket(bucket_or_name=bucket_name)
    blob = bucket.get_blob(blob_name=file_name)
    uri = f'gs://{bucket_name}/{file_name}'

    bq_client = bq.Client()
    dataset_ref = bq_client.dataset(dataset)

    load_job_config = bq.LoadJobConfig()
    load_job_config.autodetect = True
    load_job_config.schema_update_options = [
        bq.SchemaUpdateOption.ALLOW_FIELD_ADDITION
    ]
    load_job_config.create_disposition = [
        bq.CreateDisposition.CREATE_IF_NEEDED
    ]

    if str(file_name).lower().endswith('.csv'):
        load_job_config.source_format = bq.SourceFormat.CSV
    else:
        return print('Arquivo não é um CSV e não será importado')
    
    load_job_config.write_disposition = bq.WriteDisposition.WRITE_TRUNCATE

    load_job = bq_client.load_table_from_uri(
        source_uris=uri,
        destination=dataset_ref.table(table_name),
        job_config=load_job_config
    )

    print(f'Iniciando processo {load_job.job_id}')

    load_job.result()
    print('Processo finalizado')

    table_loaded = bq_client.get_table(dataset_ref.table(table_name))
    print(f'Dados carregados na tabela {table_name}. Linhas inseridas {table_loaded.num_rows}')

    

