import time
import sys

from fds.fds_client_configuration import FDSClientConfiguration
from fds.galaxy_fds_client import GalaxyFDSClient
from fds.galaxy_fds_client_exception import GalaxyFDSClientException
from fds.model.permission import AccessControlList
from fds.model.permission import Grant
from fds.model.permission import Grantee
from fds.model.permission import Permission

# Create default client
access_key = 'none'
access_secret = 'none'
config = FDSClientConfiguration()
bucket_name = 'fds-python-example-%d' % int(time.time())

fds_client = GalaxyFDSClient(access_key, access_secret, config)

#####################
# List buckets and delete them all !!!!!!
buckets = fds_client.list_buckets()
print('buckets list:')
for bucket in buckets:
  result = fds_client.list_objects(bucket)
  if result.is_truncated:
    while result.is_truncated:
      result = fds_client.list_next_batch_of_objects(result)
      for object_summary in result.objects:
        fds_client.delete_object(bucket,object_summary.object_name)
  else:
    for object_summary in result.objects:
      fds_client.delete_object(bucket,object_summary.object_name)
  fds_client.delete_bucket(bucket)