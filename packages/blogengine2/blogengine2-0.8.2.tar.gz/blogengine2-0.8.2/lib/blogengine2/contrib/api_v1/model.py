#!/usr/bin/env python
# -*- coding: utf-8 -*-
# Default model classes for use in BlogEngine
from notmm.dbapi.orm import model, ZODBFileStorageProxy
db = ZODBFileStorageProxy('127.0.0.1:4343')

class CategoryManager(model.ModelManager):
    model = 'Category'
    
class MessageManager(model.ModelManager):
    model = 'Message'
    
    def get_published_posts(self, params=[], order_by='pub_date'):
        """
        Fetch blog posts using custom selection filters
        
        params = [('reviewed', '==', True), ...]

        """
        lst = []
        for param, direction, value in params:
            q = self.db.Q.Match(self.db.Message, param, direction, value)
            lst.append(q)

        results = self.db.Q.Intersection(*lst)
        return [item for item in results()] #self.objects.find(**results())

class CommentManager(model.ModelManager):
    model = 'Comment'
    #db_connection = db

    #def__new__(cls, *args, **kwargs):
    #   cls.feedobj = cls.create_feed_obj(metaclass=RSSFeedGenerator)
    #
    #def create_feed_obj(self, metaclass):
    #   pass

#class MessageManager(object):
#    objects = RelationProxy(db.Message)

# Generic voting Manager objects
#class PollManager(object):
#    objects = RelationProxy(db.Poll)

