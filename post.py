#!/usr/bin/env python3
import subprocess
import random
import time
import string
import sys
user = "CHANGEME"
pw = "CHANGEME"
r = random.Random()
date = subprocess.check_output(["date", "+%a, %d %b %Y %T %z"]).decode("utf-8").rstrip() # strftime to the rescue
post = "<" + "".join(r.sample(string.ascii_letters, 18)) + str(int(time.time())) + "@bar2.ano>" # 18 random letters then the epoch
# References: <referenced message-id>
# X-Sage: optional
# Date: Thu, 02 May 2013 12:16:44 +0000
header = """Content-Type: text/plain; charset=UTF-8
Content-Transfer-Encoding: 8bit
From: anonymous <foo@bar1.ano>
Date: """ + date + """
Message-ID: """ + post + """
Newsgroups: overchan.test
References: <KkYZQOveHGXLljPiVh1491093559@foo.bar>
Subject: None
Path: bar3.ano"""

from twisted.internet import reactor, protocol
import twisted.protocols.basic

class client(twisted.protocols.basic.LineReceiver):
    def sl(self, line): # send string line
        print("Send: " + line)
        self.sendLine(line.encode("utf-8"))
    def lineReceived(self, data):
        data = data.decode("utf-8")
        print("Recv: " + data)
        data = data.split()
        if data[0] == "200" or data[0] == "281":  # posting allowed or authentication successful
            self.sl("IHAVE " + post)
        if data[0] == "335":  # server sends back "335 send it plz"
            self.sl(header)
            self.sl("")
            self.sl(open(" ".join(sys.argv[1:]), "r").read())
            self.sl(".")
        if data[0] == "235":  # server sends back "235 i got it"
            self.sl("QUIT")
        if data[0] == "205":  # server sends back "205 bai"
            reactor.stop()
            # sys.exit(0)
        if data[0] == "483":  # authentication required before posting
            self.sl("AUTHINFO USER " + user)
        if data[0] == "381":  # password required
            self.sl("AUTHINFO PASS " + pw)


class fac(protocol.ClientFactory):
    protocol = client


# this connects the protocol to a server running on port 8000
reactor.connectTCP("10.8.0.1", 1199, fac())
reactor.run()
