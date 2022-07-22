import boto3
# Access key ID,Secret access key
# AKIAS7SHGPQS4TK52EG7,ivEZe7V5QMthjihGTqeTDfROe6Yowrcx+HH2gXfO

session = boto3.Session(
    aws_access_key_id='AKIAS7SHGPQS4TK52EG7',
    aws_secret_access_key='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',
)
client = boto3.client(
    's3',
    aws_access_key_id='AKIAS7SHGPQS4TK52EG7',
    aws_secret_access_key='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'
)

s3 = boto3.resource('s3',
    aws_access_key_id='AKIAS7SHGPQS4TK52EG7',
    aws_secret_access_key='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')

for bucket in s3.buckets.all():
  print(bucket.name)
# client.cre
client.create_bucket(Bucket='fx-0001-2022-07-27')

fx=session.get_credentials()
print(session.region_name)