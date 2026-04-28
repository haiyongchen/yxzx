import sys
sys.path.insert(0, r'D:\openclaw-workspace\skills\epoint-oa-api\scripts')
from oa_api import call_api
call_api('mail_getunreadlist_v7', '{"currentpageindex": 0, "pagesize": 10}')
