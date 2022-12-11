import unittest
from depot.io.gridfs import GridFSStorage

FILE_CONTENT = b'HELLO WORLD'


class TestGridFSFileStorage(unittest.TestCase):
    def setUp(self):
        try:
            import pymongo.errors
            self.fs = GridFSStorage('mongodb://localhost/gridfs_example?serverSelectionTimeoutMS=0', 'testfs')
            self.fs._gridfs.exists("")  # Any operation to test that mongodb is up.
        except pymongo.errors.ConnectionFailure:
            self.skipTest('MongoDB not running')

    def tearDown(self):
        self.fs._db.drop_collection('testfs')

    def test_fileoutside_depot(self):
        fileid = self.fs._gridfs.put(FILE_CONTENT)

        f = self.fs.get(str(fileid))
        assert f.read() == FILE_CONTENT
