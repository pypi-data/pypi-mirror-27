
import json

version_json = '''
{"version": "0.7.0.post2", "error": null, "dirty": false, "date": "2017-12-21T17:31:00.504406", "full-revisionid": "5c1176d0fd4f4ab17725d68176feba0aec5eeee8"}'''  # END VERSION_JSON


def get_versions():
    return json.loads(version_json)

