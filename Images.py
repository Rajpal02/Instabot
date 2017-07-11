def get_image():
    request_url = "%susers/%s/media/recent/?access_token=%s" % (Base_URL, user, Access_Token)
    print "Get request URL : %s" % (request_url)
    client_image = requests.get(request_url).json()

    if client_image["meta"]["code"] == 200:
        if len(client_image["data"]):
            for i in range(len(client_image["data"])):
                image_name = client_image["data"][i]["id"] + ".jpeg"
                image_url = client_image["data"][i]["images"]["standard_resolution"]["url"]
                urllib.urlretrieve(image_url,image_name)