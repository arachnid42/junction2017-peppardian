"""."""
import requests
import base64


class ImageSender(object):
    """."""

    def __init__(self, endpoint):
        """."""
        self.endpoint = endpoint

    def send_image(self, path):
        """."""
        with open(path, 'rb') as im:
            files = {'file': ('image.jpg', im)}
            r = requests.post(
                    url=self.endpoint,
                    data={
                        "enctype": "multipart/form-data"
                         },
                    files=files
                    )
            return r.text


if __name__ == '__main__':
    imsend = ImageSender('http://0.0.0.0:5555/submit_image')
    imsend.send_image('/home/ddnomad/pictures/artem_conference.jpg')
