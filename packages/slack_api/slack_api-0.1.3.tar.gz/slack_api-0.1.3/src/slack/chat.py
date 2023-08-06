#!/usr/bin/python
# -*- coding: utf-8 -*-

# Hive Slack API
# Copyright (c) 2008-2017 Hive Solutions Lda.
#
# This file is part of Hive Slack API.
#
# Hive Slack API is free software: you can redistribute it and/or modify
# it under the terms of the Apache License as published by the Apache
# Foundation, either version 2.0 of the License, or (at your option) any
# later version.
#
# Hive Slack API is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE. See the
# Apache License for more details.
#
# You should have received a copy of the Apache License along with
# Hive Slack API. If not, see <http://www.apache.org/licenses/>.

__author__ = "João Magalhães <joamag@hive.pt>"
""" The author(s) of the module """

__version__ = "1.0.0"
""" The version of the module """

__revision__ = "$LastChangedRevision$"
""" The revision number of the module """

__date__ = "$LastChangedDate$"
""" The last change date of the module """

__copyright__ = "Copyright (c) 2008-2017 Hive Solutions Lda."
""" The copyright for the module """

__license__ = "Apache License, Version 2.0"
""" The license for the module """

import json

class ChatAPI(object):

    def post_message_chat(
        self,
        channel,
        text,
        parse = None,
        link_names = None,
        attachments = None,
        username = None,
        as_user = None
    ):
        url = self.base_url + "chat.postMessage"
        contents = self.post(
            url,
            channel = channel,
            text = text,
            parse = parse,
            link_names = link_names,
            attachments = json.dumps(attachments),
            username = username,
            as_user = as_user
        )
        return contents
