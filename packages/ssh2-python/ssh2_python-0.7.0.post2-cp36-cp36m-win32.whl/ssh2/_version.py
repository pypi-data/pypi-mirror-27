
import json

version_json = '''
{"date": "2017-12-21T17:38:25.195554", "dirty": false, "error": null, "full-revisionid": "5c1176d0fd4f4ab17725d68176feba0aec5eeee8", "version": "0.7.0.post2"}'''  # END VERSION_JSON


def get_versions():
    return json.loads(version_json)

