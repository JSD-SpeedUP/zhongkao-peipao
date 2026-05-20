# 题库 Schema

这个 schema 的目标是够用：能表达中考陪跑系统里的普通题、表格题、图片题、连线题，并能支撑后续错题回溯。它不是为了做一个完美通用题库标准。

## 公共字段

| 字段 | 类型 | 必填 | 说明 |
|---|---|---:|---|
| `id` | string | 是 | 题目唯一 ID。公开样例可用 `sample-*`。 |
| `type` | string | 是 | `choice`、`fill_blank`、`short_answer`、`table`、`image`、`matching`。 |
| `subject` | string | 是 | 学科，例如 `math`、`english`、`physics`、`chinese`。 |
| `stem` | string | 是 | 完整题干。不能只写“见图片”。 |
| `options` | array | 否 | 选择题选项。 |
| `tables` | array | 否 | 表格题字段，可放 markdown table。 |
| `images` | array | 否 | 图片题字段，放相对路径和说明。 |
| `matching` | object | 否 | 连线题字段，包含左右两组和配对关系。 |
| `answer` | string/object/array | 是 | 答案。 |
| `explanation` | string | 否 | 解析或复盘说明。 |
| `tags` | array | 是 | 知识点标签，用于错题回溯。 |
| `difficulty` | number | 是 | 难度，建议 1-5。 |
| `source` | object | 是 | 来源信息。公开仓库只允许自编或公共领域样例。 |
| `evidence` | object | 是 | 证据闭环字段。 |

## 来源字段

```json
{
  "kind": "self_made",
  "title": "Public sample question",
  "license": "MIT",
  "note": "Created only to demonstrate the workflow."
}
```

`kind` 建议值：

- `self_made`：自编题。
- `public_domain`：公共领域材料。
- `private_bank`：私有题库。不能进入公开仓库。
- `licensed_material`：受版权限制材料。不能进入公开仓库。

## 证据字段

```json
{
  "source_trace": "examples/sample-questions.json",
  "public_safe": true,
  "review_status": "reviewed"
}
```

`public_safe` 必须明确为 `true` 才能进入公开样例。真实学生姓名、成绩、联系方式、错题记录、买来的题库内容都不能公开。

## 选择题

```json
{
  "id": "sample-choice-001",
  "type": "choice",
  "subject": "math",
  "stem": "Which number is even?",
  "options": [
    {"label": "A", "text": "3"},
    {"label": "B", "text": "4"},
    {"label": "C", "text": "5"},
    {"label": "D", "text": "7"}
  ],
  "answer": "B",
  "explanation": "4 can be divided by 2.",
  "tags": ["number-sense"],
  "difficulty": 1,
  "source": {"kind": "self_made", "title": "Public sample question", "license": "MIT"},
  "evidence": {"source_trace": "docs/schema.md", "public_safe": true}
}
```

## 填空题

```json
{
  "id": "sample-fill-001",
  "type": "fill_blank",
  "subject": "english",
  "stem": "Fill in the blank: I ____ a book every night.",
  "answer": "read",
  "explanation": "The sentence describes a regular habit.",
  "tags": ["present-simple"],
  "difficulty": 1,
  "source": {"kind": "self_made", "title": "Public sample question", "license": "MIT"},
  "evidence": {"source_trace": "docs/schema.md", "public_safe": true}
}
```

## 简答题

```json
{
  "id": "sample-short-001",
  "type": "short_answer",
  "subject": "science",
  "stem": "Why should an experiment record the date and condition?",
  "answer": "So the result can be checked and repeated later.",
  "explanation": "Date and condition are part of the evidence trail.",
  "tags": ["experiment-record", "evidence"],
  "difficulty": 2,
  "source": {"kind": "self_made", "title": "Public sample question", "license": "MIT"},
  "evidence": {"source_trace": "docs/schema.md", "public_safe": true}
}
```

## 含表格的题目

表格可以直接放 markdown table。复杂表格也可以同时放图片字段。

```json
{
  "id": "sample-table-001",
  "type": "table",
  "subject": "math",
  "stem": "The table shows completed cards. How many cards were completed in total?",
  "tables": [
    {
      "caption": "Review cards completed",
      "markdown": "| Day | Cards |\\n|---|---:|\\n| Monday | 8 |\\n| Tuesday | 10 |\\n| Wednesday | 12 |"
    }
  ],
  "answer": "30",
  "tags": ["table-reading", "addition"],
  "difficulty": 1,
  "source": {"kind": "self_made", "title": "Public sample question", "license": "MIT"},
  "evidence": {"source_trace": "docs/schema.md", "public_safe": true}
}
```

## 含图片的题目

公开仓库里的图片必须是自制或可公开使用的图片。真实题库截图不能放入公开仓库。

```json
{
  "id": "sample-image-001",
  "type": "image",
  "subject": "physics",
  "stem": "Look at the self-made diagram. Which arrow shows the direction of gravity?",
  "images": [
    {
      "path": "examples/assets/gravity-demo.svg",
      "alt": "A public sample diagram with arrows.",
      "role": "question_diagram"
    }
  ],
  "answer": "downward arrow",
  "tags": ["force", "diagram-reading"],
  "difficulty": 1,
  "source": {"kind": "self_made", "title": "Public sample question", "license": "MIT"},
  "evidence": {"source_trace": "docs/schema.md", "public_safe": true}
}
```

## 连线题

连线题用左右两组和 `pairs` 表达，不依赖图片才能作答。

```json
{
  "id": "sample-matching-001",
  "type": "matching",
  "subject": "science",
  "stem": "Match each action with the evidence it creates.",
  "matching": {
    "left": [
      {"id": "a", "text": "Finish a practice question"},
      {"id": "b", "text": "Mark a wrong answer"}
    ],
    "right": [
      {"id": "1", "text": "EXP record"},
      {"id": "2", "text": "Mistake tag"}
    ],
    "pairs": [
      ["a", "1"],
      ["b", "2"]
    ]
  },
  "answer": "a-1, b-2",
  "tags": ["workflow", "evidence-loop"],
  "difficulty": 1,
  "source": {"kind": "self_made", "title": "Public sample question", "license": "MIT"},
  "evidence": {"source_trace": "docs/schema.md", "public_safe": true}
}
```

## 红灯规则

以下内容不应进入公开仓库：

- 真实学生姓名、家长信息、联系方式。
- 真实成绩数据、错题记录、学习报告。
- API key、密码、token、私钥。
- 买来的题库、教辅、真题原文或截图。
- 没有来源证据的答案和解析。
