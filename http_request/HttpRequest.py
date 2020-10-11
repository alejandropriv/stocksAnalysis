import requests


class HttpRequest:


    def __init__(self ):
        pass



    @staticmethod
    def execute(url,
                proxy=None,
                treat_info_as_error=True,
                headers=None):

        if headers is None:
            headers = {}


        response = requests.get(url, proxies=proxy, headers=headers)
        json_response = response.json()

        if not json_response:
            raise ValueError('Error getting data from the api, no return was given.')
        elif "Error Message" in json_response:
            raise ValueError(json_response["Error Message"])
        elif "Information" in json_response and treat_info_as_error:
            raise ValueError(json_response["Information"])
        elif "Note" in json_response and treat_info_as_error:
            raise ValueError(json_response["Note"])
        return json_response
        #else:
        #    csv_response = csv.reader(response.text.splitlines())
        #    if not csv_response:
        #        raise ValueError(
        #            'Error getting data from the api, no return was given.')
        #    return csv_response