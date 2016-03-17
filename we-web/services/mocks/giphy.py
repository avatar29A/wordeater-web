# coding=utf-8

import json


class GiphyFake(object):
    def random(self, tag=None):
        response = u'{"meta": {"status": 200, "msg": "OK"}, "data": {"fixed_height_small_height": "100", "fixed_width_small_width": "100", "fixed_height_small_still_rl": "http://media2.giphy.com/media/c5wlymFp02Amc/100_s.gif", "id": "c5wlymFp02Amc", "fixed_height_small_rl": "http://media2.giphy.com/media/c5wlymFp02Amc/100.gif", "fixed_width_small_height": "100", "caption": "", "fixed_height_downsampled_width": "200", "image_width": "245", "fixed_width_small_still_rl": "http://media2.giphy.com/media/c5wlymFp02Amc/100w_s.gif", "type": "gif", "sername": "", "image_mp4_url": "http://media2.giphy.com/media/c5wlymFp02Amc/giphy.mp4", "image_frames": "16", "fixed_width_downsampled_url": "http://media2.giphy.com/media/c5wlymFp02Amc/200w_d.gif", "fixed_width_downsampled_width": "200", "url": "http://giphy.com/gifs/spn-c5wlymFp02Amc", "fixed_width_downsampled_height": "200", "fixed_height_downsampled_height": "200", "fixed_height_downsampled_rl": "http://media2.giphy.com/media/c5wlymFp02Amc/200_d.gif", "fixed_height_small_width": "100", "image_height": "245", "image_url": "http://media2.giphy.com/media/c5wlymFp02Amc/giphy.gif", "fixed_width_small_url": "http://media2.giphy.com/media/c5wlymFp02Amc/100w.gif", "image_original_url": "http://media2.giphy.com/media/c5wlymFp02Amc/giphy.gif"}}'

        return json.loads(response)
