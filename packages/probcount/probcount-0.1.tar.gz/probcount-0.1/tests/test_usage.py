from probcount import ProbCounter, MockCounter
from functools import partial
import math
import time


def stddev(arr, desired):
    s = 0.0
    for item in arr:
        s += (item - desired) ** 2

    return math.sqrt(s / len(arr))


def run_one_trial(n):
    pc = ProbCounter()
    m = MockCounter()
    pc.create('key', partial(m.inc), partial(m.get))
    for i in range(n):
        pc.inc('key', 1)

    return pc.get('key')


def runtrial(n, seconds, trials):
    results = []
    t0 = time.time()
    runs = 0

    while time.time() - t0 <= seconds and runs < trials:
        runs += 1
        results.append(run_one_trial(n))

    error_rate = 100.0 * stddev(results) / float(n)
    return error_rate


def avg(arr):
    return sum(arr)/float(len(arr))


class TestUsage(object):
    def test_one_run(self, n=1024):
        result = run_one_trial(n)
#        assert stddev([result], n) <= 0.03 * n
        return result

    def test_many_runs(self, n=1024, n_trials=10):
        results = [self.test_one_run(n) for _ in range(n_trials)]
#        assert stddev(results, n) <= 0.03 * n
        return results

    def test_multiple_sizes(self):
        for n in range (0, 15):
            results = self.test_many_runs(2 ** n, 2 ** (16-n))
            error_rate = (100.0 * stddev(results, 2**n)) / (2 ** n)
            assert error_rate < 1.8
        #    print("for n=%9d, and %9d trials average result was %9.1f and error rate %5.3f%%" % (2 ** n,
        # 2 ** (16-n),
        # avg(results),
        # (100.0 * stddev(results, 2**n)) / (2 ** n)))

    def test_reduced_usage(self, n=131072, saved=0.20):

        """For 131072 ops we should use more than 17% of operations"""
        pc = ProbCounter()
        m = MockCounter()
        pc.create('key', partial(m.inc), partial(m.get))
        for i in range(n):
            pc.inc('key', 1)

        a_n = pc.get('key')

        assert pc.inc_ops / float(n) <= saved

    def test_many_reduced_usage(self):
        self.test_reduced_usage(262144, 0.16)
        self.test_reduced_usage(524288, 0.08)
        self.test_reduced_usage(1048576, 0.04)
        self.test_reduced_usage(4194304, 0.02)

    def test_redis_speed(self, n=131072):
        """Assert at least a 5 times reduction in time took to count to 131072"""

        import redis
        r = redis.StrictRedis()
        pc = ProbCounter()

        pc.create('redis_key_test', partial(r.incrbyfloat, 'redis_key_test'), partial(r.get, 'redis_key_test'))

        t0 = time.time()
        for i in range(n):
            r.incrbyfloat('redis_key_test_slow', 1.0)
        t1 = time.time()

        slow = t1-t0

        t0 = time.time()
        for i in range(n):
            pc.inc('redis_key_test', 1)

        t1 = time.time()

        fast = t1-t0
        assert fast * 5.0 <= slow

        r.delete("redis_key_test")

    def test_mongo_speed(self, n=32768):
        """Assert at least a 2 times reduction in time took to count to 32768"""

        import pymongo
        col = pymongo.MongoClient().some_database.some_collection
        col.update_one({"_id": "counter_fast"}, {"$set": { "value": 0.0}}, upsert=True)
        col.update_one({"_id": "counter_slow"}, {"$set": { "value": 0.0}}, upsert=True)

        pc = ProbCounter()

        def increase_function(val):
            col.update_one({"_id": "counter_fast"}, {"$inc": {"value": val}})

        def get_function():
            return col.find_one({"_id": "counter_fast"}, {"value": 1, "_id": 0})["value"]

        pc.create('mongo_key_test', increase_function, get_function)

        t0 = time.time()
        for i in range(n):
            col.update_one({"_id": "counter_slow"}, {"$inc": {"value": 1.0}})
        t1 = time.time()

        slow = t1-t0

        t0 = time.time()
        for i in range(n):
            pc.inc('mongo_key_test', 1)

        t1 = time.time()

        fast = t1-t0
        assert fast * 2.0 <= slow
        col.remove({"_id": "counter_fast"})
        col.remove({"_id": "counter_slow"})
