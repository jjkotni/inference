import backend
import codecs
import json
import pickle
import os
import requests
from requests_futures.sessions import FuturesSession
import subprocess
import sys
import time
import logging
import pdb
import numpy as np

class BackendOW(backend.Backend):
    def __init__(self):
        super(BackendOW, self).__init__()
        self.inputs = []
        self.outputs = []
        #TODO: Get APIHOST and AUTH from .wskprops file
        self.APIHOST = 'https://172.17.0.1'
        self.session = FuturesSession(max_workers=15)
        # AUTH_KEY = subprocess.check_output(WSK_PATH + " property get --auth", shell=True).split()[2]
        self.AUTH_KEY = '23bc46b1-71f6-4ed5-8c54-816aa4f8c502:123zO3xZCLrMN6v2BKK1dXYFpXlPkccOFqm12CdAsMgRU4VrNZ9lyGVCGuMDGIwP'
        # self.AUTH_KEY = AUTH_KEY.decode("utf-8")
        self.user_pass = self.AUTH_KEY.split(':')
        self.NAMESPACE = '_'
        self.RESULT = 'false'
        self.base_url = self.APIHOST + '/api/v1/namespaces/' + self.NAMESPACE + '/actions/'
        # self.base_guest_url = self.apihost + '/api/v1/web/guest/default/'
        self.session = FuturesSession(max_workers=15)

    def version(self):
        return "1.0.dummy"

    def name(self):
        return "OpenWhisk"

    def image_format(self):
        return "NCHW"

    def load(self, model_path, inputs=None, outputs=None):
        self.inputs = inputs
        self.outputs = outputs
        return self
        # raise NotImplementedError("Backend:load")

    def predict(self, feed):
        #TODO: How do you get action?
        action = 'pilot'
        url = self.base_url + action
        # print(self.inputs)
        for field in self.inputs:
            if type(feed[field]) == np.ndarray:
                # print('Entered here')
                # feed[field] = json.dumps(feed[field].tolist())
                feed[field] = codecs.encode(pickle.dumps(feed[field]), "base64").decode()
        # print(type(feed[self.inputs[0]]))
        # params = json.dumps(feed)
        params = {'body':'test'}
        future = self.session.post(url, params={'blocking': True, 'result': True}, auth=(
                    self.user_pass[0], self.user_pass[1]), json=feed, verify=False)
        post_response = json.loads(future.result().content.decode())
        # print(post_response)
        return out
