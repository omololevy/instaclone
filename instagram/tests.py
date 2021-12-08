from django.test import TestCase
from .models import Comments,Image,Profile
from django.contrib.auth.models import User


class ProfileTestClass(TestCase):
    def setUp(self):
        self.user = User(username='Softdev')
        self.user.save()
        self.user_profile = Profile(user=self.user,profile_picture="mypic.png")
   
    def tearDown(self):
        User.objects.all().delete()
        Profile.objects.all().delete()
      
    def test_instance(self):
        self.assertTrue(isinstance(self.user_profile,Profile))
            
    def test_save_user_profile(self):
        self.user_profile.save_profile()
        profiles=Profile.objects.all()
        self.assertTrue(len(profiles)>0)
        
    def test_delete_user_profile(self):
        self.user_profile.save_profile()
        self.user_profile.delete_profile()
        profiles=Profile.objects.all()
        self.assertTrue(len(profiles)==0)

class ImageTestClass(TestCase):
    def setUp(self):
        self.user = User(username='Softdev')
        self.user.save()
        self.user_profile = Profile(user=self.user,profile_picture="mypic.png")
        self.post = Image(name="views",caption="Nyc views",user=self.user_profile)
        
    def tearDown(self):
        Image.objects.all().delete()
        Profile.objects.all().delete()
        User.objects.all().delete()
        
    def test_instance(self):
        self.assertTrue(isinstance(self.post,Image))
            
    def test_save_post(self):
        self.post.save_post()
        posts=Image.objects.all()
        self.assertTrue(len(posts)>0)
        
    def test_update_caption(self):
        self.post.save_post()
        self.post.update_post_caption(self.post.id,'test')
        updated= Image.objects.get(caption='test')
        self.assertEqual(updated.caption,'test') 
        
    def test_delete_post(self):
        self.post.save_post()
        self.post.delete_post()
        posts=Image.objects.all()
        self.assertTrue(len(posts)==0)                        

class CommentsTestClass(TestCase):
    def setUp(self):
        self.user = User(username='Softdev')
        self.user.save()
        self.user_profile = Profile(user=self.user,profile_picture="mypic.png")
        self.post = Image(name="views",caption="Nyc views",user=self.user_profile)
        self.post.save()
        self.comment = Comments(comment="Awsome",post=self.post,user=self.user)
        
    def tearDown(self):
        Image.objects.all().delete()
        User.objects.all().delete()
        Comments.objects.all().delete()
        Profile.objects.all().delete()
                    
    def test_instance(self):
        self.assertTrue(isinstance(self.comment,Comments))

    def test_delete_comment(self):
        self.comment.save_comment()
        self.comment.delete_comment()
        comments=Comments.objects.all()
        self.assertTrue(len(comments)==0) 

    def test_save_comment(self):
        self.comment.save_comment()
        comments=Comments.objects.all()
        self.assertTrue(len(comments)>0)
        