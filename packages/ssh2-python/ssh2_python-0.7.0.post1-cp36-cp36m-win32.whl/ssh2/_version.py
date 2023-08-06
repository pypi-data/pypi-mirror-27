
import json

version_json = '''
{"date": "2017-12-21T16:18:30.258596", "dirty": false, "error": null, "full-revisionid": "5f899c06cbc66956367ea45b5b9fda863b50c657", "version": "0.7.0-1"}'''  # END VERSION_JSON


def get_versions():
    return json.loads(version_json)

