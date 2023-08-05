#!/usr/bin/env python
# -*- coding: utf-8 -*-

"""
.. codeauthor:: Cédric Dumay <cedric.dumay@gmail.com>


"""
from kser.entry import Entrypoint


class Task(Entrypoint):
    """"""

    @classmethod
    def init_by_id(cls, _id):
        """Load task by its ID"""

    def __init__(self, uuid=None, params=None, status="PENDING", result=None,
                 **kwargs):
        Entrypoint.__init__(self, uuid=uuid, params=params, result=result)
        self.status = status
        self.metadata = kwargs

    def get_attr(self, item):
        attr = "{}Id".format(item)
        return attr, getattr(getattr(self, item, self), attr, None)

    def __repr__(self):
        return "Task [{}](uuid={},status={}, params={})".format(
            self.__class__.path, self.uuid, self.status, self.params
        )
