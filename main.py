import json, requests, sys

print """  __    __
 /' \  /' \\
/\_, \/\_, \\
\/_/\ \/_/\ \\
   \ \ \ \ \ \\
    \ \_\ \ \_\\
     \/_/  \/_/
"""

print "--- 11's discord deleter thing ---"
print "clears all of your messages in a channel"
if(len(sys.argv) > 1):
    if(sys.argv[1] == "config"):
        with open('config.json') as json_data:
            data = json.load(json_data)
        username = data["username"]
        auth_token = data["auth_token"]
        channel_id = data["channel_id"]
        delete_from_all_users = data["delete_from_all"]
else:
    print "in order for this script to work properly the channel id, auth token, and username is required"
    username = raw_input("username: ")
    auth_token = raw_input("auth token: ")
    channel_id = raw_input("channel id: ")
    delete_from_all_users = True if raw_input("delete messages from other users (y/n): ") == "y" else False

def get_all_messages(auth, id, last="", prev=[]): # recursively find all messages in a channel, 100 at a time
    if not last: # first method call, start from beginning (might be able to remove)
        messages = json.loads(requests.get("http://canary.discordapp.com/api/v6/channels/" + id + "/messages", headers={"authorization": auth}, params={"limit": 100}).content)
    else:
        messages = json.loads(requests.get("http://canary.discordapp.com/api/v6/channels/" + id + "/messages", headers={"authorization": auth}, params={"before" : last, "limit" : 100}).content)

    prev = prev + messages

    if len(messages) < 100:
        print "got to end of channel at " + str(len(prev)) + " messages"
        return prev
    else:
        oldest = sorted(messages, key=lambda x: x["timestamp"], reverse=True)[-1]
        return get_all_messages(auth, id, last=oldest["id"], prev=prev)

def delete_all(auth, id, user, messages):
    print "deleting all messages in " + id + " from username " + user
    for message in messages:
        if delete_from_all_users:
            requests.delete("http://canary.discordapp.com/api/v6/channels/" + id + "/messages/" + message["id"], headers={"authorization": auth})
        else:
            if (message["author"]["username"] == user):
                requests.delete("http://canary.discordapp.com/api/v6/channels/" + id + "/messages/" + message["id"],
                                headers={"authorization": auth})
    print "all messages deleted"

delete_all(auth_token, channel_id, username, get_all_messages(auth_token, channel_id))