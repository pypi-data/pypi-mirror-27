
import json

version_json = '''
{"version": "0.7.0.post3", "error": null, "full-revisionid": "fd56d48f55d5a34e88426fd5dcccde4838d8469c", "date": "2017-12-27T10:57:37.612661", "dirty": false}'''  # END VERSION_JSON


def get_versions():
    return json.loads(version_json)

