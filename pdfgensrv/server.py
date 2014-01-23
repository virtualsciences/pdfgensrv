import os
import subprocess
import tempfile
import logging
import urllib
from urlparse import urlparse
from cStringIO import StringIO
from otto import Application as BaseApplication
from webob import Response

logger = logging.getLogger('pdfsrvgen')

class Application(BaseApplication):

    def set_config(self, wk_path):
        self.wk_path = wk_path
        self.notify_url = ''

app = Application()


def app_factory(global_config, **local_config):
    """ creates an otto WSGI-compliant HTTP publisher. """
    app.set_config(local_config['wk_path'])
    logger.info('wd_path: %s' % local_config['wk_path'])
    return app


def create_pdf(wk_path, url, cookies):
    os_handle, pdf_path = tempfile.mkstemp(suffix='.pdf')
    args = [wk_path, url]
    for k, v in cookies.items():
        args.extend(['--cookie', k, v])
    args.extend(['--disable-javascript', '--load-error-handling', 'ignore'])
    args.append(pdf_path)
    p = subprocess.Popen(args)
    p.wait()
    buf = StringIO()
    pdf_file = open(pdf_path, 'r')
    buf.write(pdf_file.read())
    pdf_file.close()
    os.remove(pdf_path)
    return buf


@app.connect('/')
def main_handler(request):
    q_url = request.GET.get('url')
    if q_url is None:
        return Response(content_type='text/plain',
                    body='No url specified.')
    url = urllib.unquote(q_url)
    if request.host.split(':')[0].lower() != urlparse(url).hostname:
        logger.info("Tried illegal host: %s" % url)
        return Response(content_type='text/plain',
                    body='Only for same website', status=403)
    if url is not None:
        try:
            buf = create_pdf(app.wk_path, url, request.cookies)
        except Exception, e:
            logger.error('Unable to create pdf: %s' % str(e))
            return Response(content_type='text/plain',
                        body='Error occurred, contact the site administrator.')
    return Response(content_type='application/pdf',
                    body=buf.getvalue())
