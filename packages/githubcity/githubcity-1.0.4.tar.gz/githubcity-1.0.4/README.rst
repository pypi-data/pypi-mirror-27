GitHubCity
==========

|Build Status| |GitHub license|\ |Coverage Status| |Known
Vulnerabilities| |Dependency Status|

What is this?
-------------

This is a small library which gets all GitHub users given a city.
Original idea is `Top-GitHub-Users-Data`_ by
[@JJ](https://github.com/JJ), an adaptation of `top-github-users`_ from
[@paulmillr](https://github.com/paulmillr/).

What I can do with this?
------------------------

This is an amazing Python library to study the GitHub community in a
location. You can get all the GitHub users from a given location and
obtain some data. For instance, you can generate one ranking like `this
ranking with the users from Spain (and its provinces)`_.

What I need to run this?
------------------------

You will need to install Python 3. *Python 2 is not supported*.

In addition, you will need to get an ID and Secret for a GitHub
application, `after registering your own application here!`_.

Dependencies
~~~~~~~~~~~~

There is a ``requirements.txt`` file included in this repo. Install all
dependences with ``pip install -r requirements.txt``.

How to install
--------------

There are two options to install this library and its dependencies.

Install from the source code
~~~~~~~~~~~~~~~~~~~~~~~~~~~~

You need to clone (or download) this repository. Then, go to ``src``
folder and run:

.. code:: shell

    python setup.py install

Install from pip
~~~~~~~~~~~~~~~~

`This library is available to be installed using pip.`_

.. code:: shell

    pip install githubcity

Getting started
---------------

`You can see one example about how to use this library here`_.

Basic example
~~~~~~~~~~~~~

.. code:: python

    idGH = os.environ.get('GH_ID')
    secretGH = os.environ.get('GH_SECRET')
    configuration = {
       "excludedLocations": [],
       "excludedUsers": [],
       "intervals": [
           [
               "2008-01-01",
               "2015-12-30"
           ]
       ],
       "last_date": "2015-12-30",
       "locations": [
           "Ceuta"
           ],
       "name": "Ceuta"
           }
    ciudad = GitHubCity(idGH, secretGH, configuration)
    ciudad.calculateBestIntervals()
    ciudad.addFilter("repos", ">1")
    ciudad.addFilter("followers", ">1")
    ciudad.getCityUsers()

Excluding users
~~~~~~~~~~~~~~~

You can generate a JSON file like this (each element is an use

.. _Top-GitHub-Users-Data: https://github.com/JJ/top-github-users-data
.. _top-github-users: https://github.com/paulmillr/top-github-users
.. _this ranking with the users from Spain (and its provinces): https://github.com/iblancasa/GitHubRankingsSpain
.. _after registering your own application here!: https://github.com/settings/applications/new
.. _This library is available to be installed using pip.: https://pypi.python.org/pypi?:action=display&name=githubcity
.. _You can see one example about how to use this library here: https://github.com/iblancasa/GitHubSpanishRankingGenerator

.. |Build Status| image:: https://travis-ci.org/iblancasa/GitHubCity.svg?branch=master
   :target: https://travis-ci.org/iblancasa/GitHubCity
.. |GitHub license| image:: https://img.shields.io/github/license/iblancasa/GitHubCity.svg
   :target: https://github.com/iblancasa/GitHubCity
.. |Coverage Status| image:: https://coveralls.io/repos/iblancasa/GitHubCity/badge.svg?branch=master&service=github
   :target: https://coveralls.io/github/iblancasa/GitHubCity?branch=master
.. |Known Vulnerabilities| image:: https://snyk.io/test/github/iblancasa/githubcity/badge.svg
   :target: https://snyk.io/test/github/iblancasa/githubcity
.. |Dependency Status| image:: https://gemnasium.com/badges/github.com/iblancasa/GitHubCity.svg
   :target: https://gemnasium.com/github.com/iblancasa/GitHubCity