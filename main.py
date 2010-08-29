#!/usr/bin/env python
# -*- coding: utf-8 -*-
import logging
import swfutil
import urllib

from google.appengine.ext import webapp
from google.appengine.ext.webapp import util
from google.appengine.api import urlfetch

class MainHandler(webapp.RequestHandler):
    def get(self):
        self.response.out.write('''<html>
    <head><title>Test</title></head>
    <body>
        <div id="description">
        以下のページにあるような、Flash Lite のファイルへのパラメタの埋め込みをGAE上でやってみました。
        <p>
          <a href="http://libpanda.s18.xrea.com/test_insert/sample.html">http://libpanda.s18.xrea.com/test_insert/sample.html</a>
        </p>
        Pythonのコードは以下の記事を参考にしてます。
        <p>
          <a href="http://nakagami.blog.so-net.ne.jp/2010-02-02" class="exlink">Python 3.x で Flash Lite 1.1 のパラメータ埋め込み：ある nakagami の日記：So-netブログ</a>
        </p>

        </div>
        <div style="margin:50px; padding: 20px; border: 1px solid gray">
            以下のフォームを適当に入力して「作成」を押すと、入力した文字を埋め込んだSWFのバイナリが生成されます。
            <form method="post" action="do_generate">
                <ul>
                    <li>セリフ:     <input type="text" name="serif" value="ちんぽっぽ" /></li>
                    <li>ジャンプ音: <input type="text" name="jumpsound" value="ぽいんっ" /></li>
                </ul>
                <input type="submit" value="作成"/>
            </form>
        </div>
        <div id="contact">
            連絡先など:
            <ul>
                <li>e-mail: <a href="mailto:snaka.gml@gmail.com">snaka.gml@gmail.com</a></li>
                <li>blog: <a href="http://d.hatena.ne.jp/snaka72/">http://d.hatena.ne.jp/snaka72/</a></li>
            </ul>
        </div>
    </body>
</html>''')

class DoGenerateHandler(webapp.RequestHandler):
    def post(self):
        serif = self.request.get('serif')
        jumpsound = self.request.get('jumpsound')
        res = """<html>
    <head><title>Flash lite vars for GAE</title></head>
    <body>
        <embed height='100%%' width='100%%' name='plugin' src='generated_swf?%s' type='application/x-shockwave-flash' />
    </body>
</html>""" % urllib.urlencode({
            'serif' : serif.encode('utf8'),
            'jumpsound' : jumpsound.encode('utf8')
        })
        self.response.out.write(res)

class SwfGenerator(webapp.RequestHandler):
    def get(self):
        param = {}
        param['serif'] = self.request.get('serif')
        param['jumpsound'] = self.request.get('jumpsound')

        base_swf = urlfetch.fetch('http://libpanda.s18.xrea.com/test_insert/x/base.swf')
        modified_swf = swfutil.create_swf(base_swf.content, param)

        self.response.headers['Content-Type'] = 'application/x-shockwave-flash'
        self.response.out.write(modified_swf)

def main():
    application = webapp.WSGIApplication([('/', MainHandler),
                                          ('/do_generate', DoGenerateHandler),
                                          ('/generated_swf', SwfGenerator)],
                                         debug=True)
    util.run_wsgi_app(application)


if __name__ == '__main__':
    main()
