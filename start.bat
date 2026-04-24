@echo off
chcp 65001

REM 一键启动AI行动助手后端和前端服务

echo =====================================
echo AI行动助手一键启动脚本
echo =====================================

REM 进入项目根目录
cd /d %~dp0

echo 当前目录: %cd%

REM 启动后端服务
echo 正在启动后端服务...
start "后端服务" cmd /k "cd backend && echo 启动后端服务... && uvicorn app.main:app --reload --host 0.0.0.0 --port 8000"

REM 等待3秒，确保后端服务开始启动
timeout /t 3 >nul

REM 启动前端服务
echo 正在启动前端服务...
start "前端服务" cmd /k "cd frontend && echo 启动前端服务... && npm run dev"

echo =====================================
echo 服务启动完成！
echo 后端服务地址: http://localhost:8000
echo 前端服务地址: http://localhost:5173
echo =====================================
echo 按任意键关闭此窗口...
pause >nul