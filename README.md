# 中考陪跑系统

![中考陪跑系统 GitHub 预览图](docs/github-social-preview.svg)

一个改装店老板用两个月 AI 从零搭的、给自己儿子用的中考陪跑系统。

这不是一个卖题库的项目，也不是一个开源社区项目。它只是把一个真实家庭里的中考冲刺方法，整理成可公开查看、可跑样例、可复盘机制的证据物料。

做这个系统的人是 Chous，一个改装店老板。使用对象是自己的儿子。做它的原因很简单：中考复习不能只靠感觉，必须知道今天练了什么、错在哪里、明天为什么继续练这一类题。系统在中考冲刺的两个月窗口里持续使用和迭代，保留了 EXP 驱动、证据闭环、三 agent 分工、红灯机制、量化出题和错题回溯这些核心机制。

目前私有工作区已整理过的材料口径是：9 科、84 份考卷、1300+ 道题、5700+ 张图，覆盖 2013-2025 年。公开仓库不包含这些私有题库、真题原文、教辅内容、学生姓名、成绩或错题记录。

## 系统图示

下面三张图只展示系统结构和报告形态；公开截图已人工处理后发布。

![林老板 AI 中考陪跑系统结构图](docs/images/system-architecture.png)

![Obsidian 工作区结构展示（已脱敏）](docs/images/obsidian-workspace-redacted.png)

![微信端开跑监督报告（已人工处理）](docs/images/mobile-report-redacted.png)

## 机制设计

### EXP 驱动

孩子每天不是只看到“做题”，而是看到自己完成了多少可计量任务。每道题会转成 EXP，难度越高、复盘越完整，EXP 越高。这样做的目的不是游戏化炫技，而是把复习进度从“今天好像学了”变成“今天确实推进了多少”。

### 证据闭环

每个练习任务都要能回答三个问题：

- 这题从哪里来？
- 为什么今天要练？
- 做错以后回流到哪个知识点？

如果题目没有来源、答案没复核、图片/表格缺失，系统就不能把它当成正式练习。

### 三 agent 分工

- 出题 agent：根据弱点、时间和题型优先级生成当天练习。
- 复核 agent：检查题目来源、答案、图片、表格和红灯风险。
- 教练 agent：把错题归因到知识点，安排后续回练。

三者分开，是为了避免一个模型既出题又自我证明正确。

### 红灯机制

遇到以下情况直接停：

- 题目来源不清楚
- 图片、表格、连线信息缺失
- 答案没有复核
- 出现真实学生姓名、成绩、联系方式
- 出现不能公开的题库、教辅、真题原文

红灯不是报错提示，而是防止系统把错误内容继续喂给孩子。

### 量化出题策略

出题不是平均撒题。系统会优先考虑：

- 近期高频题型
- 当前薄弱知识点
- 能在当天完成的题量
- 是否需要图表、连线、实验或阅读材料
- 上一次错题是否需要回练

目标是让每一天的练习都能解释清楚，不靠拍脑袋。

### 错题回溯

错题不会只记录“错了”。它要回到知识点、题型、来源和下一次练习任务。真正有价值的不是错题本本身，而是错题能不能驱动下一轮训练。

## 技术栈与运行

公开版只保留最小可运行样例：

- Python 3.10+
- JSON 题目 schema
- 无第三方依赖
- 自编样例题，不包含任何真实题库内容

运行步骤：

```bash
git clone https://github.com/JSD-SpeedUP/zhongkao-peipao.git
cd zhongkao-peipao
cp config.example.json config.local.json
python scripts/run_sample.py examples/sample-questions.json --config config.local.json
```

Windows PowerShell 可以用：

```powershell
Copy-Item config.example.json config.local.json
python scripts/run_sample.py examples/sample-questions.json --config config.local.json
```

正常输出会看到每道样例题的状态、EXP 和 `evidence_loop: PASS`。

## 仓库内容

- `docs/schema.md`：公开题库 schema，覆盖选择、填空、简答、表格、图片、连线题。
- `examples/sample-questions.json`：1-2 道自编样例题，只用于跑通系统。
- `scripts/run_sample.py`：最小样例 runner，演示 EXP、证据检查和红灯机制。
- `config.example.json`：三 agent 分工、EXP 和红灯配置示例。

## 作者

<img src="docs/avatar.svg" width="96" height="96" alt="Chous avatar">

**Chous（林老板）**

- B 站：加速度SpeedUP https://space.bilibili.com/12170556
- 抖音：林哥教你做改装，抖音号 1155107743
- 小红书：林哥玩改装，账号 26801384926
- 知乎：https://www.zhihu.com/people/sha-mo-wu-yin-56

这个仓库是方法论样本，不是题库产品。真实题库、孩子数据和使用效果记录不在首次公开版本中发布。
