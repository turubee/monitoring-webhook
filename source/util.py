import boto3
from datetime import datetime, timezone, timedelta

ssm = boto3.client('ssm')

def get_parameter_value(key_name):
    response = ssm.get_parameter(Name=key_name, WithDecryption=True)
    return response['Parameter']['Value']

def convert_timestamp_to_jst_iso(timestamp):
    if len(str(timestamp)) > 10:
        timestamp = int(timestamp) / 1000
    dt_utc = datetime.fromtimestamp(timestamp, timezone.utc)
    jst_offset = timezone(timedelta(hours=9))
    dt_jst = dt_utc.astimezone(jst_offset)
    return dt_jst.strftime('%Y-%m-%dT%H:%M:%S%z')
