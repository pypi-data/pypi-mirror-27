
import json

version_json = '''
{"date": "2017-12-21T13:53:30.020000", "full-revisionid": "275b67dc2938b3bb6ab0f353c461c5b838de9db8", "dirty": false, "version": "0.7.0", "error": null}'''  # END VERSION_JSON


def get_versions():
    return json.loads(version_json)

