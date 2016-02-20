import unittest
import os
from project import app, db
from project.models import User,Task


class allTest(unittest.TestCase):
        ####################
        ### start-end f  ###
        ####################

    def setUp(self):
        app.config['TESTING'] = True
        app.config['CSRF_ENABLED'] = False
        #app.config['SECRET_KEY'] = 'my_precious'
        app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///test.db'
        self.app = app.test_client()
        db.create_all()

    def tearDown(self):
        db.session.remove()
        db.drop_all()

        ##########################
        #### helper function #####
        ##########################

    def login(self,name,password):
        return self.app.post('/',data=dict(name=name,password=password),follow_redirects=True)

    def logout(self):
        return self.app.post('/logout/',follow_redirects=True)

    def register(self,name,email,password,confirm):
        return self.app.post('/register/',data=dict(name=name,email=email,password=password,confirm=confirm),follow_redirects=True)

        ###################
        ###    tests  #####
        ###################

    def test_User_created_or_not(self):
        db.session.add(User('apoorv','appu@gmail.com','apoorvrajsaxena'))
        db.session.commit()
        test = db.session.query(User).all()
        for t in test:
            t.name
            assert t.name == 'apoorv'

"""    def test_user_login_form_exists(self):
        response = self.app.get('/', follow_redirects=True)
        self.assertEquals(response.status, 200)
        self.assertIn(b"Please login to access your tasklist", response.data)
"""
    def test_user_can_register(self):
        response = self.register('admin1','yo@gmail.com','admin123','admin123')
        self.assertIn('Thanks for registering',response.data)

    def test_user_can_login(self):
        response = self.login('admin1','admin123')
        self.assertIn('Welcome',response.data)

if __name__=='__main__':
    unittest.main()
