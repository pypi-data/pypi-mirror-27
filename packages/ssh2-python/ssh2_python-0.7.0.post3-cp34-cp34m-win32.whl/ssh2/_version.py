
import json

version_json = '''
{"full-revisionid": "fd56d48f55d5a34e88426fd5dcccde4838d8469c", "date": "2017-12-27T11:51:28.189606", "version": "0.7.0.post3", "error": null, "dirty": false}'''  # END VERSION_JSON


def get_versions():
    return json.loads(version_json)

