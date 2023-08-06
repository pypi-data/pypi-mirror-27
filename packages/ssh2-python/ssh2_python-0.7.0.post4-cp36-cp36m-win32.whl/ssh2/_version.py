
import json

version_json = '''
{"date": "2017-12-27T13:51:49.764414", "dirty": false, "error": null, "full-revisionid": "bea17aacd7e0d16af3b8a0bcdd1a64cdf2d558dd", "version": "0.7.0.post4"}'''  # END VERSION_JSON


def get_versions():
    return json.loads(version_json)

