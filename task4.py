import syslog
from cli import clid
import json

data = json.loads(clid("show ip route"))
route= [x["ipprefix"] for x in data['TABLE_vrf']['ROW_vrf']['TABLE_addrf']['ROW_addrf']['TABLE_prefix']['ROW_prefix']]

if " ".join(route) == "1.1.1.1/32 2.2.2.2/32 3.3.3.3/32":
    syslog.syslog(3, "We got 3 routes , mission completed!!!")