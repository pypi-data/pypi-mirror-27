
import json

version_json = '''
{"date": "2017-12-21T15:54:57.066000", "full-revisionid": "5f899c06cbc66956367ea45b5b9fda863b50c657", "dirty": false, "version": "0.7.0-1", "error": null}'''  # END VERSION_JSON


def get_versions():
    return json.loads(version_json)

