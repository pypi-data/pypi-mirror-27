
import json

version_json = '''
{"date": "2017-12-21T17:23:51.668272", "full-revisionid": "5c1176d0fd4f4ab17725d68176feba0aec5eeee8", "error": null, "version": "0.7.0.post2", "dirty": false}'''  # END VERSION_JSON


def get_versions():
    return json.loads(version_json)

