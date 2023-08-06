
import json

version_json = '''
{"date": "2017-12-27T11:48:29.596000", "full-revisionid": "fd56d48f55d5a34e88426fd5dcccde4838d8469c", "dirty": false, "version": "0.7.0.post3", "error": null}'''  # END VERSION_JSON


def get_versions():
    return json.loads(version_json)

