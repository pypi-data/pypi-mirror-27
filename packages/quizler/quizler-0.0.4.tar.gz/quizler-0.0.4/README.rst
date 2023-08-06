|Requirements Status| |Build Status|

quizler
=======

Collection of utils for Quizlet flash cards

Requirements
------------

Tested on:

-  macOS / Python 3.6.1
-  Ubuntu 14.04 / Python 3.5.3

To install Python requirements (virtualenv is recommended):

.. code:: bash

    pip install -r requirements.txt

Usage
-----

Quizler relies onto environment variables to operate. Currently there're
two:

-  ``USER_ID`` - your username on quizlet, it can be viewed right at
   your avatar in the top right on quizlet.com
-  ``CLIENT_ID`` - Quizlet Client ID can be obtained in `Quizlet API
   dashboard <https://quizlet.com/api-dashboard>`__

Set this two before using the script. To work with quizler just invoke
CLI, e.g.:

.. code:: bash

    python main.py common

.. |Requirements Status| image:: https://requires.io/github/lancelote/quizler/requirements.svg?branch=master
   :target: https://requires.io/github/lancelote/quizler/requirements/?branch=master
.. |Build Status| image:: https://travis-ci.org/lancelote/quizler.svg?branch=master
   :target: https://travis-ci.org/lancelote/quizler
