import os
import sys
def pytest_sessionstart(session):
    lb_endpoint = os.environ.get('WAF_LB_ENDPOINT', '')
    if ( not lb_endpoint ):
        sys.exit('provide load balancer endpoint in the WAF_LB_ENDPOINT env variable!')
