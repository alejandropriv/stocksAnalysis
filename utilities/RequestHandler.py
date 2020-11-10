import requests
import time


class RequestHandler:

    def __init__(self, retries=5):
        print("Request Handler created")
        self.retries = retries

    def load_webpage(self, webpage):
        if webpage is not None:

            for retry in range(0, self.retries):
                time_to_sleep = retry * .5+1

                src = requests.get(webpage)

                status_code = src.status_code

                # headers = result.headers
                # print(headers)

                if status_code == 200:
                    print("webpage: {0} loaded successfully, Retry: {1}".format(webpage, retry))
                    return src

                else:
                    print("webpage: {0} not loaded with Status Code: {1} sleeping: {2}".format(webpage, status_code, time_to_sleep))
                    time.sleep(time_to_sleep)

            raise TimeoutError


        else:
            #  Set error and return
            raise Exception("Errror Error")
