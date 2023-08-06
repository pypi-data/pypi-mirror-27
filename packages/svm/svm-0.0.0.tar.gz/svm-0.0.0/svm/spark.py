import requests

class Spark(object):

    _spark_versions = {}
    SPARK_REPO_URL = 'https://api.github.com/repos/apache/spark'

    @classmethod
    def spark_versions(cls):
        if not cls._spark_versions:
            cls._spark_versions = {v['name']: v['zipball_url'] for v in requests.get(Spark.SPARK_REPO_URL + '/tags').json()}
        return cls._spark_versions

    @staticmethod
    def print_version_list():
        for version in sorted(spark_versions):
            print("[ ] {}".format(version[1:]))