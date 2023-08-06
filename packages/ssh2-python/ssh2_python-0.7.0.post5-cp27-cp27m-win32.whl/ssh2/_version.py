
import json

version_json = '''
{"date": "2018-01-03T11:13:45.562000", "full-revisionid": "b995bf98d29353ceaf6a7e08fa0f5dfe26d3eaad", "dirty": false, "version": "0.7.0.post5", "error": null}'''  # END VERSION_JSON


def get_versions():
    return json.loads(version_json)

