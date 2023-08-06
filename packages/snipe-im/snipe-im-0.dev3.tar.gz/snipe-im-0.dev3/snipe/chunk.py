# -*- encoding: utf-8 -*-
# Copyright © 2017 the Snipe contributors
# All rights reserved.
#
# Redistribution and use in source and binary forms, with or without
# modification, are permitted provided that the following conditions
# are met:
#
# 1. Redistributions of source code must retain the above copyright
# notice, this list of conditions and the following disclaimer.
#
# 2. Redistributions in binary form must reproduce the above
# copyright notice, this list of conditions and the following
# disclaimer in the documentation and/or other materials provided
# with the distribution.
#
# THIS SOFTWARE IS PROVIDED BY THE COPYRIGHT HOLDERS AND
# CONTRIBUTORS "AS IS" AND ANY EXPRESS OR IMPLIED WARRANTIES,
# INCLUDING, BUT NOT LIMITED TO, THE IMPLIED WARRANTIES OF
# MERCHANTABILITY AND FITNESS FOR A PARTICULAR PURPOSE ARE
# DISCLAIMED. IN NO EVENT SHALL THE COPYRIGHT HOLDER OR CONTRIBUTORS
# BE LIABLE FOR ANY DIRECT, INDIRECT, INCIDENTAL, SPECIAL,
# EXEMPLARY, OR CONSEQUENTIAL DAMAGES (INCLUDING, BUT NOT LIMITED
# TO, PROCUREMENT OF SUBSTITUTE GOODS OR SERVICES; LOSS OF USE,
# DATA, OR PROFITS; OR BUSINESS INTERRUPTION) HOWEVER CAUSED AND ON
# ANY THEORY OF LIABILITY, WHETHER IN CONTRACT, STRICT LIABILITY, OR
# TORT (INCLUDING NEGLIGENCE OR OTHERWISE) ARISING IN ANY WAY OUT OF
# THE USE OF THIS SOFTWARE, EVEN IF ADVISED OF THE POSSIBILITY OF
# SUCH DAMAGE.
'''
snipe.chunk
----------

Chunk type
'''


class Chunk:
    def __init__(self, data=()):
        self.contents = []
        self.extend(data)

    def extend(self, data):
        for tag, text in data:
            self.append((tag, text))

    def append(self, chunklet):
        tag, text = chunklet
        self.contents.append((tuple(tag), str(text)))

    def __getitem__(self, k):
        return Chunk(self.contents[k])

    def __setitem__(self, k, v):
        self.contents[k] = list(Chunk(v))

    def __len__(self):
        return len(self.contents)

    def __iter__(self):
        for tag, text in self.contents:
            yield tag, text

    def __repr__(self):
        return self.__class__.__name__ + '(' + repr(self.contents) + ')'

    def __add__(self, a, b):
        x = Chunk(a)
        x.extend(b)
        return x

    def __iadd__(self, a, b):
        self.extend(b)
