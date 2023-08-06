import unittest

from fds import utils

class UtilsTest(unittest.TestCase):

  def test_rui_to_bucket_and_object(self):
    uri = "http://bucket1/object1"
    bucket, object = utils.uri_to_bucket_and_object(uri)
    self.assertEqual(bucket, None)
    self.assertEqual(object, None)

    uri = "fds://bucket1/object1"
    bucket, object = utils.uri_to_bucket_and_object(uri)
    self.assertEqual(bucket, "bucket1")
    self.assertEqual(object, "object1")

    uri = "fds://bucket1/folder1/folder2/object1"
    bucket, object = utils.uri_to_bucket_and_object(uri)
    self.assertEqual(bucket, "bucket1")
    self.assertEqual(object, "folder1/folder2/object1")

if __name__ == "__main__":
  unittest.main()

