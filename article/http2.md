
# HTTP2.0

HTTP: 全称超文本传输协议(HyperText Transfer Protocol)


## HTTP 简史

* HTTP1.0

伴随着计算机网络和浏览器的诞生，HTTP1.0也随之而来，HTTP是建立在TCP协议之上，处于计算机网络中的应用层，所以HTTP协议的瓶颈及其优化技巧都是基于TCP协议本身的特性，例如：TCP建立连接的3次握手和4次挥手以及每次建立连接带来的RTT延迟时间。

* HTTP1.1

HTTP1.1和HTTP1.0的主要区别。

* 缓存处理：HTTP1.1则引入了更多的缓存控制策略例如Entity tag，If-Unmodified-Since, If-Match, If-None-Match等更多可供选择的缓存头来控制缓存策略。
* 带宽优化及网络连接的使用：HTTP1.1则在请求头引入了range头域，它允许只请求资源的某个部分，即返回码是206（Partial Content），这样就方便了开发者自由的选择以便于充分利用带宽和连接。
* 错误通知的管理： 在HTTP1.1中新增了24个错误状态响应码。
* Host头处理：HTTP1.1的请求消息和响应消息都应支持Host头域，且请求消息中如果没有Host头域会报告一个错误
* 长连接，HTTP 1.1支持长连接（PersistentConnection）和请求的流水线（Pipelining）处理，在一个TCP连接上可以传送多个HTTP请求和响应，减少了建立和关闭连接的消耗和延迟，在HTTP1.1中默认开启Connection： keep-alive，一定程度上弥补了HTTP1.0每次请求都要创建连接的缺点。

* HTTPS

HTTPS和HTTP的主要区别。

* HTTPS协议需要到CA申请证书，一般免费证书很少，需要交费。
* HTTP协议运行在TCP之上，所有传输的内容都是明文，HTTPS运行在SSL/TLS之上，SSL/TLS运行在TCP之上，所有传输的内容都经过加密的。
* HTTP和HTTPS使用的是完全不同的连接方式，用的端口也不一样，前者是80，后者是443。
* HTTPS可以有效的防止运营商劫持，解决了防劫持的一个大问题。

* HTTP2.0

HTTP2.0的新特性

* 新的二进制格式（Binary Format），HTTP1.x的解析是基于文本。基于文本协议的格式解析存在天然缺陷，文本的表现形式有多样性，要做到健壮性考虑的场景必然很多，二进制则不同，只认0和1的组合。基于这种考虑HTTP2.0的协议解析决定采用二进制格式，实现方便且健壮。

* 多路复用（MultiPlexing），即连接共享，即每一个request都是是用作连接共享机制的。一个request对应一个id，这样一个连接上可以有多个request，每个连接的request可以随机的混杂在一起，接收方可以根据request的 id将request再归属到各自不同的服务端请求里面。

* header压缩，如上文中所言，对前面提到过HTTP1.x的header带有大量信息，而且每次都要重复发送，HTTP2.0使用encoder来减少需要传输的header大小，通讯双方各自cache一份header fields表，既避免了重复header的传输，又减小了需要传输的大小。

* 服务端推送（server push），同SPDY一样，HTTP2.0也具有server push功能。目前，有大多数网站已经启用HTTP2.0，例如YouTuBe，淘宝网等网站。

https://www.zhihu.com/question/34074946

## HTTP2.0应用

