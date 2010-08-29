#/usr/bin/env pyton
# -*- coding: utf-8 -*-
#
# Embed parameters to Flash Lite 1.1/2.0
# modified by snaka based on following source code
# It works with Python 2.5 (maybe GAE/Python also)
#
# --- original credit ---
# Embed parameters to Flash Lite 1.1/2.0
# It works with Python 3.x.
# Author - Hajime Nakagami<nakagami@da2.so-net.ne.jp>
# License - BSD licence (http://www.opensource.org/licenses/bsd-license.php)
# Version 0.1 (2010/02/02) Initial release
# Version 0.2 (2010/02/26) For Flash Lite 2.0
# ------------------------

from struct import pack
import zlib

def _ib(v, n):
    "Convert from little endian int v to n bytes bytes"
    result = v
    if n == 2:
        result = pack('<h', v)
    elif n == 4:
        result = pack('<l', v)
    #print '%s -> %s' % (repr(v), repr(result))
    return result

def _calctaglen(d, encoding):
    n = 0
    for k in d:
        n += len(k.encode(encoding)) + len(d[k].encode(encoding)) + 11
    return n + 1

def _maketag(d, encoding):
    tag = '\x3f\x03'
    tag += _ib(_calctaglen(d, encoding), 4)
    for k in d:
        kv = k.encode(encoding)
        v = d[k].encode(encoding)
        tag += '\x96'+_ib(len(kv)+2, 2)+'\x00'+kv+'\x00'
        tag += '\x96'+_ib(len(v)+2, 2)+'\x00'+v+'\x00'
        tag += '\x1d'
    return tag + '\x00'

def create_swf(src_swf, params):
    "Create Flash Lite 1.1/2.0 swf file with embeded params."
    base_swf = src_swf[:]
    if base_swf[0] == 0x43:  #CWS (means 'Compressed')
        base_swf = base_swf[:8] + zlib.decompress(base_swf[8:])
    if ord(base_swf[3]) > 6:
        encoding = 'utf8'
    else:
        encoding = 'cp932'
    tag = _maketag(params, encoding)
        
    #rectbit = base_swf[8] >> 3
    rectbit = ord(base_swf[8]) >> 3
    head_len = int(((( 8 - ((rectbit*4+5)&7) )&7)+ rectbit*4 + 5 )/8) + 12 + 5;
    head = base_swf[:head_len]
    tail = base_swf[head_len:]
    newhead = head[:4] + _ib(len(base_swf) + len(tag), 4) + head[8:]
    new_swf = newhead + tag + tail
    if new_swf[0] == 0x43:  #CWS
        new_swf = new_swf[:8] + zlib.compress(new_swf[8:])
    return new_swf

if __name__ == '__main__':
    from urllib import urlopen
    # See http://libpanda.s18.xrea.com/test_insert/sample.html
    src_swf = urlopen('http://libpanda.s18.xrea.com/test_insert/x/base.swf').read()
    params = {
        'serif': u'ちんぽっぽ',
        'jumpsound': u'ぽいんっ！',
    }
    out_file = open('output.swf', 'wb')
    out_file.write(create_swf(src_swf, params))
