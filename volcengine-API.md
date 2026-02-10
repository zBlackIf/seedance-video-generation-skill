# 获取API Key并配置

文档地址：https://www.volcengine.com/docs/82379/1541594?lang=zh

您调用方舟平台的模型之前，您需要 API Key 来进行鉴权。同时因为 API Key 信息较为敏感，泄露 API Key 会导致您的模型用量被其他人花费，造成一定的损失，因此我们会给出配置 API Key 进环境变量的方法，方便您合理安全地使用API Key。
`<span id="20bdcc68">`

## 获取 API Key

1. 打开并登录[API Key 管理](https://console.volcengine.com/ark/region:ark+cn-beijing/apiKey) 页面。
2. （可选）单击左上角 **账号全部资源** 下拉箭头，切换项目空间。
3. 单击 **创建 API Key** 按钮。
4. 在弹出框的 **名称** 文本框中确认/更改 API Key名称，单击创建。

您可以在[API Key 管理](https://console.volcengine.com/ark/region:ark+cn-beijing/apiKey) 页面的 **API Key 列表**中查看刚创建的API Key信息。
`<span id="f1908ee9">`

## 配置 API Key

推荐将 API Key 配置在环境变量中，而不是硬编码进代码中，避免 API Key 随代码泄露，导致配额被他人使用，产生额外花费。
配置方法见：[配置 API Key 到环境变量](/docs/82379/1399008#4b62407d)。
`<span id="64cf3cd0">`

## 使用说明

* API Key 配额：一个主账号下支持创建 50 个API Key，如需更多配额请提交[工单](https://console.volcengine.com/workorder/create?step=2&SubProductID=P00001166)申请。
* API Key 权限控制：API Key 创建于您当前所在项目，用于访问当前项目下的资源（即模型服务和应用）。您可为 API Key 额外限制可鉴权的 Model ID /自定义推理接入点，或可调用该 API Key 的 IP。
  * TIPS ：您切换项目空间创建 API Key，可限制 API Key 只用于指定项目空间下的模型服务的鉴权凭证。当您的账号是多人使用，可以通过此方法进行权限隔离。
  * 注意：API Key 仅支持访问指定项目下的接入点，不支持跨项目访问。当您跨项目迁移了接入点，则原 API Key 鉴权将失效。

# 安装及升级 SDK

文档地址：https://www.volcengine.com/docs/82379/1541595?lang=zh

方舟提供了 Python 、 Go 和 Java 的 SDK ，方便使用对应编程语言快速调用方舟的模型服务。
`<span id="2708d57e">`

# Python SDK

`<span id="f2baa8aa">`

## 前提条件

本地已经安装了Python ，且版本不低于 3.7。

> 可在终端中通过命令确认 Python 版本。如需安装，参考[Python安装教程](https://wiki.python.org/moin/BeginnersGuide/Download)，注意选择3.7及以上版本。

```Bash
python -V
```

`<span id="bb014324">`

## 安装 Python SDK

在终端中执行命令安装 Python SDK。

```Bash
pip install 'volcengine-python-sdk[ark]'
```

:::tip

* 如本地安装错误，可尝试下面方法：
  * [Windows系统安装SDK失败，ERROR: Failed building wheel for volcengine-python-sdk](/docs/82379/1359411#b74e8ad6)
  * 尝试使用下面命令 `pip install volcengine-python-sdk[ark]`
* 如需源码安装，可下载&解压对应版本 SDK 包，进入目录执行命令：`python setup.py install --user`。
  :::
  `<span id="d6b883b8">`

## 升级 Python SDK

如需使用方舟提供的最新能力，请升级 SDK 至最新版本。

```Bash
pip install 'volcengine-python-sdk[ark]' -U
```

`<span id="f116fb9f">`

# Go SDK

`<span id="0fa8c2bc">`

## 前提条件

检查 Go 版本，需 1.18 或以上。

```Bash
go version
```

如未安装或版本不满足，可访问 [Go 语言官方网站](https://golang.google.cn/dl/)下载并安装，请选择 1.18 或以上版本。
`<span id="ae8b42ab">`

## 安装 Go SDK

1. Go SDK 使用 go mod 管理，可运行以下命令初始化 go mod。`<your-project-name>` 替换为项目名称。

```Bash
# 如在文件夹 ark-demo 下打开终端窗口，运行命令go mod init ark-demo
go mod init <your-project-name>
```

2. 在本地初始化 go mod 后，运行以下命令安装最新版 SDK。

```Bash
go get -u github.com/volcengine/volcengine-go-sdk 
```

:::tip
如需安装特定版本的SDK，可使用命令：
`go get -u github.com/volcengine/volcengine-go-sdk@<VERSION>`
其中 `<VERSION>`替换为版本号。SDK 版本可查询： https://github.com/volcengine/volcengine-go-sdk/releases
:::

3. 在代码中引入 SDK 使用。

```Go
import "github.com/volcengine/volcengine-go-sdk/service/arkruntime"
```

4. 更新依赖后，使用命令整理依赖。

```Bash
go mod tidy
```

`<span id="f0739bb0">`

## 升级 Go SDK

步骤与安装 Go SDK相同，可参考[安装 Go SDK](/docs/82379/1541595#ae8b42ab)，第1，2步升级至最新/指定版本SDK。

* 升级至最新版本

```Bash
go get -u github.com/volcengine/volcengine-go-sdk
```

* 升级至指定版本

```Bash
go get -u github.com/volcengine/volcengine-go-sdk@<VERSION>
```

`<span id="e7ae2925">`

# Java SDK

`<span id="41f31f3c">`

## 适用范围

本 SDK 仅适用于 Java 服务端开发，暂不支持 Android 平台。若需在 Android 平台使用相关功能，需由客户自行开发适配方案。
`<span id="e3518e9f">`

## 前提条件

1. 检查并安装 Java 版本，Java 版本需 1.8 或以上。

```Bash
java -version
```

如未安装 Java 或者版本不满足要求，可访问 [Oracle 官方网站](https://www.java.com/en/download/help/index_installing.html)下载并安装适合操作系统的 Java 版本。请确保选择 1.8 或以上版本。
`<span id="ae8db863">`

## 安装 Java SDK

火山方舟 Java SDK 支持通过 Maven 安装、通过 Gradle 安装两种方式。
`<span id="db12484d">`

### 通过 Maven 安装

在 `pom.xml` 文件中进行如下配置，完整配置可参考[Maven Central](https://central.sonatype.com/artifact/com.volcengine/volcengine-java-sdk-ark-runtime)：

```XML
...
<dependency>
  <groupId>com.volcengine</groupId>
  <artifactId>volcengine-java-sdk-ark-runtime</artifactId>
  <version>LATEST</version>
</dependency>
...
```

`<span id="4858e8c3">`

### 通过 Gradle 安装

在 `build.gradle` 文件中进行如下配置，在 `dependencies` 中添加依赖。

```Plain
implementation 'com.volcengine:volcengine-java-sdk-ark-runtime:LATEST'
```

`<span id="4ab4182d">`

## 升级 Java SDK

:::tip
获取 SDK 版本信息，替换'LATEST' 为指定/最新版本号。SDK版本号可查询：[https://github.com/volcengine/volcengine-java-sdk/releases](https://github.com/volcengine/volcengine-java-sdk/releases)
:::
同安装 Java SDK，指定需升级的版本号即可。
`<span id="6f32c555">`

# 第三方SDK

火山方舟模型调用 API 与 OpenAI API 协议兼容，可使用兼容 OpenAI API 协议的多语言社区 SDK 调用火山方舟大模型或应用。可很方便地迁移模型服务至方舟平台以及 Doubao 大模型。具体使用方法请参考[兼容 OpenAI SDK](/docs/82379/1330626)。
`<span id="4b8511f6">`

# 相关文档

[SDK 常见使用示例](/docs/82379/1544136)：包含SDK的常见用法。

# Base URL及鉴权

文档地址：https://www.volcengine.com/docs/82379/1298459?lang=zh

火山方舟API分为模型调用的API（数据面 API），及管理推理接入点等管控相关的管控面 API。他们支持的鉴权方式有所不同，下面介绍方舟API的鉴权方式。
`<span id="28e0db57">`

# 概念解释

* **数据面 API**：是直接面向**业务数据传输、实时交互、用户请求处理**的接口，聚焦于 “实际业务数据的流转与处理”，是系统对外提供核心服务能力的载体。请求大模型服务的 Chat API、Responses API 均为数据面 API。
* **管控面 API**：用于**系统资源管理、配置控制和状态监控**的接口。它专注于管理和调度数据面及系统资源，是保障系统稳定运行的“控制中枢”。例如，在方舟中用于管理 API Key、基础模型等接口，均属于管控面 API。
* **Base URL**：是构建完整 API 请求 URL 的 “基础模板”，包含**协议（如 http/https）、host（主机域名或 IP）、端口（可选）和基础路径（可选）** ，是所有具体接口路径的 “公共前缀”。你可以根据Base URL 加接口/版本等参数拼接出完整接口 URL ，典型结构：`[协议]://[host]/[基础路径（可选）]`

`<span id="b77a3928">`

# Base URL

各接口类型对应的 Base URL。

* 数据面 API：https://ark.cn\-beijing.volces.com/api/v3
* 管控面 API：https://ark.cn\-beijing.volcengineapi.com/

`<span id="0fed4817">`

# 数据面 API 鉴权

支持两种鉴权方式，API Key 鉴权（简单方便），与 Access Key 鉴权（传统云上资源权限管控，可以分资源组云产品等维度管理，面向企业精细化管理）。
`<span id="60db1ed6">`

## API Key 签名鉴权

`<span id="6011c5a5">`

### 前提条件

:::tip
方舟平台的新用户？获取 API Key 及 开通模型等准备工作，请参见 [快速入门](/docs/82379/1399008)。
:::
`<span id="d44d13a6">`

### 签名构造

在 HTTP 请求 header 中按如下方式添加 `Authorization` header:

```Shell
Authorization: Bearer $ARK_API_KEY
```

示例如下

```Shell
curl https://ark.cn-beijing.volces.com/api/v3/chat/completions \
  -H "Content-Type: application/json" \
  -H "Authorization: Bearer $ARK_API_KEY" \
  -d '{
    "model": "doubao-seed-1-6-251015",
    "messages": [
        {
            "role": "system",
            "content": "You are a helpful assistant."
        },
        {
            "role": "user",
            "content": "Hello!"
        }
    ]
  }'
```

* 可按需替换 Model ID。查询 Model ID见 [模型列表](/docs/82379/1330310)。

`<span id="21bff83b">`

## Access Key 签名鉴权

`<span id="3ad1c414">`

### 前提条件

你已获取到Access Key。如需创建/查看Access Key，请参见[API访问密钥管理](https://www.volcengine.com/docs/6257/64983)。

> 由于主账号的Access Key拥有较大权限，建议你创建IAM用户并授予方舟等权限，然后使用IAM用户的 Access Key 来进行操作，具体请参见[使用 IAM 管理权限](/docs/82379/1263493)。

`<span id="d03b2bb1">`

### 使用示例

见 [使用Access Key鉴权](/docs/82379/1544136#fa44b913)。

> 通过Access Key 鉴权，model 字段 需配置为 Endpoint ID。

`<span id="bdd329d5">`

# 管控面 API 鉴权

管控面的API，如管理API Key、管理推理接入点等接口。
`<span id="50f355e8">`

## Access Key 签名鉴权

获取Access Key。如需创建/查看Access Key，请参见[API访问密钥管理](https://www.volcengine.com/docs/6257/64983)。
`<span id="c04e9b57">`

### 方法：使用示例/说明（简单，推荐）

参见[SDK 接入指南](https://api.volcengine.com/api-sdk/view?serviceCode=ark&version=2024-01-01&language=Java)。
`<span id="101d062c">`

### 方法：自行实现签名（实现成本高，不推荐）

1. 使用 Access Key 构造签名。具体方法请参见[签名方法](https://www.volcengine.com/docs/6369/67269)。

> 签名用到的方舟相关字段信息：
>
> * Service：`ark`
> * Region：`cn-beijing`

2. 使用cURL发起请求，请求示例如下：

```Shell
curl -X POST \
  'https://ark.cn-beijing.volcengineapi.com/?Action=ListEndpoints&Version=2024-01-01' \
  -H 'Authorization: HMAC-SHA256 Credential=AKL**/20240710/cn-beijing/ark/request, SignedHeaders=host;x-content-sha256;x-date, Signature=a7a****' \
  -H 'Content-Type: application/json' \
  -H 'Host: ark.cn-beijing.volcengineapi.com' \
  -H 'X-Content-Sha256: 44***' \
  -H 'X-Date: 20240710T042925Z' \
  -d '{}'
```

# 创建视频生成任务API

文档地址：https://www.volcengine.com/docs/82379/1520757?lang=zh

`POST https://ark.cn-beijing.volces.com/api/v3/contents/generations/tasks`   [运行](https://api.volcengine.com/api-explorer/?action=CreateContentsGenerationsTasks&data=%7B%7D&groupName=%E8%A7%86%E9%A2%91%E7%94%9F%E6%88%90API&query=%7B%7D&serviceCode=ark&version=2024-01-01)
本文介绍创建视频生成任务 API 的输入输出参数，供您使用接口时查阅字段含义。模型会依据传入的图片及文本信息生成视频，待生成完成后，您可以按条件查询任务并获取生成的视频。

**不同模型支持的视频生成能力简介**

* **Seedance 1.5 pro==^new^==** ** ** **==^有声视频^==** **(自定义是否包含音频)**
  * 图生视频\-首尾帧，根据您输入的++首帧图片+尾帧图片+文本提示词（可选）+参数（可选）++ 生成目标视频。
  * 图生视频\-首帧，根据您输入的++首帧图片+文本提示词（可选）+参数（可选）++ 生成目标视频。
  * 文生视频，根据您输入的++文本提示词+参数（可选）++ 生成目标视频。
* **Seedance 1.0 pro**
  * 图生视频\-首尾帧，根据您输入的++首帧图片+尾帧图片+文本提示词（可选）+参数（可选）++ 生成目标视频。
  * 图生视频\-首帧，根据您输入的++首帧图片+文本提示词（可选）+参数（可选）++ 生成目标视频。
  * 文生视频，根据您输入的++文本提示词+参数（可选）++ 生成目标视频。
* **Seedance 1.0 pro fast**
  * 图生视频\-首帧，根据您输入的++首帧图片+文本提示词（可选）+参数（可选）++ 生成目标视频。
  * 文生视频，根据您输入的++文本提示词+参数（可选）++ 生成目标视频。
* **Seedance 1.0 lite**
  * **doubao\-seedance\-1\-0\-lite\-t2v：** 文生视频，根据您输入的++文本提示词+参数（可选）++ 生成目标视频。
  * **doubao\-seedance\-1\-0\-lite\-i2v：**
    * 图生视频\-参考图，根据您输入的**++参考图片（1\-4张）++ **  +++文本提示词（可选）+ 参数（可选）++ 生成目标视频。
    * 图生视频\-首尾帧，根据您输入的++首帧图片+尾帧图片+文本提示词（可选）+参数（可选）++ 生成目标视频。
    * 图生视频\-首帧，根据您输入的++首帧图片+文本提示词（可选）+参数（可选）++ 生成目标视频。

Tips：一键展开折叠，快速检索内容
打开页面右上角开关，**ctrl ** + **f** 可检索页面内所有内容。
`<span>`![图片](https://portal.volccdn.com/obj/volcfe/cloud-universal-doc/upload_cae7ddb0e1977b68b353f17897b8574c.png)

```mixin-react
return (<Tabs>
<Tabs.TabPane title="在线调试" key="cKmdyIjR"><RenderMd content={`<APILink link="https://api.volcengine.com/api-explorer/?action=CreateContentsGenerationsTasks&data=%7B%7D&groupName=%E8%A7%86%E9%A2%91%E7%94%9F%E6%88%90API&query=%7B%7D&serviceCode=ark&version=2024-01-01" description="API Explorer 您可以通过 API Explorer 在线发起调用，无需关注签名生成过程，快速获取调用结果。"></APILink>
`}></RenderMd></Tabs.TabPane>
<Tabs.TabPane title="鉴权说明" key="vRJT6oJZ"><RenderMd content={`本接口仅支持 API Key 鉴权，请在 [获取 API Key](https://console.volcengine.com/ark/region:ark+cn-beijing/apiKey) 页面，获取长效 API Key。
`}></RenderMd></Tabs.TabPane>
<Tabs.TabPane title="快速入口" key="MlbBRTbjal"><RenderMd content={` [ ](#)[体验中心](https://console.volcengine.com/ark/region:ark+cn-beijing/experience/vision)       <span>![图片](https://portal.volccdn.com/obj/volcfe/cloud-universal-doc/upload_2abecd05ca2779567c6d32f0ddc7874d.png =20x) </span>[模型列表](https://www.volcengine.com/docs/82379/1330310?lang=zh#2705b333)       <span>![图片](https://portal.volccdn.com/obj/volcfe/cloud-universal-doc/upload_a5fdd3028d35cc512a10bd71b982b6eb.png =20x) </span>[模型计费](https://www.volcengine.com/docs/82379/1544106?redirect=1&lang=zh#02affcb8)       <span>![图片](https://portal.volccdn.com/obj/volcfe/cloud-universal-doc/upload_afbcf38bdec05c05089d5de5c3fd8fc8.png =20x) </span>[API Key](https://console.volcengine.com/ark/region:ark+cn-beijing/apiKey?apikey=%7B%7D)
 <span>![图片](https://portal.volccdn.com/obj/volcfe/cloud-universal-doc/upload_57d0bca8e0d122ab1191b40101b5df75.png =20x) </span>[调用教程](https://www.volcengine.com/docs/82379/1366799)       <span>![图片](https://portal.volccdn.com/obj/volcfe/cloud-universal-doc/upload_f45b5cd5863d1eed3bc3c81b9af54407.png =20x) </span>[接口文档](https://www.volcengine.com/docs/82379/1520758)       <span>![图片](https://portal.volccdn.com/obj/volcfe/cloud-universal-doc/upload_1609c71a747f84df24be1e6421ce58f0.png =20x) </span>[常见问题](https://www.volcengine.com/docs/82379/1359411)       <span>![图片](https://portal.volccdn.com/obj/volcfe/cloud-universal-doc/upload_bef4bc3de3535ee19d0c5d6c37b0ffdd.png =20x) </span>[开通模型](https://console.volcengine.com/ark/region:ark+cn-beijing/openManagement?LLM=%7B%7D&OpenTokenDrawer=false)
`}></RenderMd></Tabs.TabPane></Tabs>);
```

---

`<span id="RxN8G2nH">`

## 请求参数

> 跳转 [响应参数](#y2hhTyHB)

`<span id="BJ5XLFqM">`

### 请求体

---

**model** `string` %%require%%
您需要调用的模型的 ID （Model ID），[开通模型服务](https://console.volcengine.com/ark/region:ark+cn-beijing/openManagement?LLM=%7B%7D&OpenTokenDrawer=false)，并[查询 Model ID](https://www.volcengine.com/docs/82379/1330310) 。
您也可通过 Endpoint ID 来调用模型，获得限流、计费类型（前付费/后付费）、运行状态查询、监控、安全等高级能力，可参考[获取 Endpoint ID](https://www.volcengine.com/docs/82379/1099522)。

---

**content** `object[]` %%require%%
输入给模型，生成视频的信息，支持文本、图片和视频（样片，Draft 视频）格式。支持以下几种组合：

* 文本
* 文本+图片
* 视频：其中视频指已成功生成的样片视频，模型可基于样片生成高质量正式视频。

信息类型

---

**文本信息** `object`
输入给模型生成视频的内容，文本内容部分。

属性

---

content.**type ** `string` %%require%%
输入内容的类型，此处应为 `text`。

---

content.**text ** `string` %%require%%
输入给模型的文本内容，描述期望生成的视频，包括：

* **文本提示词（必填）** ：支持中英文。建议不超过500字。字数过多信息容易分散，模型可能因此忽略细节，只关注重点，造成视频缺失部分元素。提示词的更多使用技巧请参见 [Seedance 提示词指南](https://www.volcengine.com/docs/82379/1587797)。
* **参数（选填）** ：在文本提示词后追加\-\-[parameters]，控制视频输出的规格，详情见 **模型文本命令(选填** **）** 。

---

**图片信息** `object`
输入给模型生成视频的内容，图片信息部分。

属性

---

content.**type ** `string` %%require%%
输入内容的类型，此处应为 `image_url`。支持图片URL或图片 Base64 编码。

---

content.**image_url ** `object` %%require%%
输入给模型的图片对象。

属性

---

content.image_url.**url ** `string` %%require%%
图片信息，可以是图片URL或图片 Base64 编码。

* 图片URL：请确保图片URL可被访问。
* Base64编码：请遵循此格式 `data:image/<图片格式>;base64,<Base64编码>`，注意 `<图片格式>` 需小写，如 `data:image/png;base64,{base64_image}`。

:::tip
传入图片需要满足以下条件：

* 图片格式：jpeg、png、webp、bmp、tiff、gif。其中，Seedance 1.5 pro 新增支持 heic 和 heif。
* 宽高比（宽/高）： (0.4, 2.5)
* 宽高长度（px）：(300, 6000)
* 大小：小于 30 MB

:::

---

content.**role ** `string` `条件必填`
图片的位置或用途。
:::warning
首帧图生视频、首尾帧图生视频、参考图生视频为 3 种互斥的场景，不支持混用。

:::
图生视频\-首帧

* **支持模型：** 所有图生视频模型
* **字段role取值：** 需要传入1个image_url对象，且字段role可不填，或字段role为：first_frame

图生视频\-首尾帧

* **支持模型：** Seedance 1.5 pro、Seedance 1.0 pro、Seedance 1.0 lite i2v
* **字段role取值：** 需要传入2个image_url对象，且字段role必填。
  * 首帧图片对应的字段role为：first_frame
  * 尾帧图片对应的字段role为：last_frame

:::tip
传入的首尾帧图片可相同。首尾帧图片的宽高比不一致时，以首帧图片为主，尾帧图片会自动裁剪适配。

:::

图生视频\-参考图

* **支持模型：** Seedance 1.0 lite i2v
* **字段role取值：** 需要传入1～4个image_url对象，且字段role必填。
  * 每张参考图片对应的字段role均为：reference_image

:::tip
参考图生视频功能的文本提示词，可以用自然语言指定多张图片的组合。但若想有更好的指令遵循效果，**推荐使用“[图1]xxx，[图2]xxx”的方式来指定图片**。
示例1：戴着眼镜穿着蓝色T恤的男生和柯基小狗，坐在草坪上，3D卡通风格
示例2：[图1]戴着眼镜穿着蓝色T恤的男生和[图2]的柯基小狗，坐在[图3]的草坪上，3D卡通风格

:::

---

**样片信息==^new^==** ** **  `object`
基于样片任务 ID，生成正式视频。仅 Seedance 1.5 pro 支持该功能。[阅读](https://www.volcengine.com/docs/82379/1366799?lang=zh#5acd28c8)[文档](https://www.volcengine.com/docs/82379/1366799?lang=zh#5acd28c8) 获取 draft 功能的使用教程和注意事项。

属性

---

content.**type ** `string` %%require%%
输入内容的类型，此处应为 `draft_task`。

---

content.**draft_task** ** ** `object` %%require%%
输入给模型的样片任务。

属性

---

content.draft_task.**id ** `string` %%require%%
样片任务 ID。平台将自动复用 Draft 视频使用的用户输入（**model、** content.**text、** content.**image_url、generate_audio、seed、ratio、duration、** **camera_fixed ** ），生成正式视频。其余参数支持指定，不指定将使用本模型的默认值。
使用分为两步：Step1: 调用本接口生成 Draft 视频。Step2: 如果确认 Draft 视频符合预期，可基于 Step1 返回的 Draft 视频任务 ID，调用本接口生成最终视频。[阅读文档](https://www.volcengine.com/docs/82379/1366799?lang=zh#5acd28c8) 获取详细教程。

---

**callback_url** `string`
填写本次生成任务结果的回调通知地址。当视频生成任务有状态变化时，方舟将向此地址推送 POST 请求。
回调请求内容结构与[查询任务API](https://www.volcengine.com/docs/82379/1521309)的返回体一致。
回调返回的 status 包括以下状态：

* queued：排队中。
* running：任务运行中。
* succeeded： 任务成功。（如发送失败，即5秒内没有接收到成功发送的信息，回调三次）
* failed：任务失败。（如发送失败，即5秒内没有接收到成功发送的信息，回调三次）
* expired：任务超时，即任务处于**运行中或排队中**状态超过过期时间。可通过 **execution_expires_after ** 字段设置过期时间。

---

**return_last_frame** `boolean` `默认值 false`

* true：返回生成视频的尾帧图像。设置为 `true` 后，可通过 [查询视频生成任务接口](https://www.volcengine.com/docs/82379/1521309) 获取视频的尾帧图像。尾帧图像的格式为 png，宽高像素值与生成的视频保持一致，无水印。
  使用该参数可实现生成多个连续视频：以上一个生成视频的尾帧作为下一个视频任务的首帧，快速生成多个连续视频，调用示例详见 [教程](https://www.volcengine.com/docs/82379/1366799?lang=zh#141cf7fa)。
* false：不返回生成视频的尾帧图像。

---

**service_tier** `string` `默认值 default`

> 不支持修改已提交任务的服务等级

指定处理本次请求的服务等级类型，枚举值：

* default：在线推理模式，RPM 和并发数配额较低（详见 [模型列表](https://www.volcengine.com/docs/82379/1330310?lang=zh#2705b333)），适合对推理时效性要求较高的场景。
* flex：离线推理模式，TPD 配额更高（详见 [模型列表](https://www.volcengine.com/docs/82379/1330310?lang=zh#2705b333)），价格为在线推理的 50%， 适合对推理时延要求不高的场景。

---

**execution_expires_after** ** ** `integer` `默认值 172800`
任务超时阈值。指定任务提交后的过期时间（单位：秒），从 **created at** 时间戳开始计算。默认值 172800 秒，即 48 小时。取值范围：[3600，259200]。
不论使用哪种 **service_tier**，都建议根据业务场景设置合适的超时时间。超过该时间后任务会被自动终止，并标记为 `expired`状态。

---

**generate_audio==^new^==** ** ** `boolean` `默认值 true`

> 仅 Seedance 1.5 pro 支持

控制生成的视频是否包含与画面同步的声音。

* true：模型输出的视频包含同步音频。Seedance 1.5 pro 能够基于文本提示词与视觉内容，自动生成与之匹配的人声、音效及背景音乐。建议将对话部分置于双引号内，以优化音频生成效果。例如：男人叫住女人说：“你记住，以后不可以用手指指月亮。”
* false：模型输出的视频为无声视频。

---

**draft==^new^==** ** ** `boolean` `默认值 false`

> 仅 Seedance 1.5 pro 支持

控制是否开启样片模式。[阅读文档](https://www.volcengine.com/docs/82379/1366799?lang=zh#5acd28c8) 获取使用教程和注意事项。

* true：开启样片模式，生成一段预览视频，快速验证场景结构、镜头调度、主体动作与 prompt 意图是否符合预期。消耗 token 数较正常视频更少，使用成本更低。
* false：关闭样片模式，正常生成一段视频。

:::tip
开启样片模式后，将使用 480p 分辨率生成 Draft 视频（使用其他分辨率会报错），不支持返回尾帧功能，不支持离线推理功能。

:::
---

:::warning 部分参数升级说明

* **对于 resolution、ratio、duration、frames、seed、camera_fixed、watermark 参数，平台升级了参数传入方式，示例如下。Seedance 1.0\-1.5 系列模型依然兼容支持旧方式。**
* 不同模型，可能对应支持不同的参数与取值，详见 [输出视频格式](https://www.volcengine.com/docs/82379/1366799?lang=zh#9fe4cce0)。当输入的参数或取值不符合所选的模型时，该参数将被忽略或触发报错：
  * 新方式：在 request body 中直接传入参数。此方式为**强校验，** 若参数填写错误，模型会返回错误提示。
  * 旧方式：在文本提示词后追加 \-\-[parameters]。此方式为**弱校验，** 若参数填写错误，模型将自动使用默认值且不会报错。

:::
**新方式（推荐）：在 request body 中直接传入参数**

```JSON
... 
   // Specify the aspect ratio of the generated video as 16:9, duration as 5 seconds, resolution as 720p, seed as 11, and include a watermark. The camera is not fixed. 
    "model": "doubao-seedance-1-5-pro-251215", 
    "content": [ 
        { 
            "type": "text", 
            "text": "小猫对着镜头打哈欠" 
        } 
    ], 
    // All parameters must be written in full; abbreviations are not supported 
    "resolution": "720p", 
    "ratio":"16:9", 
    "duration": 5, 
    // "frames": 29, Either duration or frames is required 
    "seed": 11, 
    "camera_fixed": false, 
    "watermark": true 
... 
```

**旧方式：在文本提示词后追加 \-\-[parameters]**

```JSON
... 
   // Specify the aspect ratio of the generated video as 16:9, duration as 5 seconds, resolution as 720p, seed as 11, and include a watermark. The camera is not fixed. 
    "model": "doubao-seedance-1-5-pro-251215", 
    "content": [ 
        { 
            "type": "text", 
            "text": "小猫对着镜头打哈欠 --rs 720p --rt 16:9 --dur 5 --seed 11 --cf false --wm true"
            // "text": "小猫对着镜头打哈欠 --resolution 720p --ratio 16:9 --duration 5 --seed 11 --camerafixed false --watermark true"
        } 
    ]
... 
```

---

**resolution **  `string`

> Seedance 1.5 pro、Seedance 1.0 lite 默认值：`720p`
> Seedance 1.0 pro & pro\-fast 默认值：`1080p`

视频分辨率，枚举值：

* 480p
* 720p
* 1080p：参考图场景不支持

---

**ratio ** `string`

> 文生视频：默认值 `16:9`（ Seedance 1.5 Pro 默认值为 `adaptive`）
> 图生视频：默认值 `adaptive`（参考图生视频场景默认值为 `16:9`）

生成视频的宽高比例。不同宽高比对应的宽高像素值见下方表格。

* 16:9
* 4:3
* 1:1
* 3:4
* 9:16
* 21:9
* adaptive：根据输入自动选择最合适的宽高比（详见下文说明）

:::warning **adaptive ** 适配规则
当配置 **ratio** 为 `adaptive` 时，模型会根据生成场景自动适配宽高比；实际生成的视频宽高比可通过 [查询视频生成任务 API](https://www.volcengine.com/docs/82379/1521309?lang=zh) 返回的 **ratio** 字段获取。

* 文生视频场景：根据输入的提示词，自动选择最合适的宽高比（仅 Seedance 1.5 Pro 支持）。
* 图生视频场景：
  * 参考图生视频：不支持配置 **ratio** 为 `adaptive`。
  * 首帧 / 首尾帧生视频：根据上传的首帧图片比例，自动选择最合适的宽高比。

:::
**不同宽高比对应的宽高像素值**
Note：图生视频，选择的宽高比与您上传的图片宽高比不一致时，方舟会对您的图片进行裁剪，裁剪时会居中裁剪，详细规则见 [图片裁剪规则](https://www.volcengine.com/docs/82379/1366799?lang=zh#f76aafc8)。

|分辨率 |宽高比|宽高像素值|宽高像素值|\

|                             |      | Seedance 1.0 系列 | Seedance 1.5 pro |
| --------------------------- | ---- | ----------------- | ---------------- |
| 480p                        | 16:9 | 864×480          | 864×496         |
| ^^                          | 4:3  | 736×544          | 752×560         |
| ^^                          | 1:1  | 640×640          | 640×640         |
| ^^                          | 3:4  | 544×736          | 560×752         |
| ^^                          | 9:16 | 480×864          | 496×864         |
| ^^                          | 21:9 | 960×416          | 992×432         |
| 720p                        | 16:9 | 1248×704         | 1280×720        |
| ^^                          | 4:3  | 1120×832         | 1112×834        |
| ^^                          | 1:1  | 960×960          | 960×960         |
| ^^                          | 3:4  | 832×1120         | 834×1112        |
| ^^                          | 9:16 | 704×1248         | 720×1280        |
| ^^                          | 21:9 | 1504×640         | 1470×630        |
| 1080p                       | 16:9 | 1920×1088        | 1920×1080       |
| > 1.0 lite 参考图场景不支持 |      |                   |                  |
| ^^                          | 4:3  | 1664×1248        | 1664×1248       |
| ^^                          | 1:1  | 1440×1440        | 1440×1440       |
| ^^                          | 3:4  | 1248×1664        | 1248×1664       |
| ^^                          | 9:16 | 1088×1920        | 1080×1920       |
| ^^                          | 21:9 | 2176×928         | 2206×946        |

---

**duration** `integer` `默认值 5`

> duration 和 frames 二选一即可，frames 的优先级高于 duration。如果您希望生成整数秒的视频，建议指定 duration。

生成视频时长，单位：秒。支持 2~12 秒。
:::warning
Seedance 1.5 pro 支持两种配置方法

* 指定具体时长：支持 [4,12] 范围内的任一整数。
* 不指定具体生成时长：设置为 `-1`，表示由模型在 [4,12] 范围内自主选择合适的视频长度（整数秒）。实际生成视频的时长可通过 [查询视频生成任务 API](https://www.volcengine.com/docs/82379/1521309?lang=zh) 返回的 **duration** 字段获取。注意视频时长与计费相关，请谨慎设置。

:::
---

**frames** `integer`

> Seedance 1.5 pro 暂不支持
> duration 和 frames 二选一即可，frames 的优先级高于 duration。如果您希望生成小数秒的视频，建议指定 frames。

生成视频的帧数。通过指定帧数，可以灵活控制生成视频的长度，生成小数秒的视频。
由于 frames 的取值限制，仅能支持有限小数秒，您需要根据公式推算最接近的帧数。

* 计算公式：帧数 = 时长 × 帧率（24）。
* 取值范围：支持 [29, 289] 区间内所有满足 `25 + 4n` 格式的整数值，其中 n 为正整数。

例如：假设需要生成 2.4 秒的视频，帧数=2.4×24=57.6。由于 frames 不支持 57.6，此时您只能选择一个最接近的值。根据 25+4n 计算出最接近的帧数为 57，实际生成的视频为 57/24=2.375 秒。

---

**seed** `integer` `默认值 -1`
种子整数，用于控制生成内容的随机性。
取值范围：[\-1, 2^32\-1]之间的整数。
:::warning

* 相同的请求下，模型收到不同的seed值，如：不指定seed值或令seed取值为\-1（会使用随机数替代）、或手动变更seed值，将生成不同的结果。
* 相同的请求下，模型收到相同的seed值，会生成类似的结果，但不保证完全一致。

:::
---

**camera_fixed** `boolean` `默认值 false`

> 参考图场景不支持

是否固定摄像头。枚举值：

* true：固定摄像头。平台会在用户提示词中追加固定摄像头，实际效果不保证。
* false：不固定摄像头。

---

**watermark** `boolean` `默认值 false`
生成视频是否包含水印。枚举值：

* false：不含水印。
* true：含有水印。

---

`<span id="y2hhTyHB">`

## 响应参数

> 跳转 [请求参数](#RxN8G2nH)

**id ** `string`
视频生成任务 ID 。仅保存 7 天（从 **created at** 时间戳开始计算），超时后将自动清除。

* 设置 `"draft": true`，为 Draft 视频任务 ID。
* 设置 `"draft": false`，为正常视频任务 ID。

创建视频生成任务为异步接口，获取 ID 后，需要通过 [查询视频生成任务 API](https://www.volcengine.com/docs/82379/1521309) 来查询视频生成任务的状态。任务成功后，会输出生成视频的 `video_url`。

# 查询视频生成任务API

文档地址：https://www.volcengine.com/docs/82379/1521309?lang=zh

`GET https://ark.cn-beijing.volces.com/api/v3/contents/generations/tasks/{id}`  [运行](https://api.volcengine.com/api-explorer/?action=GetContentsGenerationsTask&data=%7B%22id%22%3A%22cgt-20250331175019-68d9t%22%7D&groupName=%E8%A7%86%E9%A2%91%E7%94%9F%E6%88%90API&query=%7B%7D&serviceCode=ark&version=2024-01-01)
查询视频生成任务的状态。
:::tip
仅支持查询最近 7 天的历史数据。时间计算统一采用UTC时间戳，返回的7天历史数据范围以用户实际发起查询请求的时刻为基准（精确到秒），时间戳区间为 [T\-7天, T)。

:::

```mixin-react
return (<Tabs>
<Tabs.TabPane title="快速入口" key="fq9yXaKY"><RenderMd content={` [ ](#)[体验中心](https://console.volcengine.com/ark/region:ark+cn-beijing/experience/vision)       <span>![图片](https://portal.volccdn.com/obj/volcfe/cloud-universal-doc/upload_2abecd05ca2779567c6d32f0ddc7874d.png =20x) </span>[模型列表](https://www.volcengine.com/docs/82379/1330310)       <span>![图片](https://portal.volccdn.com/obj/volcfe/cloud-universal-doc/upload_a5fdd3028d35cc512a10bd71b982b6eb.png =20x) </span>[模型计费](https://www.volcengine.com/docs/82379/1099320#%E8%A7%86%E9%A2%91%E7%94%9F%E6%88%90%E6%A8%A1%E5%9E%8B)       <span>![图片](https://portal.volccdn.com/obj/volcfe/cloud-universal-doc/upload_afbcf38bdec05c05089d5de5c3fd8fc8.png =20x) </span>[API Key](https://console.volcengine.com/ark/region:ark+cn-beijing/apiKey?apikey=%7B%7D)
 <span>![图片](https://portal.volccdn.com/obj/volcfe/cloud-universal-doc/upload_57d0bca8e0d122ab1191b40101b5df75.png =20x) </span>[调用教程](https://www.volcengine.com/docs/82379/1366799)       <span>![图片](https://portal.volccdn.com/obj/volcfe/cloud-universal-doc/upload_f45b5cd5863d1eed3bc3c81b9af54407.png =20x) </span>[接口文档](https://www.volcengine.com/docs/82379/1521309)       <span>![图片](https://portal.volccdn.com/obj/volcfe/cloud-universal-doc/upload_1609c71a747f84df24be1e6421ce58f0.png =20x) </span>[常见问题](https://www.volcengine.com/docs/82379/1359411)       <span>![图片](https://portal.volccdn.com/obj/volcfe/cloud-universal-doc/upload_bef4bc3de3535ee19d0c5d6c37b0ffdd.png =20x) </span>[开通模型](https://console.volcengine.com/ark/region:ark+cn-beijing/openManagement?LLM=%7B%7D&OpenTokenDrawer=false)
`}></RenderMd></Tabs.TabPane>
<Tabs.TabPane title="鉴权说明" key="3vCxpwty"><RenderMd content={`本接口支持 API Key 鉴权，详见[鉴权认证方式](https://www.volcengine.com/docs/82379/1298459)。
`}></RenderMd></Tabs.TabPane></Tabs>);
```

---

`<span id="RxN8G2nH">`

## 请求参数

> 跳转 [响应参数](#7mi8G8RI)

---

**id** `string` %%require%%
您需要查询的视频生成任务的 ID 。
:::tip
上面参数为Query String Parameters，在URL String中传入。

:::
---

&nbsp;
`<span id="7mi8G8RI">`

## 响应参数

> 跳转 [请求参数](#RxN8G2nH)

---

**id ** `string`
视频生成任务 ID 。

---

**model** `string`
任务使用的模型名称和版本，`模型名称-版本`。

---

**status** `string`
任务状态，以及相关的信息：

* `queued`：排队中。
* `running`：任务运行中。
* `cancelled`：取消任务，取消状态24h自动删除（只支持排队中状态的任务被取消）。
* `succeeded`： 任务成功。
* `failed`：任务失败。
* `expired`：任务超时。

---

**error** `object / null`
错误提示信息，任务成功返回 `null`，任务失败时返回错误数据，错误信息具体参见 [错误处理](https://www.volcengine.com/docs/82379/1299023#%E6%96%B9%E8%88%9F%E9%94%99%E8%AF%AF%E7%A0%81)。

属性

---

error.**code** `string`
错误码。

---

error.**message** `string`
错误提示信息。

---

**created_at** `integer`
任务创建时间的 Unix 时间戳（秒）。

---

**updated_at** `integer`
任务当前状态更新时间的 Unix 时间戳（秒）。

---

**content** `object`
视频生成任务的输出内容。

属性

---

content.**video_url** `string`
生成视频的 URL，格式为 mp4。为保障信息安全，生成的视频会在24小时后被清理，请及时转存。
content.**last_frame_url ** `string`
视频的尾帧图像 URL。有效期为 24小时，请及时转存。
说明：[创建视频生成任务](https://www.volcengine.com/docs/82379/1520757) 时设置 `"return_last_frame": true` 时，会返回该参数。

---

**seed** `integer`
本次请求使用的种子整数值。

---

**resolution **  `string`
生成视频的分辨率。

---

**ratio ** `string`
生成视频的宽高比。

---

**duration** `integer`
生成视频的时长，单位：秒。
说明：**duration 和 frames 参数只会返回一个**。[创建视频生成任务](https://www.volcengine.com/docs/82379/1520757) 时未指定 frames，会返回 duration。

---

**frames** `integer`
生成视频的帧数。
说明：**duration 和 frames 参数只会返回一个**。[创建视频生成任务](https://www.volcengine.com/docs/82379/1520757) 时指定了 frames，会返回 frames。

---

**framespersecond**  `integer`
生成视频的帧率。

---

**generate_audio==^new^==** `boolean`
生成的视频是否包含与画面同步的声音。仅 Seedance 1.5 pro 会返回该参数。

* `true`：模型输出的视频包含同步音频。
* `false`：模型输出的视频为无声视频。

---

**draft==^new^==** `boolean`
生成的视频是否为 Draft 视频。仅 Seedance 1.5 pro 会返回该参数。

* `true`：表示当前输出为 Draft 视频。
* `false`：表示当前输出为正常视频。

---

**draft_task_id==^new^==** ** ** `string`
Draft 视频任务 ID。基于 Draft 视频生成正式视频时，会返回该参数。

---

**service_tier  ** `string`
实际处理任务使用的服务等级。

---

**execution_expires_after** ** ** `integer`
任务超时阈值，单位：秒。

---

**usage** `object`
本次请求的 token 用量。

属性

---

usage.**completion_tokens** `integer`
模型输出视频花费的 token 数量。

---

usage.**total_tokens** `integer`
本次请求消耗的总 token 数量。视频生成模型不统计输入 token，输入 token 为 0，故 **total_tokens**=**completion_tokens**。

# 查询视频生成任务列表

文档地址：https://www.volcengine.com/docs/82379/1521675?lang=zh

`GET https://ark.cn-beijing.volces.com/api/v3/contents/generations/tasks?page_num={page_num}&page_size={page_size}&filter.status={filter.status}&filter.task_ids={filter.task_ids}&filter.model={filter.model}`  [运行](https://api.volcengine.com/api-explorer/?action=ListContentsGenerationsTasks&data=%7B%7D&groupName=%E8%A7%86%E9%A2%91%E7%94%9F%E6%88%90API&query=%7B%7D&serviceCode=ark&version=2024-01-01)
当您要查询符合条件的任务，您可以传入条件筛选参数，返回符合要求的任务。
:::tip
仅支持查询最近 7 天的历史数据。时间计算统一采用UTC时间戳，返回的7天历史数据范围以用户实际发起批量查询请求的时刻为基准（精确到秒），时间戳区间为 [T\-7天, T)。

:::

```mixin-react
return (<Tabs>
<Tabs.TabPane title="快速入口" key="opV4RT2k"><RenderMd content={` [ ](#)[体验中心](https://console.volcengine.com/ark/region:ark+cn-beijing/experience/vision)       <span>![图片](https://portal.volccdn.com/obj/volcfe/cloud-universal-doc/upload_2abecd05ca2779567c6d32f0ddc7874d.png =20x) </span>[模型列表](https://www.volcengine.com/docs/82379/1330310)       <span>![图片](https://portal.volccdn.com/obj/volcfe/cloud-universal-doc/upload_a5fdd3028d35cc512a10bd71b982b6eb.png =20x) </span>[模型计费](https://www.volcengine.com/docs/82379/1099320#%E8%A7%86%E9%A2%91%E7%94%9F%E6%88%90%E6%A8%A1%E5%9E%8B)       <span>![图片](https://portal.volccdn.com/obj/volcfe/cloud-universal-doc/upload_afbcf38bdec05c05089d5de5c3fd8fc8.png =20x) </span>[API Key](https://console.volcengine.com/ark/region:ark+cn-beijing/apiKey?apikey=%7B%7D)
 <span>![图片](https://portal.volccdn.com/obj/volcfe/cloud-universal-doc/upload_57d0bca8e0d122ab1191b40101b5df75.png =20x) </span>[调用教程](https://www.volcengine.com/docs/82379/1366799)       <span>![图片](https://portal.volccdn.com/obj/volcfe/cloud-universal-doc/upload_f45b5cd5863d1eed3bc3c81b9af54407.png =20x) </span>[接口文档](https://www.volcengine.com/docs/82379/1521675)       <span>![图片](https://portal.volccdn.com/obj/volcfe/cloud-universal-doc/upload_1609c71a747f84df24be1e6421ce58f0.png =20x) </span>[常见问题](https://www.volcengine.com/docs/82379/1359411)       <span>![图片](https://portal.volccdn.com/obj/volcfe/cloud-universal-doc/upload_bef4bc3de3535ee19d0c5d6c37b0ffdd.png =20x) </span>[开通模型](https://console.volcengine.com/ark/region:ark+cn-beijing/openManagement?LLM=%7B%7D&OpenTokenDrawer=false)
`}></RenderMd></Tabs.TabPane>
<Tabs.TabPane title="鉴权说明" key="CPeW5vNl"><RenderMd content={`本接口支持 API Key 鉴权，详见[鉴权认证方式](https://www.volcengine.com/docs/82379/1298459)。
`}></RenderMd></Tabs.TabPane></Tabs>);
```

---

`<span id="RxN8G2nH">`

## 请求参数

> 跳转 [响应参数](#7mi8G8RI)

:::tip
下面参数为Query String Parameters，在URL String中传入。

:::
---

**page_num** `integer / null`
取值范围：[1, 500]
返回结果的页码。

---

**page_size ** `integer / null`
取值范围：[1, 500]
返回结果的每页的结果数量。

---

**filter.status ** `string / null`
过滤参数，查询某个任务状态。

* `queued`：排队中的任务。
* `running`：运行中任务。
* `cancelled`：取消的任务。
* `succeeded`： 成功的任务。
* `failed`：失败的任务。

---

**filter.task_ids ** `string[] / null`
视频生成任务 ID，精确搜索，支持同时搜索多个任务 ID。多个任务 ID 之间通过 `&`连接。示例：`filter.task_ids=id1&filter.task_ids=id2`。

---

**filter.model ** `string / null`
与返回参数不同，该字段为任务使用的推理接入点 ID，精确搜索。

---

**filter.service_tier ** `string / null` `默认值 default`
 处理任务使用的服务等级。

* `default`：在线推理模式
* `flex`：离线推理模式

`<span id="7mi8G8RI">`

## 响应参数

> 跳转 [请求参数](#RxN8G2nH)

---

**items ** `object[]`
查询到的视频生成任务列表。

属性

---

items.**id ** `string`
视频生成任务 ID 。

---

items.**model** `string`
任务使用的模型名称和版本，`模型名称-版本`。

---

items.**status** `string`
任务状态，以及相关的信息：

* `queued`：排队中。
* `running`：任务运行中。
* `cancelled`：取消任务（只支持排队中状态的任务被取消）。
* `succeeded`： 任务成功。
* `failed`：任务失败。
* `expired`：任务超时。

---

items.**error** `object / null`
错误提示信息，任务成功返回 `null`，任务失败时返回错误数据，错误信息具体参见 [错误处理](https://www.volcengine.com/docs/82379/1393047#653d2c40)。

属性

---

error.**code** `string`
错误码。

---

error.**message** `string`
错误提示信息。

---

items.**created_at** `integer`
任务创建时间的 Unix 时间戳（秒）。

---

items.**updated_at** `integer`
任务当前状态更新时间的 Unix 时间戳（秒）。

---

items.**content** `object`
当视频生成任务完成，会输出该字段，包含生成视频下载的 URL。

属性

---

content.**video_url** `string`
生成视频的URL。为保障信息安全，生成的视频会在24小时后被清理，请及时转存。

---

content.**last_frame_url ** `string`
视频的尾帧图像 URL。有效期为 24小时，请及时转存。
说明：[创建视频生成任务](https://www.volcengine.com/docs/82379/1520757) 时设置 `"return_last_frame": true` 时，会返回参数。

---

items.**seed** `integer`
本次请求使用的种子整数值。

---

items.**resolution **  `string`
生成视频的分辨率。

---

items.**ratio ** `string`
生成视频的宽高比。

---

items.**duration** `integer`
生成视频的时长，单位：秒。
说明：**duration 和 frames 参数只会返回一个**。[创建视频生成任务](https://www.volcengine.com/docs/82379/1520757) 时未指定 frames，会返回 duration。

---

items.**frames ** `integer`
生成视频的帧数。
说明：**duration 和 frames 参数只会返回一个**。[创建视频生成任务](https://www.volcengine.com/docs/82379/1520757) 时指定了 frames，会返回 frames。

---

items.**framespersecond**  `integer`
生成视频的帧率。

---

items.**generate_audio==^new^==** `boolean`
生成的视频是否包含与画面同步的声音。仅 Seedance 1.5 pro 会返回该参数。

* `true`：模型输出的视频包含同步音频。
* `false`：模型输出的视频为无声视频。

---

items.**draft==^new^==** `boolean`
生成的视频是否为 Draft 视频。仅 Seedance 1.5 pro 会返回该参数。

* `true`：表示当前输出为 Draft 视频。
* `false`：表示当前输出为正常视频。

---

items.**draft_task_id==^new^==**`string`
Draft 视频任务 ID。基于 Draft 视频生成正式视频时，会返回该参数。

---

items.**service_tier ** **==^new^==**`string`
实际处理任务使用的服务等级。

---

items.**execution_expires_after==^new^==** ** ** `integer`
任务超时阈值，单位：秒。

---

items.**usage** `object`
本次请求的 token 用量。

属性

---

usage.**completion_tokens** `integer`
模型输出视频花费的 token 数量。

---

usage.**total_tokens** `integer`
本次请求消耗的总 token 数量。视频生成模型不统计输入 token，输入 token 为 0，故 **total_tokens**=**completion_tokens**。

---

**total ** `integer`
符合筛选条件的任务数量。

# 取消或删除视频生成任务

文档地址：https://www.volcengine.com/docs/82379/1521720?lang=zh

`DELETE https://ark.cn-beijing.volces.com/api/v3/contents/generations/tasks/{id}`  [运行](https://api.volcengine.com/api-explorer/?action=DeleteContentsGenerationsTasks&data=%7B%22id%22%3A%22cgt-20250331175019-68d9t%22%7D&groupName=%E8%A7%86%E9%A2%91%E7%94%9F%E6%88%90API&query=%7B%7D&serviceCode=ark&version=2024-01-01)
取消排队中的视频生成任务，或者删除视频生成任务记录。

```mixin-react
return (<Tabs>
<Tabs.TabPane title="快速入口" key="vI631gwS"><RenderMd content={` [ ](#)[体验中心](https://console.volcengine.com/ark/region:ark+cn-beijing/experience/vision)       <span>![图片](https://portal.volccdn.com/obj/volcfe/cloud-universal-doc/upload_2abecd05ca2779567c6d32f0ddc7874d.png =20x) </span>[模型列表](https://www.volcengine.com/docs/82379/1330310)       <span>![图片](https://portal.volccdn.com/obj/volcfe/cloud-universal-doc/upload_a5fdd3028d35cc512a10bd71b982b6eb.png =20x) </span>[模型计费](https://www.volcengine.com/docs/82379/1099320#%E8%A7%86%E9%A2%91%E7%94%9F%E6%88%90%E6%A8%A1%E5%9E%8B)       <span>![图片](https://portal.volccdn.com/obj/volcfe/cloud-universal-doc/upload_afbcf38bdec05c05089d5de5c3fd8fc8.png =20x) </span>[API Key](https://console.volcengine.com/ark/region:ark+cn-beijing/apiKey?apikey=%7B%7D)
 <span>![图片](https://portal.volccdn.com/obj/volcfe/cloud-universal-doc/upload_57d0bca8e0d122ab1191b40101b5df75.png =20x) </span>[调用教程](https://www.volcengine.com/docs/82379/1366799)       <span>![图片](https://portal.volccdn.com/obj/volcfe/cloud-universal-doc/upload_f45b5cd5863d1eed3bc3c81b9af54407.png =20x) </span>[接口文档](https://www.volcengine.com/docs/82379/1521675)       <span>![图片](https://portal.volccdn.com/obj/volcfe/cloud-universal-doc/upload_1609c71a747f84df24be1e6421ce58f0.png =20x) </span>[常见问题](https://www.volcengine.com/docs/82379/1359411)       <span>![图片](https://portal.volccdn.com/obj/volcfe/cloud-universal-doc/upload_bef4bc3de3535ee19d0c5d6c37b0ffdd.png =20x) </span>[开通模型](https://console.volcengine.com/ark/region:ark+cn-beijing/openManagement?LLM=%7B%7D&OpenTokenDrawer=false)
`}></RenderMd></Tabs.TabPane>
<Tabs.TabPane title="鉴权说明" key="L8aMwmZD"><RenderMd content={`本接口支持 API Key 鉴权，详见[鉴权认证方式](https://www.volcengine.com/docs/82379/1298459)。
`}></RenderMd></Tabs.TabPane></Tabs>);
```

---

`<span id="RxN8G2nH">`

## 请求参数

> 跳转 [响应参数](#7mi8G8RI)

:::tip
下面参数为Query String Parameters，在URL String中传入。

:::
---

**id** `string` %%require%%
需要取消或者删除的视频生成任务。
任务状态不同，调用 `DELETE`接口，执行的操作有所不同，具体说明如下：

| 当前任务状态 | 是否支持DELETE操作 | 操作含义                                  | DELETE操作后任务状态 |
| ------------ | ------------------ | ----------------------------------------- | -------------------- |
| queued       | 是                 | 任务取消排队，任务状态被变更为cancelled。 | cancelled            |
| running      | 否                 | \-                                        | \-                   |
| succeeded    | 是                 | 删除视频生成任务记录，后续将不支持查询。  | \-                   |
| failed       | 是                 | 删除视频生成任务记录，后续将不支持查询。  | \-                   |
| cancelled    | 否                 | \-                                        | \-                   |
| expired      | 是                 | 删除视频生成任务记录，后续将不支持查询。  | \-                   |

&nbsp;

---

&nbsp;
`<span id="7mi8G8RI">`

## 响应参数

> 跳转 [请求参数](#RxN8G2nH)

本接口无返回参数。
