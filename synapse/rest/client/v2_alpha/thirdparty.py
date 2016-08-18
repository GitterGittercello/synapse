# -*- coding: utf-8 -*-
# Copyright 2015, 2016 OpenMarket Ltd
#
# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
#
#     http://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.


import logging

from twisted.internet import defer

from synapse.http.servlet import RestServlet
from ._base import client_v2_patterns

logger = logging.getLogger(__name__)


class ThirdPartyUserServlet(RestServlet):
    PATTERNS = client_v2_patterns("/3pu(/(?P<protocol>[^/]+))?$",
                                  releases=())

    def __init__(self, hs):
        super(ThirdPartyUserServlet, self).__init__()

        self.appservice_handler = hs.get_application_service_handler()

    @defer.inlineCallbacks
    def on_GET(self, request, protocol):
        fields = request.args
        del fields["access_token"]

        # TODO(paul): Some type checking on the request args might be nice
        #   They should probably all be strings
        results = yield self.appservice_handler.query_3pu(protocol, fields)

        defer.returnValue((200, results))


def register_servlets(hs, http_server):
    ThirdPartyUserServlet(hs).register(http_server)
