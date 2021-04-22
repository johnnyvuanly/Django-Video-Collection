from django.test import TestCase
from django.urls import reverse # this will convert the name of the URL into the actual path
from .models import Video
from django.db import IntegrityError
from django.core.exceptions import ValidationError

class TestHomePageMessage(TestCase):

    def test_app_title_message_shown_on_home_page(self):
        # first make request to the home page
        url = reverse('home') # name of url is home
        response = self.client.get(url) # get the page at this given URL
        self.assertContains(response, 'Coding Videos')

class TestAddVideos(TestCase):
    
    def test_add_video(self):
        # dictionary with example valid data
        valid_video = {
            'name': 'Web Development',
            'url': 'https://www.youtube.com/watch?v=VfGW0Qiy2I0',
            'notes': 'Great beginners guide to web developers'
        }

        url = reverse('add_video') # 'add_video' is from path in urls.py
        # follow=True, included so that if you are redirected as a part of this request, then follow that request. 
        # AssertionError: 302 != 200 : Couldn't retrieve content: Response code was 302 (expected 200)
        response = self.client.post(url, data=valid_video, follow=True) 

        self.assertTemplateUsed('video_collection/video_list.html')
        
        # Does the video list show the new video?
        self.assertContains(response, 'Web Development')
        self.assertContains(response, 'Great beginners guide to web developers')
        self.assertContains(response, 'https://www.youtube.com/watch?v=VfGW0Qiy2I0')

        # Check to see if there is one video in the database and if it has the correct data
        video_count = Video.objects.count()
        self.assertEqual(1, video_count)

        # Check if the attributes of this video is are the same as the attributes of the data above
        video1 = Video.objects.first()
        # Data base fields we are checking
        self.assertEqual('Web Development', video1.name)
        self.assertEqual('https://www.youtube.com/watch?v=VfGW0Qiy2I0', video1.url)
        self.assertEqual('Great beginners guide to web developers', video1.notes)
        self.assertEqual('VfGW0Qiy2I0', video1.video_id)

    def test_add_video_invalid_url_not_added(self):
        # Check to see if adding a URL that is not valid or not a URL
        invalid_video_urls = [
            'https://www.youtube.com/watch',
            'https://www.youtube.com/watch?',
            'https://www.youtube.com/watcha=1234',
            'https://www.youtube.com/watch?v=',
            'https://github.com',
            'https://minneapolis.edu',
            'https://minneapolis.edu?v=VfGW0Qiy2I0'
        ]

        for invalid_video_url in invalid_video_urls:

            new_video = {
                'name': 'example',
                'url': invalid_video_url,
                'notes': 'example notes'
            }

            url = reverse('add_video')
            response = self.client.post(url, new_video) # Post message to url given and then new_video

            self.assertTemplateUsed('video_collection/add.html')

            messages = response.context['messages'] # Same message variable that is used in the view
            # List comprehension
            message_texts = [ message.message for message in messages] # For every message in messages list, extract that message

            self.assertIn('Invalid YouTube URL', message_texts)
            self.assertIn('Please check the data entered', message_texts)

            video_count = Video.objects.count()
            self.assertEqual(0, video_count)


class TestVideoList(TestCase):
    
    def test_all_videos_displayed_in_correct_order(self):
        v1 = Video.objects.create(name='XYZ', notes='example', url='https://www.youtube.com/watch?v=123')
        v2 = Video.objects.create(name='abc', notes='example', url='https://www.youtube.com/watch?v=124')
        v3 = Video.objects.create(name='AAA', notes='example', url='https://www.youtube.com/watch?v=125')
        v4 = Video.objects.create(name='lmn', notes='example', url='https://www.youtube.com/watch?v=126')

        expected_video_order = [ v3, v2, v4, v1 ]

        url = reverse('video_list')
        response = self.client.get(url)

        # context is all the data that's combined with the template to display the page. So our video list, dictionary at the bottom of views.py
        videos_in_template = list(response.context['videos'])

        self.assertEqual(videos_in_template, expected_video_order)

    def test_no_video_messsage(self):
        url = reverse('video_list')
        response = self.client.get(url)
        self.assertContains(response, 'No videos')
        self.assertEqual(0, len(response.context['videos']))

    def test_video_number_message_one_video(self):
        v1 = Video.objects.create(name='XYZ', notes='example', url='https://www.youtube.com/watch?v=123')
        url = reverse('video_list')
        response = self.client.get(url)

        self.assertContains(response, '1 video')
        self.assertNotContains(response, '1 videos')

    def test_video_number_message_two_videos(self):
        v1 = Video.objects.create(name='XYZ', notes='example', url='https://www.youtube.com/watch?v=123')
        v2 = Video.objects.create(name='abc', notes='example', url='https://www.youtube.com/watch?v=124')
        
        url = reverse('video_list')
        response = self.client.get(url)

        self.assertContains(response, '2 videos')

class TestVideoSearch(TestCase):
    """ Check out Clara's GitHub for example test """
    pass

class TestVideoModel(TestCase):

    def test_invalid_url_raises_validation_error(self):
        invalid_video_urls = [
            'https://www.youtube.com/watch',
            'https://www.youtube.com/watch/somethingelse',
            'https://www.youtube.com/watch/somethingelse?v=1234567',
            'https://www.youtube.com/watch?',
            'https://www.youtube.com/watcha=1234',
            'https://www.youtube.com/watch?v=',
            'https://github.com',
            'https://minneapolis.edu',
            'https://minneapolis.edu?v=VfGW0Qiy2I0',
            'asdfghjkl',
            '123465789',
            'http://www.youtube.com/watch/somethingelse?v=1234567',

        ]

        for invalid_video_url in invalid_video_urls:
            with self.assertRaises(ValidationError):
                Video.objects.create(name='example', url=invalid_video_url, notes='Example note')

        # Check that nothing is added in the database
        self.assertEqual(0, Video.objects.count())

    
    def test_duplicate_video_raises_integrity_error(self):
        v1 = Video.objects.create(name='XYZ', notes='example', url='https://www.youtube.com/watch?v=123')
        with self.assertRaises(IntegrityError):
            v1 = Video.objects.create(name='XYZ', notes='example', url='https://www.youtube.com/watch?v=123')
