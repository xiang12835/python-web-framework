# -*- coding: utf-8 -*-
# from django.conf import settings
import os
from django.conf import settings


def gen_signature(appid, content):

    tool_path = settings.SIG_TOOL_PATH
    key_path = settings.SIG_KEY_PATH
    sig_path = settings.SIG_PATH  #'/mydata/python/live_video/api/util/tencenttools/tls_sig_api-linux-64/tools'

    
    cmd = '%s/tls_licence_tools gen %s/private_key %s/%s_sig %s %s >&null;cat %s/%s_sig' % (
        tool_path, key_path, sig_path ,content , appid, content, sig_path, content
    )

    p = os.popen(cmd)
    sig = p.read()
    #print sig
    #remove key file
    rm_cmd = 'rm -f %s/%s_sig' % (sig_path, content)
    os.system(rm_cmd)
    
    return sig

if __name__ == "__main__":
    print gen_signature(appid=10023919, content='1234')
