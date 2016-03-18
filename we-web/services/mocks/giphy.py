# coding=utf-8


class GiphyFake(object):
    def random(self, tag=None):
        with open('data/dog.gif', 'r') as f:
            return f.readall()
