import os
import json
import requests
import urllib2


class checkEvent:
        def __init__(self,req):
                self.req = req
                self.events = ['postback','message']

        def get_event(self):
                res = self.req['entry'][0]['messaging']

                for req in res:
                        for event in self.events:
                                if req.has_key(event):

                                        if event == 'message':
                                                if req['message'].has_key('quick_reply'):
                                                        return 'postback'

                                        return event

                        return None
