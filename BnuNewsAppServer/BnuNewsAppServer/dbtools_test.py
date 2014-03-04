#!/usr/bin/env python
# -*- coding: utf-8 -*-
'''
Created on 2010-10-30

'''
import unittest
import dbtools
from datetime import datetime

class DBTest(unittest.TestCase):
    db = dbtools.DB()
    default_email = 'test@gmail.com'
    default_password = '111111'
    default_name = 'test'
    default_usertype = '1'

    def setUp(self):
        self.num_user = self.get_num_of_elem('user')

        # add default test user
        self.default_userid = self.db.add_user(self.default_email,
                                               self.default_password,
                                               self.default_name,
                                               self.default_usertype)

    def tearDown(self):
        """
        ensure that there's no change for database after the test
        """
        # remove default test user
        self.remove_by_id('user', self.default_userid)
        if self.num_user != self.get_num_of_elem('user'):
            raise self.failureException(
                "expected %d, get %d" % (self.num_user, 
                                         self.get_num_of_elem('user')))

    def get_num_of_elem(self, collection_name):
        return self.db.get_collection(collection_name).find().count()

    def get_by_id(self, collection_name, object_id):
        return self.db.get_collection(collection_name).find_one({'_id':object_id})

    def remove_by_id(self, collection_name, object_id):
        self.db.get_collection(collection_name).remove({'_id':object_id})

    #===============================================================================
    # base operations
    #===============================================================================
    def test_get_db(self):
        self.assertTrue(self.db.get_db(self.db._db_name),
                             'Can not access %s' % (self.db._db_name))

    def test_get_connection(self):
        self.assertTrue(self.db.get_collection('test'))
        result = self.db.get_db(self.db._db_name).command('getLastError')
        self.assertTrue(result['ok'])

    #===============================================================================
    # user operations
    #===============================================================================
    def test_add_user(self):
        user = self.get_by_id('user', self.default_userid)
        self.assertEqual(user['email'], self.default_email, 'email mismatch')
        self.assertEqual(user['password'], self.default_password, 'password mismatch')
        self.assertEqual(user['name'], self.default_name, 'name mismatch')
        self.assertEqual(user['usertype'], self.default_usertype, 'usertype mismatch')
        
    def test_login(self):
        self.assertTrue(self.db.login(self.default_email, self.default_password) is not None, 'login error')
        


if __name__ == "__main__":
    #import sys;sys.argv = ['', 'Test.testName']
    unittest.main()
