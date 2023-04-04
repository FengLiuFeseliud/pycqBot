实现 pixiv 搜图/pid/用户

## 插件配置

> **`forward_qq`** 转发使用的 qq 号
>
> **`forward_name`** 转发使用的名字
>
> **`cookie`** pixiv 用户 cookie
>
> **`proxy`** 代理 ip
>
> **`max_pid_len`** pid 最多返回多少图片 默认 20
>
> **`max_rlen`** 其它功能最多返回多少图片 默认 10

在 plugin_config.yml 配置插件

这是我一个 bot 目前用的配置，可以参考

```yaml
# plugin_config.yml

pixiv: 
    forward_qq: qq 号
    forward_name: "涩图"
    cookie: 用户 cookie
    # clash 代理默认端口 7890
    proxy: "127.0.0.1:7890"
    max_pid_len: 60
```

## 插件指令

> **`[指令标识符]搜索用户 [用户名] [指定量] [模式(可选)]`** 从指定用户返回指定量图 最后加上模糊 将使用模糊搜索
>
> **`[指令标识符]搜索作品 [用户名] [标签]`** 从指定标签返回指定量图
>
> **`[指令标识符]图来`** 从本 bot pixiv 用户 关注画师返回随机5张图
>
> **`[指令标识符]pid [pid]`** 从指定 pid 返回图