#!/usr/bin/env python
# Copyright (C) 2007-2012 Etienne Robillard <erob@gthcfoundation.org>
# All rights reserved.
# -*- coding: utf-8 -*-
# <LICENSE=ISC>
# Default model classes for use in BlogEngine
from notmm.dbapi.orm import ZODBFileStorageProxy
from notmm.dbapi.orm.model import Model

__all__ = ['Message', 'Comment',]

class Message(Model):
    class Meta:
        db_backend = ZODBFileStorageProxy
        db_addr = '127.0.0.1:4343'

#MessageManager = ModelManager(Message)

class Comment(Model):
    class Meta:
        db_backend = ZODBFileStorageProxy
        db_addr = '127.0.0.1:4343'

#CommentManager = ModelManager(Comment)


