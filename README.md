# UDEND Sparkify Data Pipeline Project with Apache Airflow
The purpose of this project is to build a dynamic ETL data pipeline that utilizes automation and monitoring. The data pipeline is built from reusable tasks allows for easy backfills. It utilizes custom operators to perform tasks  such as staging the data, filling the data warehouse, and running a check on the data as the final step so as to to catch any discrepancies in the datasets.

## Database Schema Design
The project comprises of a redshift postgres database in the cluster with staging tables that contain all the data retrieved from the s3 bucket and copied over to the tables. It also contains a fact table `songplays` and four dimensional tables namely `users`, `songs`, `artists` and `time`. This will store data from the staging tables that has been transformed to provide the relevant data in the tables.

## ETL Pipeline
The pipeline utilizes one main dag that contains several tasks that call four custom operators. These operators are:
```
Stage Operator - Loads any JSON formatted files from S3 to Amazon Redshift.
Fact Operator - Utilizes the provided SQL helper class to run data transformations for the facts table.
Dimension Operator - Utilizes the provided SQL helper class to run data transformations for the dimension tables.
Data Quality Operator - Runs checks on the data itself.
```

The data gets that gets extracted will need to be transformed to to fit the data model in the target destination tables. For instance the source data for timestamp is in unix format and that will need to be converted to timestamp from which the year, month, day, hour values etc can be extracted which will fit in the relevant target time and songplays table columns. The script will also need to cater for duplicates, ensuring that they aren't part of the final data that is loaded in the tables.

## Datasets used
The datasets used are retrieved from the s3 bucket and are in the JSON format. There are two datasets namely `log_data` and `song_data`. The `song_data` dataset is a subset of the the [Million Song Dataset](http://millionsongdataset.com/) while the `log_data` contains generated log files based on the songs in `song_data`.

## Getting Started
In order to have a copy of the project up and running locally, you will need to take note of the following:

### Prerequisites
   - Python 2.7 or greater.
   - AWS Account.

### Installation
   - Follow the instructions given [here](https://www.ryanmerlin.com/2019/07/apache-airflow-installation-on-ubuntu-18-04-18-10/) to setup apache airflow locally.
   - After setting up airflow, run  the commands `airflow scheduler` and `airflow webserver` which will spin up the web server on localhost using port 8080 http://0.0.0.0:8080
   - Create a redshift cluster.
   - Retrieve your `AWS_ACCESS_KEY_ID` and `AWS_SECRET_ACCESS_KEY` and add them well as your redshift database credentials to `Connections` on the Admin tab of the airflow UI.
   - You can then go ahead and Trigger the DAG and sit back and watch as the magic happens.

## Built With
- Python and Apache Airflow.

## Authors
- Jonathan Kamau - [Github Profile](https://github.com/jonathankamau)


