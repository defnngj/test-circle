# 盘点2022值得关注的测试开源项目

testerhome发起了2022年开源项目评选，最终入围的有17个开源项目。

其中一些被广泛熟知的项目，例如 Airtest、Httprunner、MeterSphere，也有一些新的值得关注的项目，例如sonic、lyrebird等。

## 项目汇总

|  项目   | 开源平台  |  类型 | star | commits | address|
|  ----  | ----  | ----  |  ----  |  ----  | ----  |
| OpenHarmony Wukong  | gitee | 工具  | 5  | 95  | https://gitee.com/openharmony/wukong |
| OpenHarmony arkXtest  | gitee | 框架  | 12  | 114  | https://gitee.com/openharmony/arkXtest |
| hrun4j  | github | 工具  | 142  | 183  | https://github.com/lematechvip/hrun4j |
| HttpRunner  | github | 工具  | 3.1k  | 2862 | https://github.com/httprunner/httprunner |
| Airtest  | github | 工具  | 6.2k  | 738  | https://github.com/AirtestProject/Airtest  |
| MeterSphere  | github | 平台  |7.7k  | 12022  | https://github.com/metersphere/metersphere |
| sonic  | github | 平台 |  1.2k | 344 | https://github.com/SonicCloudOrg/sonic-server  |
| react-agiletc-minder-editor  | github | 工具 | 12  | 16 | https://github.com/sxyy/react-agiletc-minder-editor |
| mobileperf  | github | 工具  | 490  | 23  | https://github.com/alibaba/mobileperf |
| garbevents  | github | 工具  | 85  | 121  | https://github.com/Pactortester/garbevents  |
| swaggerjmx  | github | 工具  | 76  | 63  | https://github.com/Pactortester/swaggerjmx  |
| 流马  | github | 平台 | 30  | 18  | https://github.com/Chras-fu/Liuma-engine |
| seldomQA  | github | 框架  | 609  | 813  | https://github.com/SeldomQA/seldom  |
| SoloPi  | github | 工具  | 4.7k  | 203  | https://github.com/alipay/SoloPi  |
| LuckyFrame | gitee | 平台  | 2.7k  | 454  | https://gitee.com/seagull1985/LuckyFrameWeb |
| Takin  | github | 平台  | 1.1k  | 145  | https://github.com/shulieTech/Takin |
| lyrebird  | github | 平台 | 912  | 399  | https://github.com/Meituan-Dianping/lyrebird  |

> 说明：
>
> 1. `star` 和 `commits` 会有变化，统计截止时间:`2022.6.9 23:00:00`。
>
> 2. 由多个子项目组成的项目，这里选取多star 的一个，例如 airtest、sonic、seldomQA都是由多个项目组成的。
> 
> 3. `commits` 是项目的提交次数，一方面可以拿来和`star` 对比，另一方面反应作者对项目的投入（大多开源项目都是靠爱发电）。

## 值得关注的项目

* OpenHarmony Wukong
* OpenHarmony arkXtest

这两个项目是针对`OpenHarmony` 操作系统的项目；`Wukong` 是一个Monkey 测试工具；`arkXtest`是测试框架；对于 `OpenHarmony` 操作系统来说，这个配套的工具非常重要。

* HttpRunner

无需多言，非常成熟的接口自动化测试工具，作者多年来对于项目的投入也是值得肯定的，随着，Htpprunner 4.0 的发布，在接口性能测试、多协议方面更进一步。

* hrun4j 

一个定位于java版本的Httprunner。

* Airtest

移动自动化测试工具，它所提供的图像识别功能为移动端UI定位带来了很大便利。虽然，他不是第一个提供图像识别的工具。


* MeterSphere

由专门的公司维护，使它在各种开源测试平台中脱颖而出，从`star` 和 `commits` 也可以看出项目的维护非常积极。比起 个人的开源平台从功能、易用性、成熟度上都有很大的优势。


* sonic

我愿称其为2022年最佳开源项目；远程云真机平台已经不算特别新鲜的技术了。但是，作者远程云真机平台做到了企业级的水平，甚至媲美各大收费的云真机平台，而且提供了更加丰富的一些功能。简直是普惠了许多中小企业。

* react-agiletc-minder-editor

`AgileTC`是一个开源的用例管理平台。`react-agiletc-minder-editor`可以看作是 AgileTC 的子项目，基于基于`React`的脑图编辑器。

* MobilePerf

基于python实现的Android性能测试工具。可是，已经两年没有维护了。emmm...


* garbevents

埋点数据测试工具。对于互联网产品来说，埋点测试非常重要，往往也会占用测试人员不少时间。他可以辅助测试人员更容易地进行埋点测试。

* swaggerjmx

可以将`Swagger/YApi`接口文档转成`JMeter`工具的脚本`.jmx`。


* 流马

一款简单易用、快速实现的自动化测试平台，将 API/WEB/APP自动化测试一套方案搞定。从平台提供的功能来看比较简单。用平台去做API/WEB/APP测试，理想很美好，真正用于生产环境做面临的挑战会很多。


* seldomQA

基于unittest的 Web UI/HTTP 自动化测试框架。seldom的目标是打造一套完整的自动化测试方案。

* 由几个子项目组成：
  * seldom
  基于unittest开发的测试框架。seldom 1.x 支持Web自动化测试， seldom 2.x 支持http接口测试，seldom 3.x 支持App测试（开发中...）。
  * XTestRunner
  基于unittest实现的高颜值HTML测试报告。
  * poium
  用于实现page objects模式的测试库。
  * seldom-platform （开发中...）
  基于seldom框架实现的测试平台，可以读取代码中的 文件、类、方法展示到web页面上。

> 介绍到自己的项目，不免要多说两句，哈哈！

* SoloPi

一个无线化、非侵入式的 Android 自动化工具，拥有录制回放、性能测试、一机多控三项主要功能。 这个项目2020年11月停止维护，直到2022年5月继续维护。

* LuckyFrame

一款免费开源的测试平台，最大的特点是全维度覆盖了接口自动化、WEB UI 自动化、APP 自动化。 从定位上和`流马`类似，功能上要更加丰富。

* Takin

Takin 是一套生产全链路压测的系统，可以在无业务代码侵入的情况下，嵌入到各个应用程序节点，实现生产环境的全链路性能测试，适用于复杂的微服务架构系统。 从实现方案上 和 `MeterSphere` 有些类似，都是基于JMeter实现的压测平台。可惜项目已经9个月没有维护了。

* Lyrebird

一个基于拦截以及模拟 HTTP/HTTPS 网络请求的面向移动应用的插件式测试平台。可以通过插件扩展能力，实现埋点自动测试、API 覆盖率统计、移动设备及 App 控制和信息记录、自定义检查脚本等一系列功能。 这是一个非常值得关注的项目。

## 总结

首先，所有的开源项目都是应该被鼓励的，做开源的同学知道需要极大的热情和时间精力投入。

其次，我个人觉得2022年最优秀的项目 `sonic`和 `lyredird`，这两个平台项目功能鲜明。而且，都在积极维护中。

最后，当然是要为 `seldomQA` 项目拉拉票了。`seldomQA` 在2022年得到了快速的发展，也正在被越来越多的公司使用（包括我们公司自己）， `seldomQA`有着自己的定位和发展规划，未来会带来更多好用的功能。








