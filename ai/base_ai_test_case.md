# 借助AI, 像管理代码一样管理测试用例

# 当前现状测试团队

## 当前问题

作为一个中小规模的测试团队，当前面临产线多，迭代速度快，多格式混用，无统一沉淀等问题。

| 问题                                  | 痛点                                                   |
| ------------------------------------- | ------------------------------------------------------ |
| 用例格式不统一（XMind/Excel/Word）    | **缺乏结构化标准**，导致无法自动化、难搜索、难维护     |
| 用例散落在本地/云效/钉钉文档          | **缺乏单一可信源**，协作成本高                         |
| 按“全量功能”写用例 → 工作量大、易过期 | **用例粒度与产品迭代节奏不匹配**，静态资产 vs 动态交付 |
| 按“版本”写用例 → 无传承、重复造轮子   | **缺乏用例的版本关联与复用机制**，知识随人员流动而流失 |

## 测试管理工具调研

基于目前测试团队对于测试管理的迫切需求，我们对测试管理工具进行了调研。

| 类型                 | 项目                                                                                             |
| -------------------- | ------------------------------------------------------------------------------------------------ |
| 项目管理平台         | *   云效：测试管理包含测试用例管理、测试计划、测试报告<br>    <br>*   JIRA集成Zephyr插件         |
| 专业测试用例管理平台 | *   TestRail：专业的Web端测试用例管理软件。                                                      |
| 开源用例平台         | *   Testlink: 基于PHP开发的用例管理平台。<br>    <br>*   AgileTC: 滴滴开源测试管理平台。         |
| 自研 or 二开         | *   公司自己重新开发一套用例管理平台。<br>    <br>*   基于一些开源的测试管理平台，进行二次开发。 |

## 互联网大厂是经验

那么，互联网大厂是如何做的呢？很多人误以为大厂都用 TestRail或自研重型平台，但真相是：

🟢 真相 1：大厂也在“分层管理”用例

*   **核心稳定功能**（如登录、支付）：用结构化系统（如 TestRail）维护**主干用例库**，强调复用；
    
*   **迭代新增功能**：用 **轻量方式（Confluence + 标签 / Git + Markdown）** 写**增量用例**，只覆盖变更点；
    
*   **自动化用例**：直接写在代码库（如 `tests/e2e/`），与 CI 绑定，不进用例管理系统。
    

> 📌 **关键理念**：**不是所有用例都值得“长期管理”**，区分“资产型用例”和“任务型用例”。

🟢 真相 2：用例与需求/代码强关联

*   阿里/腾讯/字节等：用例 ID 会写入 Jira/TAPD 的“测试计划”字段；
    
*   每次 MR（Merge Request）必须包含：
    
    *   新增/修改的用例（文本或链接）；
        
    *   自动化覆盖情况；
        
*   **用例变更 = 代码变更的一部分**，纳入 Code Review。
    

🟢 真相 3：格式统一 ≠ 工具统一，而是“结构统一”

*   允许用不同工具（脑图、表格、文档），但**必须导出为结构化数据**（如 JSON/YAML）存入中央仓库；
    
*   或者，**强制使用一种轻量格式**（如 Markdown + Front Matter），兼顾灵活性与可解析性。
    

🟢 真相 4：不追求“全量用例”，而是“有效覆盖”

*   大厂 QA 更关注：**本次变更影响了哪些路径？哪些用例需要回归？**
    
*   通过 **Impact Analysis（影响分析）** + **标签/模块映射** 快速筛选，而非维护百万级用例库。
    

> 💡 **结论**：大厂的成功不在工具多高级，而在**流程设计 + 工程习惯 + 轻量标准化**。

## 核心目标

针对当前测试团队，测试用例管理的核心目标是：

> **“主干用例资产化，增量用例任务化，所有用例结构化”**

1.  **主干用例资产化**
    

*   **主干用例**：指系统中长期稳定、高频使用、核心路径的功能用例。 比如：用户登录、下单支付、数据导出等。
    
*   **资产化**：把它们当作公司资产来对待——
    
    *   需要精心设计、持续维护、版本控制；
        
    *   要求结构清晰、可复用、可追溯；
        
    *   投入成本是值得的，因为会被反复使用。
        

1.  **增量用例任务化**
    

*   **增量用例**：指本次版本新增、临时调整、边缘场景的用例。 比如：v2.3 新增“支持微信扫码登录”、临时修复一个边界 bug。
    
*   **任务化**：把它们当作一次性任务来处理——
    
    *   只需覆盖当前需求，不追求长期维护；
        
    *   可以轻量编写（甚至用钉钉文档）；
        
    *   版本上线后，若无长期价值，可归档或丢弃。
        

1.  **所有用例结构化**
    

*   **无论主干还是增量**，最终呈现形式必须是结构化的（如 YAML/JSON），而非自由文本。
    
*   **目的**：
    
    *   便于搜索；
        
    *   便于对比（diff 清晰）；
        
    *   便于未来自动化（脚本可解析）；
        
    *   避免“**这个人写三段话，那个人画个图**”的混乱。
        

# 基于 Git + Markdown / YAML 的轻量级用例管理 

## 行业案例参考

| **公司/项目**                       | **实践方式**                                         | **效果**                            |
| ----------------------------------- | ---------------------------------------------------- | ----------------------------------- |
| **GitLab（部分 QA 团队）**          | 用例以 Markdown/YAML 形式随代码提交，通过 MR 评审    | 用例与需求/代码同步演进，变更可追溯 |
| **Zalando（欧洲电商）**             | 微服务验收场景用 YAML 定义，CI 自动校验              | 减少沟通成本，提升交付质量          |
| **某国内 SaaS 初创公司（50 人）**   | 全量功能用例用 YAML + Git 管理，自动生成 HTML 文档站 | 用例更新效率提升 3 倍，新人上手快   |
| **Apache APISIX / Kubernetes 社区** | E2E 场景以 YAML/Markdown 存于代码库                  | 开源贡献者可清晰理解验收标准        |

**共性结论**：技术驱动型中小团队通过“文本化 + 版本控制”实现高效、可持续的用例管理。

## 方案优点

| **维度**       | **优势说明**                                                                           |
| -------------- | -------------------------------------------------------------------------------------- |
| **沉淀可靠**   | 所有用例存于 Git，天然具备版本历史、分支对比、回滚能力，彻底解决“钉钉文档覆盖丢失”问题 |
| **协作高效**   | 通过 Merge Request（MR）机制，用例与需求/代码一同评审，避免信息孤岛                    |
| **结构统一**   | 强制字段（ID、步骤、预期结果等）确保用例质量，减少自由文本混乱                         |
| **零成本**     | 无需采购工具，复用现有 Git/GitLab/Github + VS Code 工具链                              |
| **未来可扩展** | 若后续推进自动化，YAML 可直接作为数据源驱动 pytest/Lounger 脚本。                      |
| **轻量灵活**   | 无流程负担，不强制复杂状态（如“设计中/执行中/阻塞”），聚焦用例本身。                   |

⚠️ **不适用场景**：重度依赖截图的 UI 验收、纯非技术背景手工测试团队。

## 用例编写规范

### 目录结构

```
testing-cases/
├── core/                       # 主干用例（长期维护）
│   ├── user-auth/              # 功能模块（小写+中划线）
│   │   ├── login.yaml          # 子功能用例集（一个文件 = 一个场景）
│   │   └── password-reset.yaml
│   └── order-core/
│       └── create-order.yaml
├── releases/                   # 增量用例（按需求/版本）
│   ├── webhook-v5/                   
│   │   ├── case.yaml                 
│   └── multilingual-trajectory/      
│       └── case.yaml
├── common/               # 公共步骤 或 数据
│   └── login.yaml
├── schema/               #（可选）YAML 校验规则
│   └── test-case.schema.json
├── docs/                 # （可选）补充说明文档
│   └── writing-guide.md
├── .gitignore            # 忽略临时文件
└── README.md             # 总索引 + 编写指南链接

```

### 文件命名

*   模块目录：`小写+中划线`，如 `user-auth`
    
*   用例文件：`动词-名词.yaml`，如 `login.yaml`, `cancel-order.yaml`
    

### YAML Schema定义

```
metadata:
  module: "用户中心"                # ★ 所属大模块
  feature: "手机号密码登录"         # ★ 当前文件聚焦功能
  owner: "Broni"                  # ★ 负责人（英文名）
  last_reviewed: "2026-01-16"     # 最后评审日期（YYYY-MM-DD）
  tags: [auth, mobile]            # 全局标签

test_cases:
  - id: "TC_LOGIN_001"            # ★ 唯一ID，格式 TC_<功能缩写>_<三位序号>
    title: "正确凭据登录成功"       # ★ 简洁动词开头
    description: "验证已注册用户..." # 补充说明（可选）
    priority: "P0"                # ★ P0/P1/P2
    type: "functional"            # ★ functional/ui/security/performance
    preconditions:                # 执行前提（可选）
      - "用户已完成注册"
    steps:                        # ★ 操作步骤（每步一句话）
      - "打开 App 首页"
      - "点击登录按钮"
    expected_results:             # ★ 预期结果（可多条）
      - "跳转至首页"
      - "顶部显示用户名"
    tags: [smoke, happy-path]     # 用例级标签
    auto: false                   # 是否计划自动化（默认 false）

```

**各字段详细说明**

| 字段名（YAML Key） | 是否必填 | 说明                                                                                                                                      | 示例 / 规范                                                          |
| ------------------ | -------- | ----------------------------------------------------------------------------------------------------------------------------------------- | -------------------------------------------------------------------- |
| `**metadata**`     | 是       | 用例文件的元信息区块，描述整体上下文                                                                                                      | —                                                                    |
| `module`           | ★ 必填   | 所属**大业务模块**，用于跨功能归类                                                                                                        | `"用户中心"`、`"Webhooks 管理"`                                      |
| `feature`          | ★ 必填   | 当前文件聚焦的**具体功能点**                                                                                                              | `"手机号密码登录"`、`"添加 Webhook 表单"`                            |
| `owner`            | ★ 必填   | 用例负责人（使用英文名，便于协作）                                                                                                        | `"Broni"`                                                            |
| `last_reviewed`    | 建议填   | 最后一次评审/更新日期，格式 `YYYY-MM-DD`                                                                                                  | `"2026-01-16"`                                                       |
| `tags`             | 可选     | **文件级全局标签**，用于分类、筛选或报告聚合                                                                                              | `[auth, mobile]`、<br>`[webhooks, form]`                             |
| `**test_cases**`   | 是       | 测试用例列表，每个元素为一个独立用例                                                                                                      | —                                                                    |
| `id`               | ★ 必填   | **全局唯一标识符**，命名规则：`TC_<功能缩写>_<三位序号>`                                                                                  | `"TC_LOGIN_001"`、`"TC_WEBHOOK_ADD_006"`                             |
| `title`            | ★ 必填   | 用例标题，**动词开头、简洁明确**，描述“做什么 + 预期结果”                                                                                 | `"正确凭据登录成功"`、`"Endpoint URL 格式校验失败"`                  |
| `description`      | 可选     | 补充说明，用于解释背景、复杂逻辑或特殊场景                                                                                                | `"验证已注册用户在输入正确手机号和密码后能成功登录并获取有效 token"` |
| `priority`         | ★ 必填   | 优先级：<br>\- `P0`：核心主流程、冒烟测试、阻塞性<br>\- `P1`：重要功能、边界/异常场景<br>\- `P2`：低频、UI 细节、优化项                   | `"P0"`                                                               |
| `type`             | ★ 必填   | 用例类型，用于分类执行策略：<br>\- `functional`（功能）<br>\- `ui`（界面交互）<br>\- `security`（安全）<br>\- `performance`（性能）<br>等 | `"functional"`                                                       |
| `preconditions`    | 可选     | 执行本用例前必须满足的**系统状态或前提条件**（列表形式）                                                                                  | `- "用户已完成注册"`<br>`- "存在至少一个 Webhook 配置"`              |
| `steps`            | ★ 必填   | **操作步骤**，每步一句话，按顺序执行，主语隐含为“用户”或“系统”                                                                            | `- "打开 App 首页"`<br>`- "点击登录按钮"`                            |
| `expected_results` | ★ 必填   | **预期结果**，与 steps 对应或整体验证点，可多条                                                                                           | `- "跳转至首页"`<br>`- "顶部显示用户名"`                             |
| `tags`             | 可选     | **用例级标签**，用于精细化筛选（如冒烟、正向路径、错误处理等）                                                                            | `[smoke, happy-path]`、`[error-handling]`、`[regression]`            |
| `auto`             | 可选     | 是否计划自动化：<br>\- `true`：已自动化或计划自动化<br>\- `false`（默认）：暂不自动化（如纯 UI 验证）                                     | `false`                                                              |

**Tags 标签说明**

| 标签             | 含义                       | 示例                                     |
| ---------------- | -------------------------- | ---------------------------------------- |
| `happy-path`     | 正常主流程，一切顺利       | 正确登录、成功提交表单                   |
| `error-handling` | 异常输入或错误场景处理     | 密码错误、空 URL 提交                    |
| `boundary`       | 边界值测试                 | 描述字段刚好 100 字 vs 101 字            |
| `regression`     | 回归测试，防止旧功能被破坏 | 列表页字段展示逻辑变更后，原有功能仍正常 |
| `security`       | 安全相关                   | 密码是否明文传输、token 是否泄露         |

## 用例格式检查

**测试用例不仅是测试团队的“执行清单”，更是跨角色（开发、产品、运维）的“质量契约”**。如果关键字段缺失（比如没有 `expected_results` 或 `priority`），会导致理解偏差、验收争议，甚至漏测。

而**格式校验**正是解决“人为偷懒/疏忽”的最有效工程手段。下面我们将提供一套**轻量、低成本、高落地性**的校验方案，确保 YAML 用例始终符合规范，且对非技术人员友好。

### 制定schema格式校验文件

在项目的跟目录下创建：`schema/test-case-schema.json`

```json
{
  "$schema": "http://json-schema.org/draft-07/schema#",
  "type": "object",
  "required": ["metadata", "test_cases"],
  "properties": {
    "metadata": {
      "type": "object",
      "required": ["module", "feature", "owner", "last_reviewed"],
      "properties": {
        "module": {
          "type": "string",
          "description": "所属大模块"
        },
        "feature": {
          "type": "string",
          "description": "当前文件聚焦功能"
        },
        "owner": {
          "type": "string",
          "description": "负责人（英文名）"
        },
        "last_reviewed": {
          "type": "string",
          "format": "date",
          "description": "最后评审日期（YYYY-MM-DD）"
        },
        "tags": {
          "type": "array",
          "items": {
            "type": "string"
          },
          "description": "全局标签"
        }
      },
      "additionalProperties": false
    },
    "test_cases": {
      "type": "array",
      "minItems": 1,
      "items": {
        "type": "object",
        "required": ["id", "title", "steps", "expected_results", "priority", "type"],
        "properties": {
          "id": {
            "type": "string",
            "pattern": "^TC_[A-Z0-9_]{3,}_[0-9]{3}$",
            "description": "全局唯一ID，格式 TC_<功能缩写>_<三位序号>"
          },
          "title": {
            "type": "string",
            "description": "简洁动词开头的标题"
          },
          "description": {
            "type": "string",
            "description": "补充说明（可选）"
          },
          "priority": {
            "type": "string",
            "enum": ["P0", "P1", "P2"],
            "description": "优先级"
          },
          "type": {
            "type": "string",
            "enum": ["functional", "ui", "security", "performance", "accessibility"],
            "description": "用例类型"
          },
          "preconditions": {
            "type": "array",
            "items": {
              "type": "string"
            },
            "description": "执行前提（可选）"
          },
          "steps": {
            "type": "array",
            "items": {
              "type": "string",
              "minLength": 1
            },
            "minItems": 1,
            "description": "操作步骤（每步一句话）"
          },
          "expected_results": {
            "type": "array",
            "items": {
              "type": "string",
              "minLength": 1
            },
            "minItems": 1,
            "description": "预期结果（可多条）"
          },
          "tags": {
            "type": "array",
            "items": {
              "type": "string"
            },
            "description": "用例级标签"
          },
          "auto": {
            "type": "boolean",
            "default": false,
            "description": "是否计划自动化（默认 false）"
          }
        },
        "additionalProperties": false
      }
    }
  },
  "additionalProperties": false
}
```

### VS Code 引用规则

*   **安装插件**：VS Code + [YAML 插件](https://marketplace.visualstudio.com/items?itemName=redhat.vscode-yaml)
    
    ![Clipboard_Screenshot_1769050797.png](https://alidocs.oss-cn-zhangjiakou.aliyuncs.com/res/r4mlQ5bBrRmxNlxo/img/d3f79a06-ca45-43e3-beb4-0553bfd16f0a.png)
    
*   **配置校验**：创建VS code 配置文件: `.vscode/settings.json`

```json
{
  "yaml.schemas": {
    "./schema/test-case-schema.json": [
      "core/**/*.yaml",
      "releases/**/*.yaml"
    ]
  }
}
```

*   **检验是否生效**：编写 YAML 格式的测试用例。
    

![Clipboard_Screenshot_1769051029.png](https://alidocs.oss-cn-zhangjiakou.aliyuncs.com/res/r4mlQ5bBrRmxNlxo/img/12535ba5-3caf-4c86-89ea-8f304cb34cda.png)

通过错误信息，可以清楚的看到缺少关键字段 “owner” 用例的拥有者。

## 基于AI 快速生成用例实践案例

## 需求分析

需求文档：略

> xx api涉及状态体系调整, 因此相应的webhook功能也需进行相关调整。

通过分析，本次需求包含前端部分的改动 和 后端服务架构的重构。其中，前端部分的改动评估之后比较适合按照这种模式编写测试用例。

## AI 编写测试用例

1.  这里采用 Qwen 大模型，将要webhook 的需求逐步的丢给Qwen 模型，让其生成测试用例。
    
    ![Clipboard_Screenshot_1769052330.png](https://alidocs.oss-cn-zhangjiakou.aliyuncs.com/res/r4mlQ5bBrRmxNlxo/img/d3b62102-5059-44c9-8f4a-6a507aeb3bd2.png)
    
2.  将生成的 YAMl 测试用例复制到测试文件中，参考需求文档逐条进行确认。
    
    ![Clipboard_Screenshot_1769052416.png](https://alidocs.oss-cn-zhangjiakou.aliyuncs.com/res/r4mlQ5bBrRmxNlxo/img/a01a4dd6-1e0d-4719-aee7-fc82be6e6065.png)
    
3.  重复前面两步，最终 完成webhook 的列表、添加、详情几个页面交互重构的测试用例。
    

## AI生成测试文档

每个需求下面创建一个`README.md`的测试文档，利用 VS code 集成 Copilot 完成测试用例的总计，并生成

```

...

## 🔗 相关链接

- 需求文档：https://alidocs.dingtalk.com/i/nodes/xxx
- Jira Issue：[TM-668](https://channelwill.atlassian.net/browse/TM-668)

```

## 引入skill

关于skill 我们同样进行了技术调研，完全可以在我们的测试用例编写的过程中引入SKILL.md，来提高用例编写的规范和精确性。

## 📄 `Skill.md`

```md
---
name: CWILL Test Case Generator
description: Generate structured, standardized YAML test cases for CWILL's lightweight test management system.
---

## Overview
This Skill helps testers and engineers at CWILL create consistent, review-ready YAML test cases that follow the team's official specification. It ensures all required fields (ID, steps, expected results, priority, etc.) are present and formatted correctly for Git-based test case management.

Use this Skill whenever you need to:
- Draft new functional test cases
- Convert manual test steps into YAML format
- Validate or fix existing YAML test cases
- Ensure compliance with CWILL's test case schema

## Input Format
Provide one of the following:
- A natural language description of a test scenario (e.g., "User logs in with wrong password")
- An incomplete or malformed YAML test case
- A list of test steps and expected outcomes

## Output Format
A complete, valid YAML snippet that can be directly saved into the `test-cases/` repository, including:
- Proper `meta` section
- Correctly formatted `test_cases` array
- Valid `id`, `title`, `steps`, `expected_results`, `priority`, and `tags`

## Example Usage

### Input:
> Write a P0 test case for successful user login with phone and password.

### Output:

``
meta:
  module: "用户中心"
  feature: "手机号密码登录"
  owner: "Tester"
  last_reviewed: "2026-01-30"
  tags: [auth, mobile]

test_cases:
  - id: "TC_LOGIN_001"
    title: "正确手机号和密码登录成功"
    description: "验证已注册用户使用正确凭据可正常登录"
    priority: "P0"
    type: "functional"
    preconditions:
      - "用户已完成手机号注册"
      - "网络连接正常"
    steps:
      - "打开 App 首页"
      - "点击「登录」按钮"
      - "输入已注册手机号"
      - "输入正确密码"
      - "点击「登录」按钮"
    expected_results:
      - "跳转至首页"
      - "顶部导航栏显示用户名"
      - "本地存储包含有效 token"
    tags: [smoke, happy-path]
    auto: false
``


## Rules & Constraints

*   Always use Chinese for field values (`module`, `title`, `steps`, etc.), but keep keys in English.
    
*   `id` must follow pattern: `TC_<UPPERCASE_MODULE>_<NNN>` (e.g., `TC_LOGIN_001`).
    
*   `priority` must be one of: `"P0"`, `"P1"`, `"P2"`.
    
*   `steps` and `expected_results` must be lists of clear, atomic, verifiable actions/outcomes.
    
*   Never include sensitive data, real URLs, or credentials.
    
*   If owner is unknown, use `"Tester"` as placeholder.
    

## When to Use This Skill

*   During test design phase
    
*   When onboarding new QA engineers
    
*   While preparing MRs for test case reviews
    
*   When converting legacy Excel/XMind test cases to YAML

```

## 下一步探索

## 协作流程

**【用例评审】像开发 Code Review 一样。**

1.  **新建/修改用例** → 在本地 Git 分支编辑 YAML；
    
2.  **提交 MR** → 关联对应需求（如 GitLab Issue）；
    
3.  **团队评审** → 至少 1 名测试同事 Review；
    
4.  **合并主干** → 用例正式生效；
    
5.  **定期清理** → 每季度检查 `last_reviewed`，过期用例标记或归档。
    

## 测试用例可视化

**【测试用例展示】想 Allure 报告一样，将YAML转 HTML 。**

*   **示例1：**
    

![Clipboard_Screenshot_1769054205.png](https://alidocs.oss-cn-zhangjiakou.aliyuncs.com/res/r4mlQ5bBrRmxNlxo/img/7c6e7733-a759-4eea-afdc-3c55fbbc1ae4.png)

## 总结

该方案已在公司成功落地。用 YAML 编写测试用例，并非接口测试的专利——功能测试用例同样适用。虽然表面看起来比 XMind 或测试用例平台复杂，但借助AI 生成，你几乎无需手动编写，唯一需要做的就是**理解需求并将理解传达给 AI**。

基于 Git 的版本控制让每次修改都有迹可循。我们内部要求：用例编写完成提交一次、评审&修改后提交一次、测试结束提交一次。通过对比第一版和最终上线版本的差异，可以直观反映测试工程师编写用例的质量成长。

这种模式的最大价值在于**帮助 AI 理解产品**。当产品的测试用例库足够丰富时，编写新需求就无需补充太多背景知识，AI 生成的用例也会更加精准、贴合产品特点。

将"版本用例"合并到"核心用例"虽然是体力活，但借助AI 让这个过程变得高效许多。

当前很多公司在测试平台上建设"测试用例生成"功能，本质上只是加入一些公司规则后调用大模型。而我们的方案更加贴合业务实际——**测试工程师与 AI 共建产品的用例库**，让测试资产在迭代中持续沉淀和进化。
