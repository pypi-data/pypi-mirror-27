
import json

version_json = '''
{"version": "0.7.0.post3", "dirty": false, "date": "2017-12-27T11:57:37.945491", "full-revisionid": "fd56d48f55d5a34e88426fd5dcccde4838d8469c", "error": null}'''  # END VERSION_JSON


def get_versions():
    return json.loads(version_json)

