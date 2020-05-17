class config:
    
    class expressions:
        
        drop_expressions = [
            "cloudflare",
            "google",
            "twimg",
            "adfly",
            "adsense",
            "websocket",
            "socket",
            ".js",
            ".css",
            "captcha",
            "twitter.com/share"
            ]

        
        seek_expressions = [
            "@gmail.com",
            "@hotmail.com",
            "@yahoo.com",
            "@yandex.com",
            "@mail.com",
            "@mail.ru",
            "@google.com",
            "pastebin",
            "facebook.com",
            "youtube",
            "yandex",
            "huawei",
            "username",
            "auth",
            ".gov",
            "mil"
            ]




        
class glbls:
    
    # INTRINSINCS
    sought_expressions = config.expressions.seek_expressions
    drop_expressions = config.expressions.drop_expressions
    sesh_id = str()
    tld = str()
    data_dir = str()    
    usage_type = int()
    pool = list()
    current_url = ""
    last_pool_len = 0
    last_index = 0
    current_index_data = dict()
    tmp = dict()
    http_proxies = list()
    ssl_proxies = list()
    proxy_in_use = ""
    proxy_timeout_seconds = 8

    # FRONTEND GLOBALS
    host = None
    amount = None
    sleep_ = None
    bg_color = None
    b_grid = None
    b_label = None
    lbl_clr = None
    bool_ready = None

    # FRONTEND - THREAD CONTROL
    term = None
    shell_thread = None
    message = str()
    main_thread = None
    err_out = str()
    master_hook = None
