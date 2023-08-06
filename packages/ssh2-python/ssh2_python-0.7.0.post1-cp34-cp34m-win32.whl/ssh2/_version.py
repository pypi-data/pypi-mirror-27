
import json

version_json = '''
{"full-revisionid": "5f899c06cbc66956367ea45b5b9fda863b50c657", "version": "0.7.0-1", "dirty": false, "date": "2017-12-21T15:57:56.385456", "error": null}'''  # END VERSION_JSON


def get_versions():
    return json.loads(version_json)

