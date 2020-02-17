#!/usr/bin/env python3

import json
import os
from urllib import request


event_path = os.environ['GITHUB_EVENT_PATH']

with open(event_path, "r") as f:
    event_data = json.load(f)

if event_data['action'] != 'published':
    print("Invalid state to trigger this action")
    exit(1)

def get_asset_by_name(name):
    for asset in event_data['release']['assets']:
        if asset['name'] == name:
            return asset
    return None

release_info_asset = get_asset_by_name('release_information.json')

if release_info_asset == None:
    print("release_information.json couldn't be found on the published release")
    exit(1)

release_info_asset_data = request.urlopen(release_info_asset['browser_download_url']).read()
release_info_asset_parsed = json.loads(release_info_asset_data)

# Add URL to all artifacts
for artifact in release_info_asset_parsed['artifacts']:
    artifact_asset = get_asset_by_name(artifact['fileName'])
    if artifact_asset == None:
        print("%s couldn't be found on the published release" % artifact['fileName'])
        exit(1)
    artifact['url'] = artifact_asset['browser_download_url']


with open("latest.json", "w") as f:
    f.write(json.dumps(release_info_asset_parsed, sort_keys=True, indent=4))

with open(release_info_asset_parsed['version'] + ".json", "w") as f:
    f.write(json.dumps(release_info_asset_parsed, sort_keys=True, indent=4))
