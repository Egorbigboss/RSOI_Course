from GatewayApp.requests_lib import Requests
import time
import requests


class ReqQueue:

    queue = []

    @staticmethod
    def add_patch_task_to_queue(url: str,data: dict):
        ReqQueue.queue.append({'url' : url , 'data' : data})

    @staticmethod
    def unqueue_tasks_from_queue():
        am_of_tasks = len(ReqQueue.queue)
        if(am_of_tasks != 0):
            for task in ReqQueue.queue:
                response = Requests.patch_request(url = task['url'], data = task['data'])
                if response.status_code == 200:
                    ReqQueue.queue.remove(task)
            print(am_of_tasks, " tasks were successfully unqueued")
