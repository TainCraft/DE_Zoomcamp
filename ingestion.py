import argparse
import pandas as pd
from time import time
import os
from sqlalchemy import create_engine

def main(params):
    user = params.user
    password = params.password
    host = params.host
    port = params.port
    db = params.db
    table_name = params.table_name
    url = params.url 
    
    #download parquet file 

    csv_file = 'output.csv'
    os.system(f"wget {url} -O {csv_file}")

    engine = create_engine(f'postgresql://{user}:{password}@{host}:{port}/{db}') #defining connection between script and database
    engine.connect()
    print('engine connected!')
    df = pd.read_csv(csv_file, compression="gzip")

    df['lpep_pickup_time'] = pd.to_datetime(df.lpep_pickup_datetime).dt.time
    df['lpep_dropoff_time'] = pd.to_datetime(df.lpep_dropoff_datetime).dt.time
    df['lpep_pickup_date'] = pd.to_datetime(df.lpep_pickup_datetime).dt.date
    df['lpep_dropoff_date'] = pd.to_datetime(df.lpep_dropoff_datetime).dt.date

#ingesting zones tablen
    zone_file='zones.csv'
    lookup_zone="https://s3.amazonaws.com/nyc-tlc/misc/taxi+_zone_lookup.csv"
    os.system(f"wget {lookup_zone} -O {zone_file}")
    df_zones=pd.read_csv(zone_file)
    df_zones.to_sql(name='taxi_lookup_zone', con=engine, if_exists='append')
    print('taxi zones table created!')

 #   print(pd.io.sql.get_schema(df, name='yellow_tripdata_2021-01.parquet', con=engine)) #Adjusting schema/datatypes as per database
    print('processing green_taxi dataset...')
    t_start=time()
    df.to_sql(name=table_name, con=engine, if_exists='append') #putting into database
    t_end=time()
    print('done in %.3f seconds' % (t_end - t_start))
    

if __name__ == '__main__':

    parser = argparse.ArgumentParser(description='Ingest Parquet data to Postgres')

    parser.add_argument('--user', help='user name for postgres')   
    parser.add_argument('--password', help='password for postgres')
    parser.add_argument('--host', help='host for postgres')
    parser.add_argument('--port', help='port for postgres')
    parser.add_argument('--db', help='database name for postgres')
    parser.add_argument('--table_name', help='name of the table where we will write the results to')
    parser.add_argument('--url', help='url of the dataset file')

    args = parser.parse_args()

    main(args)