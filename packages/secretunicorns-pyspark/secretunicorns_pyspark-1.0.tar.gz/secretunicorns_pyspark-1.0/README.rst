============================
Secretunicorns PySpark SDK
============================

The secretunicorns PySpark SDK provides a pyspark interface to secretunicorns.

Quick Start
------------

First, install the library:

.. code-block:: sh

    $ pip install secretunicorns_pyspark

Then, to load the secretunicorns jars programatically:

.. code-block:: python

    from pyspark import SparkContext, SparkConf
    import secretunicorns_pyspark

    conf = (SparkConf()
            .set("spark.driver.extraClassPath", ":".join(secretunicorns_pyspark.classpath_jars())))
    SparkContext(conf=conf)


Alternatively pass the jars to your pyspark job via the -jars flag:

.. code-block:: sh

    $ pyspark -jars `secretunicornspyspark-jars` ...

Running Tests
-------------

Our recommended way of running the tests is using pyenv + pyenv-virtualenv. This allows you to
test on different python versions, and to test the installed distribution instead of your local
files.

Install `pyenv <https://github.com/pyenv/pyenv>`__, `pyenv-virtualenv <https://github
.com/pyenv/pyenv-virtualenv>`__ and `pyenv-virtualenvwrapper <https://github
.com/pyenv/pyenv-virtualenvwrapper>`__

You can do this in OSX using `brew <https://brew.sh/>`__

.. code-block:: sh

    $ brew install pyenv pyenv-virtualenv pyenv-virtualenvwrapper

For linux you can just follow the steps in each of the package's Readme. Or if your distribution
has them as packages that is a good alternative.

make sure to add the pyenv and virtualenv init functions to your corresponding
shell init (**.bashrc**, **.zshrc**, etc):

.. code-block:: sh
    
    eval "$(pyenv init -)"
    eval "$(pyenv virtualenv-init -)"

Start a new shell once you do that to pick up your changes.

Setup the python version we need. At the moment we are testing with python
2.7, 3.5 and 3.6 so we need to install these versions:

.. code-block:: sh

    $ pyenv install 2.7.10
    $ pyenv install 3.5.2
    $ pyenv install 3.6.2

Set them as global versions

.. code-block:: sh
    $ pyenv global 2.7.10 3.5.2 3.6.2

Verify they show up when you do:

.. code-block:: sh
    $ pyenv versions

Restart your shell and run the command again to verify that it persists across shell sessions.

Now we just need to install tox to run our tests:

.. code-block:: sh
    $ pip install tox

Run the tests by running:

.. code-block:: sh
    $ tox
