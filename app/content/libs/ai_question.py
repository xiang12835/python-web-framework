# coding=utf-8
import json
import requests
import logging


class AiQuestion(object):
    """ 智能问答

    """

    def __init__(self):
        self.ai_category_url = "https://www.yzdongfang2.com/bsk/ai/v1.0/classify/"

    def send_get_request(self):
        r = requests.get(self.ai_category_url)
        return r.json()

    def send_post_request(self, payload):
        r = requests.post(self.ai_category_url, data=payload, timeout=2)
        return r.json()

    def get_ai_category_info(self, commentId, reviewContent, category_id, reviewPic=""):
        payload = {
            "commentId": commentId,
            "reviewContent": reviewContent,
            "category_id": category_id,
        }
        if reviewPic:
            payload.update({"reviewPic": reviewPic})
        json_data = self.send_post_request(payload)
        return json_data


if __name__ == "__main__":
    commentId = '201806131028377875382187'
    reviewContent = '强烈要求旭哥回话，我是山东d类考生。感谢乡村振兴给我压中。行测考的有点小不开心。但是我进面以后报我们线下的班。能有针对d类的面试课程吗。'
    category_id = '201803281522068219340211'
    reviewPic = ''

    json_data = AiQuestion().get_ai_category_info(commentId, reviewContent, category_id, reviewPic)
    print json_data
    print json.dumps(json_data, ensure_ascii=False, sort_keys=True, indent=4)
