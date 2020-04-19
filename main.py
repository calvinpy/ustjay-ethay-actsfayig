import os

import requests
from flask import Flask, send_file, Response
from bs4 import BeautifulSoup

app = Flask(__name__)


def get_fact():
    response = requests.get("http://unkno.com")

    soup = BeautifulSoup(response.content, "html.parser")
    facts = soup.find_all("div", id="content")

    return facts[0].getText(strip=True)


def translate():
    input_text = get_fact()

    # Either way seems to work using the request.url or headers['Location']
    post_request = requests.post("https://hidden-journey-62459.herokuapp.com/piglatinize/",
                                 data={'input_text': input_text})

    post_no_redirect = requests.post("https://hidden-journey-62459.herokuapp.com/piglatinize/",
                                     data={'input_text': input_text}, allow_redirects=False)

    return post_request.url, post_no_redirect.headers['Location']


@app.route('/')
def home():
    pig_link1, pig_link2 = translate()
    return '<a href="{0}">{0}</a>'.format(pig_link2)


if __name__ == "__main__":
    port = int(os.environ.get("PORT", 6787))
    app.run(host='0.0.0.0', port=port)
