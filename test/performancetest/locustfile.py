from locust import HttpUser, TaskSet, task, between


class UserBehavior(TaskSet):

    @task(1)
    def show_summary(self):
        self.client.post(
            '/showSummary',
            data={'email': 'admin@irontemple.com'},
        )

    @task(2)
    def show_summary(self):
        self.client.post(
            '/showSummary',
            data={'email': 'john@simplylift.co'},
        )

    @task(3)
    def show_summary(self):
        self.client.post(
            '/showSummary',
            data={'email': 'kate@shelifts.co.uk'},
        )

    @task(4)
    def show_summary(self):
        self.client.post(
            '/showSummary',
            data={'email': 'dominique@gmail.com'},
        )

    @task(5)
    def purchase_places(self):
        self.client.post(
            '/purchasePlaces',
            data={
                'competition': 'Spring Festival',
                'club': 'Iron Temple',
                'places': '1',
            },
        )


class WebsiteUser(HttpUser):
    tasks = [UserBehavior]
    wait_time = between(1, 5)  # Wait time between tasks (in seconds)
