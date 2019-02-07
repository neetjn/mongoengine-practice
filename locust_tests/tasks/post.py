from locust import TaskSet, task, HttpLocust


class PostTasks(TaskSet):

    def on_start(self):
        self.client.get('google.com')
        print('called how many times?')

    @task
    def index(self):
        self.client.get('google.com')
        print('index tested')

    @task
    def about(self):
        self.client.get('google.com')
        print('about tested')


class WebsiteUser(HttpLocust):
    task_set = PostTasks
    min_wait = 5000
    max_wait = 15000
