#!/usr/bin/env python

import re
import locale
import datetime
import urllib2
import json

import mechanize
import cookielib

facebook_url = 'https://www.facebook.com'
email = 'dimva13@gmail.com'
password = ''
statuses = ['Going', 'Maybe', 'Invited']

app_id = '103589486427618'
app_secret = 'e84ac39202bd4b44ce3d692e9ed2c7dd'

TIMEOUT = 10.0

class Api(object):
    def __init__(self):
        self._token = None

    def login(self):
        self._token = urllib2.urlopen('https://graph.facebook.com/oauth/access_token?client_id={0}&client_secret={1}&grant_type=client_credentials'.format(app_id, app_secret)).read()

    def get_info(self, event_id):
        if self._token is not None:
            try:
                return self._get_info(event_id)
            except Exception:
                pass

        # got here if not logged in or error
        self.login()
        return self._get_info(event_id)

    def _get_info(self, event_id):
        return json.load(urllib2.urlopen('https://graph.facebook.com/{0}?{1}'.format(event_id, self._token)))

class Facebook(object):
    def __init__(self):
        self._logged_in = False
        self._br = br = mechanize.Browser()

        # Cookie Jar
        cj = cookielib.LWPCookieJar()
        br.set_cookiejar(cj)

        # Browser options
        br.set_handle_equiv(True)
        br.set_handle_redirect(True)
        br.set_handle_referer(True)
        br.set_handle_robots(False)

        # emulate firefox
        br.addheaders = [('User-agent', 'Mozilla/5.0 (X11; U; Linux i686; en-US; rv:1.9.0.1) Gecko/2008071615 Fedora/3.0.1-1.fc9 Firefox/3.0.1')]

    def login(self, url=facebook_url):
        """returns the data of the page after logging in"""
        br = self._br

        resp = br.open(url, timeout=TIMEOUT)

        br.select_form(nr=0)
        br.form.set_value(email, name='email')
        br.form.set_value(password, name='pass')
        response = br.submit()
        data = response.get_data()

        self._logged_in = True

        return data

    def get_stats(self, event_id):
        url = '{0}/events/{1}'.format(facebook_url, event_id)

        if self._logged_in:
            try:
                return parse(self._get_page(url))
            except Exception:
                pass # fall through

        # code runs when not logged in or when error
        return parse(self.login(url))

    def _get_page(self, url):
        return self._br.open(url, timeout=TIMEOUT).get_data()

def parse(data):
    ret = {
        'time': datetime.datetime.now()
    }

    for status in statuses:
        text = re.search(r"{0} \(((\d|,)+?)\)".format(status), data).group(1)
        ret[status.lower()] = int(text.replace(',', ''))

    return ret

if __name__ == '__main__':
    fb = Facebook()
    print fb.get_stats(198328520252594)
