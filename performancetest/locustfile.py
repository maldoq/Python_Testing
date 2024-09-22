from locust import HttpUser, TaskSet, task, between


class UserBehavior(TaskSet):

    @task(1)
    def show_summary(self):
        self.client.post(
            '/showSummary', data={'email': 'admin@irontemple.com'},
        )

    @task(2)
    def purchase_places(self):
        self.client.post(
            '/purchasePlaces', data={
                'competition': 'Spring Festival',
                'club': 'Iron Temple',
                'places': '1',
            },
        )


class WebsiteUser(HttpUser):
    tasks = [UserBehavior]
    wait_time = between(1, 5)  # Wait time between tasks (in seconds)
