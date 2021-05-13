#!/usr/bin/env python
# -*- coding: utf-8 -*-

"""Teachers-Tracker.

A flask app with social network bots that informs about teachers
absence and substitute teachers.
"""

from flask import Flask

__author__ = "Ilya B. Anosov"
__credits__ = ["Maria A. Zamaryokhina", "Sofia P. Kalinina"]
__license__ = "GPL"
__version__ = "1.0.1"
__maintainer__ = "Ilya B. Anosov"
__email__ = "anosovilya465@yandex.ru"
__status__ = "Development"

app = Flask(__name__)
app.config['SECRET_KEY'] = 'yandexlyceum_secret_key'


def main():
    app.run()


if __name__ == '__main__':
    main()
