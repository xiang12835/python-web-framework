upstream make_app_api {
    server 127.0.0.1:10000 fail_timeout=0;
    server 127.0.0.1:10001 fail_timeout=0;
    server 127.0.0.1:10002 fail_timeout=0;
    server 127.0.0.1:10003 fail_timeout=0;
}

# init lua
#lua_code_cache on;


server {
    listen 80;
    server_name h5.platform.winlesson.com;
    charset utf-8;

    set $x_remote_addr $proxy_add_x_forwarded_for;


    location  /static/ {
        # deny all;
        alias /data/python/it_platform/app/statics/;
        expires 15m;
    }

    if ($x_remote_addr = "") {
        set $x_remote_addr $remote_addr;
    }


    location ~ /is/ {

        #access_by_lua_file conf/lua/check_pid_signature.lua;

        proxy_pass          http://make_app_api;
        proxy_connect_timeout 3;
        proxy_send_timeout 3;
        proxy_read_timeout 3;
        proxy_redirect      default;
        proxy_set_header    X-Forwarded-For $proxy_add_x_forwarded_for;
        proxy_set_header    X-Real-IP $x_remote_addr;
        proxy_set_header    Host $http_host;
        proxy_set_header    Range $http_range;
    }
}


