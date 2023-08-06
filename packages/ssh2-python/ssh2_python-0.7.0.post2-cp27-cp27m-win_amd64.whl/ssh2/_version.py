
import json

version_json = '''
{"date": "2017-12-21T17:13:55.698000", "full-revisionid": "5c1176d0fd4f4ab17725d68176feba0aec5eeee8", "dirty": false, "version": "0.7.0.post2", "error": null}'''  # END VERSION_JSON


def get_versions():
    return json.loads(version_json)

