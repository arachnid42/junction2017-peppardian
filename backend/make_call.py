#!/usr/bin/env python2

import requests


class PhoneController:
    
    def __init__(self):
        self.API_USERNAME = "u75ad4186753ab834b55705ddcf83a539"
        self.API_PASSWORD = "1D287B5B037A00A9F065A3ADC469044D"
        self.URL_CALL = "https://api.46elks.com/a1/Calls"
        self.URL_SMS = "https://api.46elks.com/a1/SMS"
        self.sender = '+37253934021'
        self.audio_file = '{"play":"http://www.fromtexttospeech.com/output/0261326001511704090/30447358.mp3"}'
        self.auth = (
                self.API_USERNAME,
                self.API_PASSWORD
                )

    def send_sms(self, receiver, msg):
        data = {
            'from': self.sender,
            'to': receiver,
            'message': msg
            }
        response = requests.post(self.URL_SMS,
                                 auth=self.auth,
                                 data=data)
        return response.text

    def make_call(self, receiver):
        data = {
            'from': self.sender,
            'to': receiver,
            'voice_start': self.audio_file
            }       
        response = requests.post(self.URL_CALL,
                                 auth=self.auth,
                                 data=data)
        return response.text

if __name__ == '__main__':
    pc = PhoneController()

