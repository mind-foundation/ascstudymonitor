""" For execution on Elastic Beanstalk """

from ascmonitor import app

# alias for AWS
application = app

if __name__ == '__main__':
    application.run()
