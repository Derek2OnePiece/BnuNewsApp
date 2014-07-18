#!/usr/bin/env python
# -*- coding: utf-8 -*-
'''
Created on 2010-10-30

'''
import sys
import dbtools


class UploadTestData():
    db = dbtools.DB()

    def upload(self):
        # self.upload_user()
        self.upload_admin()
        # self.upload_news_1()
        # self.upload_news_2()
        # self.upload_news_3()

    #==========================================================================
    # user operations
    #==========================================================================
    def upload_user(self):
        self.default_email = r'xxxx@bnu.edu.cn'
        if not self.db.check_user_exist_by_email(self.default_email):
            self.db.add_user(email = self.default_email,
                             password = r'xxxxxx',
                             name = r'北京师范大学',
                             user_type = r'1', )
    
    def upload_admin(self, ):
        self.default_admin_email = r'admin2014@bnu.edu.cn'
        if not self.db.check_user_exist_by_email(self.default_admin_email):
            self.db.add_user(email = self.default_admin_email,
                             password = r'admin2014bnu',
                             name = r'北京师范大学党委宣传部',
                             user_type = r'2',
                             is_admin = 1, )
        
    #==========================================================================
    # news operations
    #==========================================================================
    def upload_news_1(self):
        news_type = 0
        title = r'【京师人物】何克抗：蓄力十年“助跑”农村娃'
        abstract = r'一个二年级的农村学生，能够阅读简写版的《三国演义》'
        body = r'“一个二年级的农村学生，能够阅读简写版的《三国演义》？能手写出150字以上结构完整、通顺流畅的文章？”在“最不适合人类居住”的宁夏西海固地区农村教师眼中这简直是天方夜谭。然而，这么不可思议的事情却真实地发生在这片土地上。'
        author = r'北京师范大学'
        module = 5
        pub_status = 1
        is_delete = 0
        inner_pic_sub_url = r'test_inner_pic_1.jpg'
        self.db.admin_add_news(news_type, title, abstract, author, module,
                         pub_status, is_delete, body, inner_pic_sub_url)
        
    def upload_news_2(self):
        news_type = 1
        title = r'2013“Looking China”中外青年暑期DV计划硕果累累'
        abstract = r'“Looking China”中外青年暑期DV计划'
        body = r'7月12日，由我校中国文化国际传播研究院主办的2013“Looking China”中外青年暑期DV计划，在中国电影资料馆艺术影院举行展映暨颁奖仪式。北京师范大学副校长陈光巨，中国文化传播研究院负责同志、创作委员会和学术委员会委员、客座研究员等出席了仪式。'
        author = r'北京师范大学'
        module = 3
        pub_status = 1
        is_delete = 0
        inner_pic_sub_url = r'test_inner_pic_2.jpg'
        video_target_url = r'http://v.youku.com/v_show/id_XNjgxNzM4MzU2.html'
        self.db.admin_add_news(news_type, title, abstract, author, module,
                         pub_status, is_delete, body, inner_pic_sub_url,
                         video_target_url, )
        
    def upload_news_3(self):
        news_type = 1
        title = r'【中外名师】“看中国”让中国文化走向世界'
        abstract = r'波士顿大学教授山姆•考夫曼与来自不同国家的同学们在一起讨论影片的后期剪辑'
        body = r'中国文化国际传播研究院院长黄会林  黄会林认为，尽管语言不同、文化各异，但是人类在面临世界变化的时候拥有相似的感受，这使得来自不同文化区域的人们能够相互沟通、相互学习。中国一直以一种开放和包容的态度对待译制的文化，早在四百年前中国的科学家徐光启就提出过一句话，叫“慧慧通以求超胜”，意为不同文化之间互相有相互学习才能够进步。北京师范大学副校长陈光巨，中国文化传播研究院负责同志、创作委员会和学术委员会委员、客座研究员等出席了仪式。'
        author = r'北京师范大学'
        module = 4
        pub_status = 1
        is_delete = 0
        inner_pic_sub_url = r'test_inner_pic_3.jpg'
        video_target_url = r'http://v.youku.com/v_show/id_XNjgxNzM4MzU2.html'
        self.db.admin_add_news(news_type, title, abstract, author, module,
                         pub_status, is_delete, body, inner_pic_sub_url,
                         video_target_url, )

if __name__ == "__main__":
    uploadTestData = UploadTestData()
    uploadTestData.upload()
    
