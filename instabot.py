import requests
import urllib
from textblob import TextBlob
from textblob.sentiments import NaiveBayesAnalyzer
import matplotlib.pyplot as plt
import numpy as np
from wordcloud import WordCloud, STOPWORDS
from os import path
from random import Random


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

def list_of_likes(media_id):
    request_url = "%smedia/%s/likes?access_token=%s" %(Base_URL,media_id,Access_Token)
    print "Get request URL : %s" %(request_url)
    list_of_likes = requests.get(request_url).json()

    if list_of_likes["meta"]["code"]==200:
        if len(list_of_likes["data"]):
            for i in range(len(list_of_likes["data"])):
                print str(i+1) + ") " + list_of_likes["data"][i]["username"]
        else:
            print "No comments"
    else:
        print "Some error occurred!"

def remove_a_like(media_id):
    request_url = "%smedia/%s/likes?access_token=%s" %(Base_URL,media_id,Access_Token)
    print "Get request URL : %s" %(request_url)
    like_details = requests.delete(request_url).json()

    if like_details["meta"]["code"] == 200:
        print "Your like was removed successful"
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

def list_of_comments(media_id):
    request_url = "%smedia/%s/comments?access_token=%s" %(Base_URL,media_id,Access_Token)
    print "Get request URL : %s" %(request_url)
    list = requests.get(request_url).json()

    if list["meta"]["code"]==200:
        if len(list["data"]):
            for i in range(len(list["data"])):
                print str(i+1) + ") " + list["data"][i]["text"]
        else:
            print "No comments"
    else:
        print "Some error occurred!"

def select_comment_id(media_id):
    list = requests.get(Base_URL+"media/"+media_id+"/comments?access_token="+Access_Token).json()
    if list["meta"]["code"]==200:
        if len(list["data"]):
            for i in range(len(list["data"])):
                print str(i+1) + ") " + list["data"][i]["text"]
            q=raw_input("select comment to delete: ")
            if len(q)>0 and q.isdigit():
                q=int(q)
                if q>0 and q<=len(list["data"]):
                    return list["data"][q-1]["id"]
                else:
                    print "Data out of range"
            else:
                print "Invalid input"
        else:
            print "No comments to access comment id"
    else:
        print "Some error occurred!"

def delete_a_comment(media_id):
    comment_id = select_comment_id(media_id)
    request_url="%smedia/%s/comments/%s?access_token=%s" %(Base_URL,media_id,comment_id,Access_Token)
    print "Get request URL : %s" %(request_url)
    list = requests.delete(request_url).json()
    if list["meta"]["code"]==200:
        print "comment deleted"
    else:
        print "Some error occurred"

def delete_negative_comments(media_id):
    request_url = "%smedia/%s/comments?access_token=%s" % (Base_URL, media_id, Access_Token)
    print "Get request URL : %s" % (request_url)
    list_of_comments = requests.get(request_url).json()

    if list_of_comments["meta"]["code"] == 200:
        if len(list_of_comments["data"]):
            pos=0
            neg=0
            for i in range(len(list_of_comments["data"])):
                blob = TextBlob(list_of_comments["data"][i]["text"],analyzer=NaiveBayesAnalyzer())
                if blob.sentiment.classification == "neg":
                    neg=+1
                    q=raw_input("Do you want to delete negative comment? (Y/N): ")
                    if q.upper() == 'Y':
                        url = "%smedia/%s/comments/%s?access_token=%s" %(Base_URL,media_id,list_of_comments["data"][i]["id"],Access_Token)
                        list = requests.delete(url).json()
                        if list["meta"]["code"] == 200:
                            print "comment deleted"
                        else:
                            print "Some error occurred"
                else:
                    pos=+1
            query = raw_input("Do you want to plot the data on pie chart? (Y/N): ")
            if query.upper()=='Y':
                labels = "Positive" , "Negative"
                sizes = [pos,neg]
                explode = (0,0.5)
                fig1, ax1 = plt.subplots()
                ax1.pie(sizes,explode=explode,labels=labels,autopct="%1.1f%%",shadow=True,startangle=90)
                ax1.axis("equal")
                plt.show()
        else:
            print "No comments"
    else:
        print "Some error occurred!"

def search_by_tag():
    tag = raw_input("Enter your tag by which you want to search: ")
    request_url ="%stags/%s/media/recent?access_token=%s" %(Base_URL,tag,Access_Token)
    print "Get Request URL : %s" %(request_url)
    list = requests.get(request_url).json()
    if list["meta"]["code"] == 200:
        if len(list["data"]):
            x={}
            for i in range(len(list["data"])):
                for j in range(len(list["data"][i]["tags"])):
                    url="%stags/%s?access_token=%s" %(Base_URL,list["data"][i]["tags"][j],Access_Token)
                    list1=requests.get(url).json()
                    if list1["meta"]["code"]==200:
                        if len(list1["data"]):
                            x[list1["data"]["name"]]=list1["data"]["media_count"]
                        else:
                            print "No data present"
                    else:
                        "Some error occurred"
            query = raw_input("Do you want to plot the data on worldcloud? (Y/N): ")
            if query.upper() == 'Y':
                wordcloud = WordCloud().generate_from_frequencies(x)
                plt.imshow(wordcloud,interpolation="bilinear")
                plt.axis("off")
                plt.show()
            else:
                exit()


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
    ques = raw_input("1) Know info\n"
                     "2) Get Post\n"
                     "3) Like operations\n"
                     "4) comment operations\n"
                     "5) Delete Negative Comments\n"
                     "6) Find Sub-trends by tags\n"
                     "7) Exit\n ")

    if len(ques)>0 and ques.isdigit():
        ques = int(ques)
        if ques == 1:
            q1 = raw_input("Do you wana know own info(Y/N): ")
            user = select_user(q1)
            user_info(user)

        elif ques == 2:
            q2 = raw_input("own post?(Y/N):")
            user = select_user(q2)
            get_post_id(user)

        elif ques == 3:
            q3 = raw_input("self post?(Y/N): ")
            user = select_user(q3)
            media_id=get_post_id(user)
            q = raw_input("1) like Post\n2) Get list of like\n3) remove a like")
            if len(q) > 0 and q.isdigit():
                q = int(q)
                if q == 1:
                    like_a_post(media_id)
                elif q == 2:
                    list_of_likes(media_id)
                elif q == 3:
                    remove_a_like(media_id)

        elif ques == 4:
            q4 = raw_input("self post?(Y/N): ")
            user = select_user(q4)
            media_id = get_post_id(user)
            q = raw_input("1) comment Post\n2) Get list of comment\n3) Delete comment")
            if len(q) > 0 and q.isdigit():
                q = int(q)
                if q == 1:
                    comment_a_post(media_id)
                elif q == 2:
                    list_of_comments(media_id)
                elif q==3:
                    delete_a_comment(media_id)

        elif ques == 5:
            q4 = raw_input("self post?(Y/N): ")
            user = select_user(q4)
            media_id = get_post_id(user)
            delete_negative_comments(media_id)

        elif ques == 6:
            search_by_tag()

        elif ques == 7:
            exit()

    else:
        print "Invalid option"