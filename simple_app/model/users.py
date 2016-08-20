# encoding:utf-8
'''
This is a user class module for testing
By YT
2016
'''

class Users(object):
    # args

    def __init__(self):
        pass

    users = [{'id':1,'name':'YT'},{'id':2,'name':'Tony'},{'id':3,'name':'See'}]
    name = None
    def set_name(self,id):

        if id == 1:
            self.name = 'YT'
        elif id == 2:
            self.name = 'Tony'
        print "Name is:",self.name

def load_user(id):
    user = Users()
    Users.set_name(user,id)
    if user.name:
        return user
    else:
        return False



