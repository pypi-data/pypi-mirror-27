
import json

version_json = '''
{"version": "0.7.0", "full-revisionid": "275b67dc2938b3bb6ab0f353c461c5b838de9db8", "dirty": false, "date": "2017-12-21T14:02:55.525523", "error": null}'''  # END VERSION_JSON


def get_versions():
    return json.loads(version_json)

