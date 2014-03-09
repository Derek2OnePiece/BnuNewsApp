#!/usr/bin/env python
# -*- coding: utf-8 -*-
'''
Created on 2010-10-30

'''
import unittest
import dbtools


class DBTest(unittest.TestCase):
    db = dbtools.DB()
    default_email = 'test@gmail.com'
    default_password = '111111'
    default_name = 'test'
    default_usertype = '1'
    
    default_news_type = '1'
    default_tilte = 'News for Test'
    default_body = r'一个二年级的农村学生，能够阅读简写版的《三国演义》'
    default_author = r'bnu teacher'
    

    def setUp(self):
        self.num_user = self.get_num_of_elem('user')
        self.num_news = self.get_num_of_elem('news')

        # add default test user
        self.default_user_id = self.db.add_user(self.default_email,
                                                self.default_password,
                                                self.default_name,
                                                self.default_usertype)
        # add default test news
        self.default_news_id = self.db.add_news(self.default_news_type,
                                                self.default_title,
                                                self.default_body,
                                                self.default_author,
                                                self.default_user_id)

    def tearDown(self):
        """
        ensure that there's no change for database after the test
        """
        # remove default test user
        self.remove_by_id('user', self.default_user_id)
        self.remove_by_id('news', self.default_news_id)
        
        if self.num_user != self.get_num_of_elem('user'):
            raise self.failureException(
                "user expected %d, get %d" % (self.num_user, 
                                              self.get_num_of_elem('user')))
        if self.num_news != self.get_num_of_elem('news'):
            raise self.failureException(
                "news expected %d, get %d" % (self.num_news,
                                              self.get_num_of_elem('news')))
            

    def get_num_of_elem(self, collection_name):
        return self.db.get_collection(collection_name).find().count()

    def get_by_id(self, collection_name, object_id):
        return self.db.get_collection(collection_name).find_one({'_id':object_id})

    def remove_by_id(self, collection_name, object_id):
        self.db.get_collection(collection_name).remove({'_id':object_id})

    #==========================================================================
    # base operations
    #==========================================================================
    def test_get_db(self):
        self.assertTrue(self.db.get_db(self.db._db_name),
                             'Can not access %s' % (self.db._db_name))

    def test_get_connection(self):
        self.assertTrue(self.db.get_collection('test'))
        result = self.db.get_db(self.db._db_name).command('getLastError')
        self.assertTrue(result['ok'])

    #==========================================================================
    # user operations
    #==========================================================================
    """
    def test_add_user(self):
        user = self.get_by_id('user', self.default_userid)
        self.assertEqual(user['email'], self.default_email, 'email mismatch')
        self.assertEqual(user['password'], self.default_password, 'password mismatch')
        self.assertEqual(user['name'], self.default_name, 'name mismatch')
        self.assertEqual(user['usertype'], self.default_usertype, 'usertype mismatch')
    """ 
    def test_login(self):
        self.assertTrue(self.db.login(self.default_email, self.default_password) is not None, 'login error')
        
    #==========================================================================
    # news operations
    #==========================================================================
    

if __name__ == "__main__":
    #import sys;sys.argv = ['', 'Test.testName']
    unittest.main()
