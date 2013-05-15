#!/usr/bin/env python

import os
import persona.index as persona
import unittest
import tempfile

class PersonaTestCase(unittest.TestCase):

    def setUp(self):
        print 'SETTING UP'
        #self.db_fd, persona.app.config['DATABASE'] = tempfile.mkstemp()
        persona.app.config['TESTING'] = True
        self.app = persona.app.test_client()
        #persona.init_db()

    def tearDown(self):
        #os.close(self.db_fd)
        #os.unlink(persona.app.config['DATABASE'])
        print 'TEARING DOWN'

    def test_home(self):
        rv = self.app.get('/')
        assert 'Welcome' in rv.data

    def test_login_page(self):
        rv = self.app.get('/login')
        assert 'Login' in rv.data


if __name__ == '__main__':
    unittest.main()
