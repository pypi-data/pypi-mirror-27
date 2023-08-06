
import json

version_json = '''
{"date": "2017-12-21T14:18:49.289663", "dirty": false, "error": null, "full-revisionid": "275b67dc2938b3bb6ab0f353c461c5b838de9db8", "version": "0.7.0"}'''  # END VERSION_JSON


def get_versions():
    return json.loads(version_json)

