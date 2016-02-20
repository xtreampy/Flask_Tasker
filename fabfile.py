from fabric.api import local, settings, abort
from fabric.contrib.console import confirm

def commit():
    message = raw_input("Enter a git commit message: ")
    local("git add . && git commit -am '{}'".format(message))

def push():
    local("git push origin master")

def prepare():
    commit()
    push()

def pull():
    local("git pull origin master")

def heroku():
    local("git push heroku master")

def deploy():
    pull()
    heroku()

def rollback():
    local("heroku rollback")
