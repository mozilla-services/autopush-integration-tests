import json

REQUEST_TIMEOUT = 3.0
LINE = '----------------------------'


class UrlChecker(object):

    def __init__(self, application, env_selected, test_manifest):

        self.test_manifest = test_manifest
        self.application = application
        self.env_selected = env_selected

    def _header_label(self, env=''):

        if env:
            env = '({0})'.format(env.upper())
        label = 'URL CHECKS {0}'.format(env)
        return '{0}\n{1}\n{2}\n\n'.format(LINE, label, LINE)

    def _http_request(self, url):
        # requests: r.status_code, r.headers, r.content

        import requests
        out = ''
 
        try:
            response = requests.get(url, timeout=REQUEST_TIMEOUT)
            response_time = requests.get(url).elapsed.total_seconds() 
            if response.history:
                out += "Request was redirected!\n"
                for resp in response.history:
                    print( resp.status_code, resp.url)
                out += 'status code: {0} --> destination: {1}\n'.format(
                    response.status_code, response.url)
            else:
                try:
                    j = json.loads(response.content)
                    out += json.dumps(j, indent=4)
                except ValueError:
                    out = response.content
            out += '\nResponse time: {0}\n'.format(response_time)
        except requests.exceptions.Timeout:
            out += ">>> ERROR! Request timed out! <<<\n"
        return out + '\n\n'

    def substitute_param(self, manifest, env, val):

        import re
        # TODO: we need to pass env var
        env = env.lower()
        # if we have a param in brackets, we substitute it for an url
        # with a key indicated:  <key_name_here>
        # example:
        # <root> becomes:  https://xxx.services.mozilla.com
        param = re.search(r'<(.*)>', val)
        if param:
            key_substitute = param.group(1)
            val = manifest["envs"][env]["urls"][key_substitute]
            val = 'https://{0}'.format(val)
        return val

    def verify_urls(self, urls):

        out = ''
        for url in urls:
            # TODO: iterate thru protocols
            out += '{0}:\n'.format(url)
            out += str(self._http_request(url))
        return out + '\n\n'

    def main(self, manifest):

        out = ''
        env_selected = self.env_selected.lower()

        environment = self.env_selected
        out += self._header_label(environment)

        urls = self.test_manifest.urls(manifest, env_selected)
        out += self.verify_urls(urls)

        return out

if __name__ == '__main__':

    # example
    application = 'loop-server'
    ec2 = EC2Handler()

    checker = UrlChecker(
        self, application, env_selected, host_string, 
        instance_properties, test_manifest
    )

    print('================')
    checker.main()
