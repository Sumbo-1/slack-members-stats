import urllib
import urllib2
import json

token = '<your slack api key here>'
url = 'https://<your-slack-team-name-here>.slack.com/api/users.list'


# helper functions 
def is_active(member):
    deleted = member.get('deleted')
    return not deleted if deleted != None else False

def is_human(member):
    is_bot = member.get('is_bot')
    is_slackbot = member.get('id') == 'USLACKBOT'
    return not is_bot if is_bot !=  None and not is_slackbot else False

def is_online(member):
    is_online = member.get('presence')
    return is_online == 'active'
    
    
# get user data
def members():
    data = dict(token=token, presence=1)
    url_params = urllib.urlencode(data)
    get_url = url + '?' + url_params

    resp = urllib2.urlopen(get_url)
    resp_data = json.loads(resp.read())
    
    members = resp_data.get('members')

    real_members = [member for member in members if is_human(member) and is_active(member)]
    members_online = [member for member in real_members if is_online(member)]
    
    members_info = dict(members=len(real_members), online=len(members_online))

    return members_info


def lambda_handler(event, context):
    return members()
