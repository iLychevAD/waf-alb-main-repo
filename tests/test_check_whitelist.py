import pytest
import requests
from pprint import pprint as pp

def check_code(url : str, code : int) -> bool:
    if ( '/' in url ):
        ( host, path ) = url.split('/', 1)
    else:
        ( host, path ) = ( url, "" )
    print(f'H: {host}, P: {path}')
    lb_endpoint = os.environ.get('WAF_LB_ENDPOINT', '')
    return requests.get(f'http://{lb_endpoint}/{path}', headers={'Host': host}).status_code == code

raw_testdata = '''
    OK foo.waf-acme-lb.example.com/static/
    OK bar.waf-acme-lb.example.com/static/
    OK foo.waf-acme-lb.example.com/static/foo
    OK bar.waf-acme-lb.example.com/static/foo
    OK foo.waf-acme-lb.example.com/static/foo/bar
    OK bar.waf-acme-lb.example.com/static/foo/bar
    NA foo.waf-acme-lb.example.com/status
    NA bar.waf-acme-lb.example.com/status
    NA foo.waf-acme-lb.example.com
    NA bar.waf-acme-lb.example.com

    OK foo.waf-acme-lb.example.com/webhook
    OK bar.waf-acme-lb.example.com/webhook
    NA foo.waf-acme-lb.example.com/webhook/viber
    NA bar.waf-acme-lb.example.com/webhook/viber

    OK foo.waf-acme-lb.example.com/webhooks/viber
    NA bar.waf-acme-lb.example.com/webhooks/viber

    OK bar.waf-acme-lb.example.com/webhooks/facebook/webhook
    NA bar.waf-acme-lb.example.com/webhooks/facebook/webhook/foo
    NA foo.waf-acme-lb.example.com/webhooks/facebook/webhook
'''

testdata = [ ( line.strip().split() ) for line in raw_testdata.splitlines() if line ]

@pytest.mark.parametrize("expected,url", testdata)
def test_whitelist(expected : str, url : str):
    code = 200 if ( expected == "OK" ) else 403
    assert check_code(url, code) == True
