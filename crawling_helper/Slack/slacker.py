import sys
import json
import requests
from datetime import datetime

class Slacker:
    def __init__(self, server_div, title, status, input_text):
        self.server_div = server_div
        self.title = title
        self.status = status
        self.input_text = input_text

    def make_attachment(self):
        """
        function info make_attachment : slack 배치 입력 내용 포멧 변환
        """
        color = '#68FF33' if self.status == 'Success' else '#FF3349'
        status_text = 'SUCCESS' if self.status == 'Success' else 'FAIL'

        payload = {
            'attachments': [{
                "color": f"{color}",
                "blocks": [
                    {
                        "type": "section",
                        "text": {
                            "type": "mrkdwn",
                            "text": f"{self.title}\n{self.server_div} :zap: "
                        }
                    },
                    {
                        "type": "section",
                        "fields": [
                            {
                                "type": "mrkdwn",
                                "text": f"*result:*\n{self.input_text}",
                            },
                            {
                                "type": "mrkdwn",
                                "text": f"*Status:*\n{status_text}",
                            },
                            {
                                "type": "mrkdwn",
                                "text": f"*Event Time:*\n{datetime.now().__str__()}",
                            }
                        ]
                    }
                ]}]}

        return payload


    def postingBatchInfo(self):
        """
        function info postingBatchInfo : slack 배치 입력 수행
        """

        slackurl = 'hook!'
        url = slackurl
        payload = self.make_attachment()
        byte_length = str(sys.getsizeof(payload))
        headers = {'Content-Type': 'application/json', "Content-Length": byte_length}

        requests.post(url=url, data=json.dumps(payload), headers=headers)



