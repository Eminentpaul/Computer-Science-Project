from datetime import datetime
from .models import Forum, Notification
from user_auth.models import Profile

forum = Forum.objects.all()
users = Profile.objects.all()


# tatal = 0


def leader():
    leaderboard = {}
    leaders = []
    for post in forum:
        total = int(post.comment_count) + int(post.likes.all().count()) + int(post.views.all().count())
        if str(post.author.profile.id) in leaderboard:
            leaderboard[f'{post.author.profile.id}'] += total 
        else:
            leaderboard[f'{post.author.profile.id}'] = total 

    n = sorted(leaderboard.items(), key=lambda kv:kv[1], reverse=True)



    for v in n:
        for user in users:
            if str(user.id) == str(v[0]) and int(v[1]) > 0:
                leaders.append(
                    {
                        'user': user.user.full_name, 
                        'score': str(v[1]), 
                        'image': user.user.profile.avatar,
                        'profile': user.user.profile.id
                    }
                )
            

              
    return leaders
        

def checkDate():
    date = datetime.today().date().strftime('%Y-%m-%d')
    return date

   
class UserNotification:
    def __init__(self, user):
        self.user = user


    def myNotifiction(self):
        return Notification.objects.all().filter(user=self.user, isRead=False)

    
    def follow_notify(self, status, receiver):
        return Notification.objects.create(
            user=receiver,
            status=status,
            sender=self.user
        )
        # return notify

    def repost_notify(self, status, post, receiver):
        return Notification.objects.create(
            user=receiver,
            sender=self.user,
            post=post,
            status=status
        )
    

    def like_notify(self, status, post, receiver):
        return Notification.objects.create(
            user=receiver,
            sender=self.user,
            post=post,
            status=status
        )
    

    def comment_notify(self, status, post, receiver):
        return Notification.objects.create(
            user=receiver,
            sender=self.user,
            post=post,
            status=status
        )
    

    def post_notify(self, status, post):
        for follower in self.user.profile.followers.all():
            Notification.objects.create(
                user=follower,
                post=post, 
                status=status,
                sender=self.user
            )
        return True