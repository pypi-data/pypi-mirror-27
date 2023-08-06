#!/usr/bin/env python
# coding: utf-8

from __future__ import unicode_literals, print_function

try:
    from http.cookies import SimpleCookie
except ImportError:
    from Cookie import SimpleCookie

import pyquery

from robobrowser import RoboBrowser


class RoboBrowserQuery(RoboBrowser):
    simple_cookie = None

    @property
    def query(self):
        if not hasattr(self.state, 'pyquery'):
            self.state.pyquery = pyquery.PyQuery(
                self.state.response.content)

        return self.state.pyquery

    def set_cookie_at_next_request(self, cookie_text):
        """
        DEPRECATED
        set cookie text.
        recommend: from django.utils.encoding import smart_str
                   set_cookie_at_next_request(smart_str(cookie_text))
        """
        self.simple_cookie = SimpleCookie()
        self.simple_cookie.load(cookie_text)

    def set_cookie(self, cookie_dict):
        """
        DEPRECATED
        :param cookie_dict:
        """
        self.session.cookies.set(**cookie_dict)

    def cookie_as_dict(self):
        """
        DEPRECATED
        """
        if not self.simple_cookie:
            return None
        return {k: v.value for k, v in self.simple_cookie.items()}

    def get_cookies(self):
        """
        :return: http.cookiejar.Cookie list
        For serialize, example django cache
        """
        return list(iter(self.session.cookies))

    def set_cookies(self, cookies):
        """
        From serialized, example django cache
        """
        for cookie in cookies:
            self.session.cookies.set_cookie(cookie)

    def open(self, *args, **kwargs):
        if self.simple_cookie:
            kwargs.update({'cookies': self.cookie_as_dict()})
        super(RoboBrowserQuery, self).open(*args, **kwargs)

    def preview(self):
        """
        Preview latest response with GUI web browser
        """
        import tempfile
        import subprocess

        f = tempfile.NamedTemporaryFile(delete=False)
        f.write(self.state.response.content)
        f.close()

        # for mac.
        subprocess.Popen(['open', f.name])
        # Auto delete required?
