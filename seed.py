import requests, json, random, string
from models import Users, Comment, Post, Subpage, db
from faker import Faker
from bs4 import BeautifulSoup
import re

comments_list = []
headers = {
    'User-Agent': 'Mozilla/5.2 (Windows NT 6.1) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/41.0.2228.0 Safari/537.36'
}

def get_random_string(length):
    letters = string.ascii_lowercase
    result_str = ''.join(random.choice(letters) for i in range(length))
    return result_str

used_data = []
def createUsers():
    ranks = ['Staff', 'Senior Mod', 'Mod', 'Distinguished User', 'Experienced User', 'User', 'New User']
    for i in range(0,200):
        faker = Faker()
        
        user_name = faker.user_name()
        user_email = faker.email()
        user_phone = faker.phone_number()
        if user_name not in used_data and user_email not in used_data and user_phone not in used_data:
            used_data.extend([user_name, user_email, user_phone])
            user_data = {
                'name' : user_name,
                'email': user_email,
                'avatar_url': 'https://avatars.dicebear.com/api/open-peeps/{0}.svg'.format(get_random_string(8)),
                'password': '',
                'phone': user_phone,
                'rank': random.choices(ranks, weights=(0.5, 2.0, 7.5, 15, 20, 40, 30), k=1)[0],
                'created_at': None
            }
            user = Users(**user_data)
            print(user)
            try:
                db.session.add(user)
                db.session.commit()
            except:
                print('failed')
    


def populateRedditDB(sub_list, postQtdy):
    for subreddit in sub_list:
        url = f"https://www.reddit.com/r/{subreddit}.json?limit={postQtdy}"
        url_res = requests.get(url, headers=headers)
        reddit_json = json.loads(url_res.text)
        reddit_posts_url = ['http://reddit.com{0}.json'.format(post['data']['permalink'][:-1]) for post in reddit_json['data']['children']]
        result = requests.get(f"https://www.reddit.com/r/{subreddit}/", headers=headers)
        # print(result)
        body = BeautifulSoup(result.text, "html.parser")
        subpage_about = body.find(class_="_1zPvgKHteTOub9dKkvrOl4")
        subpage = createSubpage(subreddit, subpage_about.get_text())

        for post_url in reddit_posts_url[3:]:
            print(post_url)
            post_res = requests.get(post_url, headers=headers)
            post_data = json.loads(post_res.text)
            if post_data[0]['data']['children'][0]['data']['num_comments']:
                
                    post_data_media = extractMedia(post_data[0]['data']['children'][0]['data'])
                    if not post_data_media.get('url') and post_data_media.get('type') != 'text':
                        print('broke url')
                        continue
                    
                    print(post_data_media)
                    post_obj = {
                        'title': post_data[0]['data']['children'][0]['data']['title'],
                        'body': post_data[0]['data']['children'][0]['data']['selftext'],
                        'body_styled': post_data[0]['data']['children'][0]['data']['selftext_html'],
                        'users': getRandomUser(),
                        'votes': post_data[0]['data']['children'][0]['data']['score'],
                        'ref_id': post_data[0]['data']['children'][0]['data']['name'].split('_')[1],
                        'subpage': subpage,
                        'media_type': post_data_media['type'],
                        'media_link': post_data_media['url'],
                    }
                    post_final = Post(**post_obj)
                    print(post_obj['title'])
                    extractComments(post_data[1]['data']['children'], post_obj['ref_id'], post_final)

                
                    db.session.add(post_final)
                    db.session.commit()

def extractComments(comment_arr, parent_id, post):
    for comment in comment_arr:
        comment_data = comment['data']
        recursiveCommentExtractor(comment_data, parent_id, post)  


    
def recursiveCommentExtractor(comment_data, parent_id, post):
    if 'body' in comment_data:
        rand = random.randrange(0, 200) 
        ref_id_clean = comment_data['name'].split('_')[1]

        comment_dict = {
            'body' : comment_data['body'],
            'body_styled': comment_data['body_html'],
            'parent_comment_id': comment_data['parent_id'],
            'ref_id': ref_id_clean,
            'post': post,
            'users': Users.query.all()[rand],
            'parent_comment_id': parent_id,
            'votes': comment_data['score'],
        }
        comment_sql_obj = Comment(**comment_dict)
        db.session.add(comment_sql_obj)
        db.session.commit()
        print(comment_dict['ref_id'], parent_id)
        if comment_data['replies'] != '':
            if len(comment_data['replies']['data']['children']) >= 1:
                for data in comment_data['replies']['data']['children']:
                    recursiveCommentExtractor(data['data'], comment_data['name'].split('_')[1], post)
        else:
            return 'end'
        
def createSubpage(subreddit, description):
    checkSub = Subpage.query.filter_by(title=subreddit).all()
    if not len(checkSub):
        subpage = Subpage(title=subreddit, description=description)
        db.session.add(subpage)
        db.session.commit()
        return subpage
    else:
        return checkSub[0]
    
def extractMedia(data):
    media_data ={}
    media_data['url'] = None
    media_data['type'] = 'text'
    if data.get('media'):
        print('media' in data)
        media_data['type'] = 'video'
        print(data['media'].get('reddit_video'))
        if data['media'].get('reddit_video'):
            
            media_data['url'] = data['media']['reddit_video']['fallback_url']
        else:
            video_url = data['media']['oembed']['html']
            media_data['url'] = data['media']['oembed']['html'].split('src')[1].split(' ')[0][2:len(video_url)-1]
            media_data['type'] = 'yt_url'
    elif data.get('url_overridden_by_dest'):
        # console.log('has url')
        media_data['url'] = data['url_overridden_by_dest']
        regex = re.compile('(?i).(jpg|png|gif)$')
        if regex.search(str(media_data['url'])):
            media_data['type'] = 'image'
            if isURLWorking(media_data['url']):
                return media_data
            else:
                return {}
        elif media_data.get('selftext'):
            media_data['type'] = 'text_with_links'
        else:
            media_data['type'] = 'link'
    
    
       
    return media_data

def postDataTest():
    post_res = requests.get('https://www.reddit.com/r/webdev/comments/tvvsuz/how_do_fullstack_devs_here_feel_about_people_with.json', headers=headers)
    print(post_res)
    post_data = json.loads(post_res.text)
    post_data_media = extractMedia(post_data[0]['data']['children'][0]['data'])
    print(post_data_media)
    post_obj = {
        'title': post_data[0]['data']['children'][0]['data']['title'],
        'body': post_data[0]['data']['children'][0]['data']['selftext'],
        'body_styled': post_data[0]['data']['children'][0]['data']['selftext_html'],
        'users': getRandomUser(),
        'votes': post_data[0]['data']['children'][0]['data']['score'],
        'ref_id': post_data[0]['data']['children'][0]['data']['id'],
        'media_type': post_data_media['type'],
        'media_link': post_data_media['url'],
    }
    post_final = Post(**post_obj)
    print(post_final)
        
    
def getRandomUser():
    rand = random.randrange(0, 120) 
    return Users.query.all()[rand]

def getRandomSubPage():
    rand = random.randrange(0, 7) 
    return Subpage.query.all()[rand]
    

def UserFollowingSubpage():
    for i in range(200):
        user = getRandomUser()
        subpage = getRandomSubPage()
        print(user, subpage)
        user.following.append(subpage)
        db.session.commit()

def isURLWorking(url):
    r = requests.get(url)
    return r.status_code

    
createUsers()
populateRedditDB(['woahdude','blackcats','awww', 'london', 'gaming','LifeProTips', 'mildlyinteresting'], 15)
UserFollowingSubpage()