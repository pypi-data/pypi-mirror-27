
import json

version_json = '''
{"error": null, "dirty": false, "version": "0.7.0-1", "full-revisionid": "5f899c06cbc66956367ea45b5b9fda863b50c657", "date": "2017-12-21T16:04:06.832891"}'''  # END VERSION_JSON


def get_versions():
    return json.loads(version_json)

