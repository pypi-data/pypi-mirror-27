
import json

version_json = '''
{"version": "0.7.0.post5", "date": "2018-01-03T11:22:48.335661", "dirty": false, "full-revisionid": "b995bf98d29353ceaf6a7e08fa0f5dfe26d3eaad", "error": null}'''  # END VERSION_JSON


def get_versions():
    return json.loads(version_json)

