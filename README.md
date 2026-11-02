# phidata
把斐讯m1数值转发到邮箱

使用hosts劫持取出m1数值转发到局域网内的NanoPi

`tcp_receive.py` 监听 TCP 9000，由 Supervisor 的 `phidata` 服务管理。接收的数据按接收日期追加到 `YYYY-MM-DD.txt`；连接断开后会释放资源。网页数据由独立的 9999 端口服务提供。
