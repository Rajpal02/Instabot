import requests
import urllib

Access_Token = "1464437497.eae116d.b211e96a32954ee18bacb63fc6e6498b"
Base_URL = "https://api.instagram.com/v1/"
def user_info(user):
    request_url = "%susers/%s/?access_token=%s" %(Base_URL,user,Access_Token)
    print "Get request URL : %s" %(request_url)
    user_info = requests.get(request_url).json()

    if user_info["meta"]["code"] == 200:
        if len(user_info["data"]):
            print "Username : %s" %(user_info["data"]["username"])
            print "Name : %s" %(user_info["data"]["full_name"])
            print "Bio : %s" %(user_info["data"]["bio"])
            print "No. of posts Upload : %s" %(user_info["data"]["counts"]["media"])
            print "No. of followers : %s" %(user_info["data"]["counts"]["followed_by"])
            print "No. of people you follow : %s" %(user_info["data"]["counts"]["follows"])
        else:
            print "user does not exist"
    else:
        print "Some error occurred"

def get_user_id(name):
    request_url = "%susers/search?q=%s&access_token=%s" %(Base_URL,name,Access_Token)
    print "Get request URL of client : %s" %(request_url)
    client_info = requests.get(request_url).json()

    if client_info["meta"]["code"] == 200:
        if len(client_info["data"]):
            return client_info["data"][0]["id"]
        else:
            print "No data"
    else:
        print "Some error occurred"
    return None

def get_post_id(user):
    request_url = "%susers/%s/media/recent/?access_token=%s" %(Base_URL,user,Access_Token)
    print "Get request URL : %s" %(request_url)
    client_post = requests.get(request_url).json()

    if client_post["meta"]["code"] == 200:
        if len(client_post["data"]):
            for i in range(len(client_post["data"])):
                print str(i+1) + ") " + client_post["data"][i]["id"]

            take_id = raw_input("enter the id:")
            if len(take_id):
                take_id = int(take_id)
                return client_post["data"][take_id-1]["id"]
        else:
            print "post doesnot exist"
    else:
        print "Some error occurred"
    return  None

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

def get_image_url():
    request_url = "%susers/%s/media/recent/?access_token=%s" % (Base_URL, user, Access_Token)
    print "Get request URL : %s" % (request_url)
    client_image = requests.get(request_url).json()

    if client_image["meta"]["code"] == 200:
        if len(client_image["data"]):
            for i in range(len(client_image["data"])):
                print (i+1) + ") " + client_image["data"][i]["id"] + ".jpeg"

        image_name = raw_input("Select from images:")
        if len(image_name):
            image_name = int(image_name)
            return client_image["data"][image_name-1]["image"] + ["standard_resolution"]["url"]
        else:
            print "Enter valid input"

def like_a_post(media_id):
    request_url = "%smedia/%s/likes" %(Base_URL,media_id)
    print "Get request URL : %s" %(request_url)
    like_details = requests.post(request_url,{"access_token" : Access_Token}).json()

    if like_details["meta"]["code"] == 200:
        print "Your like was successful"
    else:
        print "Some error occurred"

def comment_a_post(media_id):
    request_url = "%smedia/%s/comments" %(Base_URL,media_id)
    print "Get request URL : %s" %(request_url)
    your_comment = raw_input("Write your comment")
    comment_details = requests.post(request_url,{"access_token" : Access_Token,"text" : your_comment}).json()

    if comment_details["meta"]["code"] == 200:
        if len(comment_details["data"]):
            print "Your comment was successful"
    else:
        print "Some error occurred"

def select_user(q):
    if q.upper() == 'Y':
        user = "self"
    else:
        username = raw_input("Enter instagram's username: ")
        user = get_user_id(username)
        if user == None:
            print "user does not exist"
            exit()
    return user

i = True
while(i):
    ques = raw_input("1) Know info\n2) Get Post\n3) Like Post\n4) comment post\n5) Exit\n ")
    if ques == '1':
        q1 = raw_input("Do you wana know own info(Y/N): ")
        user = select_user(q1)
        user_info(user)

    elif ques == '2':
        q2 = raw_input("own post?(Y/N):")
        user = select_user(q2)
        get_post_id(user)

    elif ques == '3':
        q3 = raw_input("like self post?(Y/N): ")
        user = select_user(q3)
        media_id=get_post_id(user)
        like_a_post(media_id)

    elif ques == '4':
        q4 = raw_input("comment self post?(Y/N): ")
        user = select_user(q4)
        media_id = get_post_id(user)
        comment_a_post(media_id)

    elif ques == '5':
        exit()

    else:
        print "Invalid option"