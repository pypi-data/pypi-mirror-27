import json
import unittest
from nose.tools import assert_equal
import server

class FlaskrTestCase(unittest.TestCase):

    def setUp(self):
        server.app.testing = True
        self.app = server.app.test_client()

    def tearDown(self):
        # remove db.pickle?
        pass

    def test_roundtrip(self):
        r = self.app.put('/badge/user/repo/subject',
            data=json.dumps(dict(status="mayday", color="cyan")),
            content_type='application/json')
        assert_equal(r.data, b"OK")
        r = self.app.get('/badge/user/repo/subject.svg')
        print(r.data)
        assert_equal(r.status_code, 307)
        assert_equal(r.headers['Location'], 'https://img.shields.io/badge/subject-mayday-cyan.svg')
    
    def test_404(self):
        r = self.app.put('/nope', data={})
        assert_equal(r.status_code, 404)

if __name__ == '__main__':
    unittest.main()
