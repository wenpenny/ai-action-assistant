# 基于截图与系统上下文理解的 AI 行动助手

## 项目介绍

这是一个前后端分离的 H5 Web Demo，核心流程为：
截图上传 → OCR → 大模型解析 → 场景识别 → 生成建议动作 → 执行动作 → 历史记录

该项目旨在通过识别用户上传的截图内容，自动分析并生成相应的行动建议，帮助用户更高效地管理日程、任务和出行计划。

## 技术栈

### 前端
- Vue 3
- Vite
- TypeScript
- Vant
- Axios

### 后端
- Python 3.10+
- FastAPI
- Uvicorn
- SQLAlchemy
- SQLite

### OCR
- MockOCRService
- 预留 HttpOCRService

### LLM
- MockLLMService
- 预留 HttpLLMService

## 功能说明

- 上传截图并自动进行 OCR 识别
- 大模型解析 OCR 文本，提取结构化信息
- 识别场景类型（日程、任务、出行）
- 生成智能建议动作
- 执行建议动作（创建待办、设置提醒、打开地图、导出日历）
- 保存历史记录，支持查看和管理
- **删除事项功能**：支持删除不需要的事项，保持界面整洁

## 支持的截图场景

1. **schedule（日程类）**：活动海报、面试通知、会议安排、课程安排
2. **task（任务类）**：作业通知、群公告、报名要求、材料提交通知
3. **travel（出行类）**：车票截图、酒店订单、航班信息、地址与预约信息

## 支持的动作类型

- **create_todo**：创建待办事项
- **set_reminder**：设置提醒
- **open_map**：打开地图
- **export_calendar**：导出日历

## 项目目录结构

```
ai-action-assistant/
├── backend/
│   ├── app/
│   │   ├── core/
│   │   │   ├── config.py
│   │   │   └── database.py
│   │   ├── models/
│   │   │   ├── image.py
│   │   │   ├── parse_result.py
│   │   │   ├── todo.py
│   │   │   ├── reminder.py
│   │   │   └── action_record.py
│   │   ├── schemas/
│   │   │   ├── image.py
│   │   │   ├── parse_result.py
│   │   │   ├── action.py
│   │   │   └── history.py
│   │   ├── services/
│   │   │   ├── ocr_service.py
│   │   │   ├── llm_service.py
│   │   │   ├── parse_service.py
│   │   │   ├── action_service.py
│   │   │   ├── calendar_service.py
│   │   │   └── map_service.py
│   │   ├── api/
│   │   │   ├── upload.py
│   │   │   ├── parse.py
│   │   │   ├── action.py
│   │   │   └── history.py
│   │   ├── utils/
│   │   │   ├── file_utils.py
│   │   │   ├── json_utils.py
│   │   │   └── datetime_utils.py
│   │   └── main.py
│   ├── uploads/
│   └── requirements.txt
├── frontend/
│   ├── src/
│   │   ├── main.ts
│   │   ├── App.vue
│   │   ├── router/
│   │   │   └── index.ts
│   │   ├── api/
│   │   │   ├── http.ts
│   │   │   ├── upload.ts
│   │   │   ├── parse.ts
│   │   │   ├── action.ts
│   │   │   └── history.ts
│   │   ├── views/
│   │   │   ├── Home.vue
│   │   │   ├── Result.vue
│   │   │   ├── History.vue
│   │   │   └── HistoryDetail.vue
│   │   ├── components/
│   │   │   ├── ImageUploader.vue
│   │   │   ├── ParseSummaryCard.vue
│   │   │   ├── EntityEditor.vue
│   │   │   ├── ActionButtons.vue
│   │   │   ├── HistoryList.vue
│   │   │   ├── EmptyState.vue
│   │   │   └── LoadingBlock.vue
│   │   ├── types/
│   │   │   ├── parse.ts
│   │   │   ├── action.ts
│   │   │   └── history.ts
│   │   ├── styles/
│   │   │   └── theme.css
│   │   └── utils/
│   │       ├── scene.ts
│   │       ├── actions.ts
│   │       └── format.ts
│   ├── package.json
│   ├── vite.config.ts
│   ├── tsconfig.json
│   ├── tsconfig.node.json
│   └── index.html
├── start.bat
└── README.md
```

## 前端安装依赖步骤

1. 进入前端目录：
   ```bash
   cd ai-action-assistant/frontend
   ```

2. 安装依赖：
   ```bash
   npm install
   ```

## 后端安装依赖步骤

1. 进入后端目录：
   ```bash
   cd ai-action-assistant/backend
   ```

2. 安装依赖：
   ```bash
   pip install -r requirements.txt
   ```

## 如何启动后端

在后端目录下执行：
```bash
uvicorn app.main:app --reload --port 8000
```

## 如何启动前端

在前端目录下执行：
```bash
npm run dev
```

## 一键启动脚本

项目根目录提供了 `start.bat` 脚本，可一键启动前后端服务：

1. 双击运行 `start.bat` 文件
2. 脚本会自动启动后端和前端服务
3. 服务启动完成后，可访问以下地址：
   - 前端：http://localhost:5173
   - 后端：http://localhost:8000

## 默认端口说明

- 前端：http://localhost:5173
- 后端：http://localhost:8000

## 前后端联调说明

1. 确保后端服务已启动
2. 确保前端服务已启动
3. 前端会通过 Vite 代理将 `/api` 请求转发到后端服务
4. 访问 http://localhost:5173 即可使用应用

## Mock 服务说明

### MockOCRService 的作用

- 模拟 OCR 服务，根据图片文件名或内容返回示例 OCR 文本
- 无需真实 OCR API 即可测试完整流程
- 支持识别不同类型的截图（日程、任务、出行）

### MockLLMService 的作用

- 模拟大模型服务，根据 OCR 文本返回结构化解析结果
- 无需真实 LLM API 即可测试完整流程
- 支持识别不同场景类型并生成相应的建议动作

### 没有真实 OCR / 模型 API 时如何跑通 Demo

1. 确保后端配置中 OCR_SERVICE_TYPE 和 LLM_SERVICE_TYPE 都设置为 "mock"
2. 启动后端服务
3. 启动前端服务
4. 上传测试图片，系统会使用 Mock 服务进行处理

### 如果切换到真实 API，应修改哪些配置或服务类

1. 修改 `backend/app/core/config.py` 中的配置：
   - 设置 OCR_SERVICE_TYPE = "http"
   - 设置 OCR_API_URL 和 OCR_API_KEY
   - 设置 LLM_SERVICE_TYPE = "http"
   - 设置 LLM_API_URL 和 LLM_API_KEY

2. 实现 `HttpOCRService` 和 `HttpLLMService` 类中的具体 API 调用逻辑

## 前端界面优化

### 视觉风格

- 移动端 H5 风格设计
- 柔和渐变背景（蓝紫色或蓝白渐变）
- 主内容区居中，移动端宽度 max-width: 430px
- 卡片统一使用圆角、阴影、留白
- 按钮颜色区分动作类型：
  - 创建待办：蓝色
  - 设置提醒：橙色
  - 导出日历：绿色
  - 打开地图：紫色或青色
- 场景标签颜色区分：
  - task：蓝色或橙色
  - schedule：绿色或蓝色
  - travel：紫色或青色

### 页面优化

#### Result.vue
- 顶部固定风格的页面头部，包含返回按钮和标题
- 图片预览区域做成卡片，加载失败时显示占位图
- OCR 文本默认折叠，点击后展开
- 顶部增加统计卡片：已识别事项数、已生成建议动作数等
- 事项卡片之间有明显间距
- 每个事项卡片顶部展示场景标签、item_id、执行状态
- summary 作为卡片主标题，字体加粗
- entities 转成可读字段列表，只展示有值字段
- action buttons 放在卡片底部，按钮宽度统一
- 编辑和删除按钮放在卡片底部

#### ActionButtons.vue
- 按钮根据 action_type 显示不同颜色和文案
- 按钮支持 loading 状态
- 按钮执行成功后显示"已完成"
- 如果 payload 缺关键字段，按钮禁用，并显示原因
- 点击动作成功后，在当前 item 卡片内显示执行结果摘要

#### EntityEditor.vue
- 编辑字段时使用弹窗，字段分组显示
- 只显示当前 item 相关字段
- 字段分组：基础信息、时间信息、地点与链接、任务信息
- 保存按钮使用主色，取消按钮使用浅色
- 保存成功后显示 toast

#### HistoryDetail.vue
- 与 Result.vue 一致的视觉风格
- 每个 item 下展示对应 action_records
- 已执行动作用时间线或小卡片展示
- 如果某个 item 没有执行记录，显示"暂无执行记录"
- 支持重新执行未完成动作

#### Home.vue
- 首页增加产品 slogan："让截图变成下一步行动"
- 上传区做成大卡片按钮
- 增加三个示例场景说明
- 最近记录入口明显

## 推荐演示流程

1. 上传活动海报截图
2. 查看系统识别的日程信息
3. 点击"导出日历"或"打开地图"
4. 再上传作业通知截图
5. 点击"创建待办"或"设置提醒"
6. 尝试删除不需要的事项
7. 最后去历史记录页查看处理结果

## 常见问题排查

### 前端无法请求后端怎么办

1. 检查后端服务是否已启动
2. 检查后端端口是否为 8000
3. 检查前端 vite.config.ts 中的代理配置是否正确
4. 检查网络连接是否正常

### 图片上传失败怎么办

1. 检查图片大小是否超过 10MB
2. 检查图片格式是否支持（JPG、PNG、GIF 等）
3. 检查后端 uploads 目录是否存在且有写入权限
4. 检查后端服务是否正常运行

### 图片加载失败怎么办

1. 检查图片是否已成功上传到 `backend/uploads/` 目录
2. 检查数据库中 `images` 表的 `file_name` 字段是否正确
3. 检查前端是否正确获取了 `image_url` 字段

### SQLite 文件在哪里

SQLite 文件位于 `backend/db.sqlite3`

### .ics 文件生成后保存在哪里

.ics 文件保存在 `backend/uploads/calendar/` 目录下

### 如何查看 uploads 文件夹内容

直接访问 `backend/uploads/` 目录查看上传的图片和生成的文件

## 后续可扩展方向

1. 支持更多场景类型识别
2. 集成真实 OCR 和 LLM API
3. 添加用户认证系统
4. 支持多语言
5. 增加批量处理功能
6. 优化前端界面和用户体验
7. 添加更多动作类型
8. 支持云存储图片
9. 增加数据分析和统计功能
10. 开发移动端原生应用