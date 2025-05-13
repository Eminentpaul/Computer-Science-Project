from datetime import datetime
from .models import Forum
from user_auth.models import Profile

forum = Forum.objects.all()
users = Profile.objects.all()


# tatal = 0


def leader():
    leaderboard = {}
    leaders = []
    for post in forum:
        total = post.comment_count + post.likes.all().count() + post.views.all().count()
        if str(post.author.profile.id) in leaderboard:
            leaderboard[f'{post.author.profile.id}'] += total 
        else:
            leaderboard[f'{post.author.profile.id}'] = total 

    n = sorted(leaderboard.items(), key=lambda kv:kv[1], reverse=True)
    # print(n)


    for user in users:
        for v in n:
            if str(user.id) == str(v[0]):
                leaders.append(
                    {'user': user.user.full_name, 'score': str(v[1]), 'image': user.user.profile.avatar}
                )

                
    return leaders
        

def checkDate():
    date = datetime.today().date().strftime('%Y-%m-%d')
    return date

   
