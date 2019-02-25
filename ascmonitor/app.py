""" For execution on Elastic Beanstalk """

from ascmonitor import app

application = app

if __name__ == '__main__':
    application.run()
