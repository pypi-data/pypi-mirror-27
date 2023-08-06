
import json

version_json = '''
{"full-revisionid": "bea17aacd7e0d16af3b8a0bcdd1a64cdf2d558dd", "error": null, "dirty": false, "version": "0.7.0.post4", "date": "2017-12-27T13:35:25.192446"}'''  # END VERSION_JSON


def get_versions():
    return json.loads(version_json)

