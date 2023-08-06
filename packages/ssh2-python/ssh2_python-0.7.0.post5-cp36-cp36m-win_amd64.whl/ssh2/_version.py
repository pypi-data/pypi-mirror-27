
import json

version_json = '''
{"date": "2018-01-03T11:43:41.043667", "dirty": false, "error": null, "full-revisionid": "b995bf98d29353ceaf6a7e08fa0f5dfe26d3eaad", "version": "0.7.0.post5"}'''  # END VERSION_JSON


def get_versions():
    return json.loads(version_json)

