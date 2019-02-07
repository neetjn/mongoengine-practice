from blog.constants import BLOG_HOST, BLOG_PORT
from locust import TaskSet, task, HttpLocust


class BlogTasks(TaskSet):

    # def on_start(self):
    #     self.client.get('/')

    @task
    def service_description(self):
        self.client.get('/')


class WebsiteUser(HttpLocust):
    task_set = BlogTasks
    host = f'http://{BLOG_HOST}:{BLOG_PORT}'
    min_wait = 5000
    max_wait = 15000
