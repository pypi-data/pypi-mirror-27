
.. |gitlogo| image:: _static/git_logo.png
             :height: 20

lightmlboard
============

.. image:: https://travis-ci.org/sdpython/lightmlboard.svg?branch=master
    :target: https://travis-ci.org/sdpython/lightmlboard
    :alt: Build status

.. image:: https://ci.appveyor.com/api/projects/status/6g0xro11tmc6t05d?svg=true
    :target: https://ci.appveyor.com/project/sdpython/lightmlboard
    :alt: Build Status Windows

.. image:: https://circleci.com/gh/sdpython/lightmlboard/tree/master.svg?style=svg
    :target: https://circleci.com/gh/sdpython/lightmlboard/tree/master

.. image:: https://badge.fury.io/py/lightmlboard.svg
    :target: http://badge.fury.io/py/lightmlboard

.. image:: https://img.shields.io/badge/license-MIT-blue.svg
    :alt: MIT License
    :target: http://opensource.org/licenses/MIT

.. image:: https://requires.io/github/sdpython/lightmlboard/requirements.svg?branch=master
     :target: https://requires.io/github/sdpython/lightmlboard/requirements/?branch=master
     :alt: Requirements Status

.. image:: https://codecov.io/github/sdpython/lightmlboard/coverage.svg?branch=master
    :target: https://codecov.io/github/sdpython/lightmlboard?branch=master

.. image:: http://img.shields.io/github/issues/sdpython/lightmlboard.png
    :alt: GitHub Issues
    :target: https://github.com/sdpython/lightmlboard/issues

.. image:: https://badge.waffle.io/sdpython/lightmlboard.png?label=ready&title=Ready
    :alt: Waffle
    :target: https://waffle.io/sdpython/lightmlboard

.. image:: nbcov.png
    :target: http://www.xavierdupre.fr/app/lightmlboard/helpsphinx/all_notebooks_coverage.html
    :alt: Notebook Coverage

*lightmlboard* implements a light machine learning leaderboard
based on :epkg:`tornado`.

.. toctree::
    :maxdepth: 1

    tutorial/index
    api/index
    i_index
    i_ex
    all_notebooks
    blog/blogindex
    index_modules

You can start the web application by running:

::

    import lightmlboard
    lightmlboard.LightMLBoard.start_app(config='server_options.py', port=8897)

**Links:** `github <https://github.com/sdpython/lightmlboard/>`_,
`documentation <http://www.xavierdupre.fr/app/lightmlboard/helpsphinx/index.html>`_,
:ref:`l-README`,
:ref:`blog <ap-main-0>`

+----------------------+---------------------+---------------------+--------------------+------------------------+------------------------------------------------+
| :ref:`l-modules`     |  :ref:`l-functions` | :ref:`l-classes`    | :ref:`l-methods`   | :ref:`l-staticmethods` | :ref:`l-properties`                            |
+----------------------+---------------------+---------------------+--------------------+------------------------+------------------------------------------------+
| :ref:`modindex`      |  :ref:`l-EX2`       | :ref:`search`       | :ref:`l-license`   | :ref:`l-changes`       | :ref:`l-README`                                |
+----------------------+---------------------+---------------------+--------------------+------------------------+------------------------------------------------+
| :ref:`genindex`      |  :ref:`l-FAQ2`      | :ref:`l-notebooks`  |                    | :ref:`l-statcode`      | `Unit Test Coverage <coverage/index.html>`_    |
+----------------------+---------------------+---------------------+--------------------+------------------------+------------------------------------------------+
