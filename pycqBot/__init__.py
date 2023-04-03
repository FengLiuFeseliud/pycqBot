from pycqBot.cqApi import cqBot, cqHttpApi, cqLog
from pycqBot.object import Plugin, cqEvent


__VERSIONS__ = "v0.5.0"


TIT = """
#################################################################
██████╗ ██╗   ██╗ ██████╗ ██████╗ ██████╗  ██████╗ ████████╗
██╔══██╗╚██╗ ██╔╝██╔════╝██╔═══██╗██╔══██╗██╔═══██╗╚══██╔══╝
██████╔╝ ╚████╔╝ ██║     ██║   ██║██████╔╝██║   ██║   ██║   
██╔═══╝   ╚██╔╝  ██║     ██║▄▄ ██║██╔══██╗██║   ██║   ██║   
██║        ██║   ╚██████╗╚██████╔╝██████╔╝╚██████╔╝   ██║   
╚═╝        ╚═╝    ╚═════╝ ╚══▀▀═╝ ╚═════╝  ╚═════╝    ╚═╝   
                                            {__VERSIONS__}  BY FengLiu
#################################################################
""".format(__VERSIONS__=__VERSIONS__)

# 默认生成框架 cgo-cqhttp 配置
GO_CQHTTP_CONFIG = """# go-cqhttp 详细配置见 go-cqhttp 文档 https://docs.go-cqhttp.org/guide/config
account:
    encrypt: false
    status: 0
    relogin:
        delay: 3
        interval: 3
        max-times: 0
    use-sso-address: true
    allow-temp-session: true

heartbeat:
    interval: 40

message:
    post-format: string
    ignore-invalid-cqcode: false
    force-fragment: false
    fix-url: false
    proxy-rewrite: ''
    report-self-message: false
    remove-reply-at: false
    extra-reply-data: false
    skip-mime-scan: false

output:
    log-level: trace
    log-aging: 15
    log-force-new: true
    log-colorful: true
    debug: false

default-middlewares: &default
    access-token: ''
    filter: ''
    rate-limit:
        enabled: false 
        frequency: 1
        bucket: 1

database:
    leveldb:
        enable: true

    cache:
        image: data/image.db
        video: data/video.db

servers:
    - http:
        host: 127.0.0.1
        port: 5700
        timeout: 5
        middlewares:
            <<: *default
        post:

    - ws:
        host: 127.0.0.1
        port: 8080
        middlewares:
            <<: *default
"""
