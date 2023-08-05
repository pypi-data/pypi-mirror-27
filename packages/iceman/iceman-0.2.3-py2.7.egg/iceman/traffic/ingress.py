# -*- coding: utf-8 -*-
"""iceman/Traffic/ingress.py
"""
from iceman.traffic.traffic import Traffic

class Ingress(Traffic):
    """Ingress Traffic implementation

    :param protocol: tcp or udp
    :type cipher_suite: str

    :param queue: queue number
    :type cipher_suite: int

    :param cipher_suite: crypto wrapper cipher strategy
    :type cipher_suite: instance

    :param encryption_enabled: encryption flag
    :type encryption_enabled: bool
    """

    def callback(self, payload):
        """nfqueue callback
        """
        self.transform('decrypt', payload)
