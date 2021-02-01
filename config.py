#!/usr/bin/env python3
# Copyright (c) Microsoft Corporation. All rights reserved.
# Licensed under the MIT License.

import os

class DefaultConfig:
    """ Bot Configuration """

    PORT = 3978
    APP_ID = os.environ.get("MicrosoftAppId", "bc4fdbe8-a324-4513-bcc7-5510260dd85d")
    APP_PASSWORD = os.environ.get("MicrosoftAppPassword", "jfor5qLdi8pf8t5Cjj-Hz_~9-KjA.vgb4_")