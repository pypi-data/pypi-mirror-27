# -*- coding: utf-8 -*-
"""TODO: doc module"""


class ModelBase(object):
    """TODO: doc class"""

    def __init__(self):
        """TODO: doc method"""
        pass


class TProject(ModelBase):
    """TODO: doc class"""

    _res_members = None

    # Testlink object properties
    id = None
    name = None
    is_public = None

    def __init__(self, res_members):
        """TODO: doc method"""
        super(TProject, self).__init__()
        if res_members is None:
            raise Exception('Bad param, res_member can\'t be None')
        if len(res_members) <= 0:
            raise Exception(
                'Bad param, res_member can\'t be empty list')
        self._res_members = res_members
        self._load()
    
    def _load(self):
        for res_member in self._res_members:
            name = res_member.name
            value = res_member.value
            if name == 'id':
                self.id = value
            if name == 'name':
                self.name = value
            if name == 'is_public':
                self.is_public = value

    def __repr__(self):
        return "TProject: id={}, name={}, is_public={}".format(
            self.id,
            self.name,
            self.is_public
        )