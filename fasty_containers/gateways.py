import sqlite3

import boto3
from dependency_injector import providers
from dependency_injector.containers import DeclarativeContainer


class Gateways(DeclarativeContainer):

    config = providers.Configuration()

    database_client = providers.Singleton(
        sqlite3.connect,
        config.database.dsn,
    )

    s3_client = providers.Singleton(
        boto3.client,
        service_name="s3",
        aws_access_key_id=config.aws.access_key_id,
        aws_secret_access_key=config.aws.secret_access_key,
    )
