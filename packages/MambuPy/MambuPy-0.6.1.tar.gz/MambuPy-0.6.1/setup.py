#!/usr/bin/python

import setuptools

setuptools.setup(name             = "MambuPy",
                 version          = "0.6.1",
                 description      = "A python lib for using Mambu APIs",
                 author           = "Javier Novoa C.",
                 author_email     = "jstitch@gmail.com",
                 license          = "GPLv3",
                 url              = "https://jstitch.github.io/MambuPy",
                 packages         = ['mambupy',],
                 keywords         = ["mambu",],
                 long_description = """\
                 MambuPy, A python API for using Mambu.

                 Allows accessing Mambu via its REST API. Also includes
                 SQLAlchemy mappings to a backup of its DataBase.

                 Mambu is a cloud platform which lets you rapidly build,
                 integrate, launch and service any lending portfolio into any
                 market (https://www.mambu.com).\
                 """ )
