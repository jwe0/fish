import json, base64

def minecraft(url, session):
    results = {}

    response = session.get(url)
    if not response.status_code == 200:
        return {"message" : "Error in API request {}".format(response.status_code)}
    info = response.json()

    name = info.get("name")
    id   = info.get("id")

    results["name"] = name
    results["uuid"] = id

    skin_api = "https://sessionserver.mojang.com/session/minecraft/profile/{}".format(id)

    response = session.get(skin_api)
    print(response.status_code)
    if response.status_code != 200:
        return results

    info = response.json()

    properties = info.get("properties")[0].get("value")

    extra_data = json.loads(base64.b64decode(properties).decode())

    keys = ["timestamp", "profileId", "profileName"]

    for key in keys:
        results[key] = extra_data[key]

    textures = extra_data.get("textures")

    skin = textures.get("SKIN").get("url")

    results["skin"] = skin


    return results