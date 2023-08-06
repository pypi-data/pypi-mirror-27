
import json

version_json = '''
{"version": "0.7.0.post4", "full-revisionid": "bea17aacd7e0d16af3b8a0bcdd1a64cdf2d558dd", "date": "2017-12-27T13:31:44.855342", "error": null, "dirty": false}'''  # END VERSION_JSON


def get_versions():
    return json.loads(version_json)

