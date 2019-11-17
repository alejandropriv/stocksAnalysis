import requests


class RequestHandler:

    error = None


    def __init__(self):
        print("Request Handler created")


    def load_webpage(self, webpage):
        if webpage is not None:

            src = requests.get(webpage)

            status_code = src.status_code

            #headers = result.headers
            #print(headers)


            if status_code == 200:
                print("webpage: " +webpage+" loaded successfully")
                return src

            else:
                #set error and return
                return None
        else:
            #  Set error and return
            raise Exception("Errror Error")



