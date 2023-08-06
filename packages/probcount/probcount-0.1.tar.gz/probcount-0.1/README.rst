=========================
 Probabilistic Counter
=========================

A simple and efficient probabilistic counter, suited for rate limiting and counting efficiently, without uploading every action to the remote database.

Usage
=============


Instructions
------------

.. code:: python

  from probcount import ProbCounter
  from functools import partial

  pc = ProbCounter()

  def old_increase_function(counter_name, value):
      # run the real call to the DB increasing the counter
      # for a redis
      # return redis.Redis().incrby(name=counter_name, amount=value)
      # or a MongoDB
      # return (pymongo.MongoClient().database_name.collection_name.find_one_and_update({"_id": counter_name},
                                                                                        {"$inc": {"value": value}},
                                                                                        {"value": 1}).get("value", 0) + value)
      pass

  def old_get_function(counter_name):
      # run the real call to the DB increasing the counter
      # for a redis
      # redis.Redis().get(name=counter_name)
      # or a MongoDB
      # pymongo.MongoClient().database_name.collection_name.find_one({"_id": counter_name}, {"value": 1}).value
      pass


  pc.create("name_of_counter", partial(old_increase_function, "name_of_counter"), partial(old_get_function, "name_of_counter"))
  pc.inc("name_of_counter", 42.0)
  pc.get("name_of_counter")


Supported Python Versions
=========================

Python Project Template supports the following versions out of the box:

* CPython 2.6, 2.7, 3.3, 3.4, 3.5, 3.6, 3.7
* PyPy 1.9

Authors
=======

* Tudor Aursulesei
