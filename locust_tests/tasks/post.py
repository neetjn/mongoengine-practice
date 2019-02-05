from locust import TaskSet, task, Locust


class PostTasks(TaskSet):

    def on_start(self):
        self.client.get('google.com')
        print('called how many times?')

    @task
    def index(self):
        print('index tested')

    @task
    def about(self):
        print('about tested')


class WebsiteUser(Locust):
    task_Set = PostTasks
    min_wait = 5000
    max_wait = 15000
