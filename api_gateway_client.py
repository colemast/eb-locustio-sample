import requests

HEADERS = {
'content-type': "application/x-www-form-urlencoded",
'authorization': "AWS4-HMAC-SHA256 Credential=AKIAIT5HVGQZTIJV5EXQ/20161122/eu-west-1/execute-api/aws4_request, SignedHeaders=content-length;content-type;host;x-amz-date, Signature=d4611db348fa15086c231972050e31e0cafa79944935cdb04ad42f1fd0ada905",
'cache-control': "no-cache"
}

class ApiGatewayClient():

    def __init__(self, url):
        # Connect to Kinesis
        self.url = url

    def send_event(self, data):
        response = requests.request("POST", self.url, headers=HEADERS, data=data)
        #async_response.send()
        return None