# Author: echel0n <echel0n@sickrage.ca>
# URL: https://sickrage.ca
#
# This file is part of SickRage.
#
# SickRage is free software: you can redistribute it and/or modify
# it under the terms of the GNU General Public License as published by
# the Free Software Foundation, either version 3 of the License, or
# (at your option) any later version.
#
# SickRage is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
# GNU General Public License for more details.
#
# You should have received a copy of the GNU General Public License
# along with SickRage.  If not, see <http://www.gnu.org/licenses/>.

from __future__ import unicode_literals

import feedparser
from feedparser import FeedParserDict

import sickrage
from sickrage.core.websession import WebSession


def getFeed(url, params=None, request_headers=None, handlers=None):
    try:
        resp = WebSession().get(url, params=params)
        if resp.ok:
            return feedparser.parse(
                resp.text,
                agent=sickrage.app.user_agent,
                etag=False,
                modified=False,
                request_headers=request_headers,
                handlers=handlers
            )
    except Exception as e:
        sickrage.app.log.debug("RSS Error: {}".format(e.message))

    return FeedParserDict()
