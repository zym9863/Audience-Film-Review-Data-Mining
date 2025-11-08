@echo off
chcp 65001 >nul
echo ========================================
echo 🔧 创建Python虚拟环境
echo ========================================
echo.

echo [1/4] 检查Python环境...
python --version
if errorlevel 1 (
    echo ❌ 错误：未找到Python！请先安装Python 3.8+
    pause
    exit /b 1
)
echo ✅ Python环境正常
echo.

echo [2/4] 创建虚拟环境...
python -m venv venv
if errorlevel 1 (
    echo ❌ 虚拟环境创建失败
    pause
    exit /b 1
)
echo ✅ 虚拟环境创建成功
echo.

echo [3/4] 激活虚拟环境...
call venv\Scripts\activate.bat
echo ✅ 虚拟环境已激活
echo.

echo [4/4] 安装项目依赖...
python -m pip install --upgrade pip
pip install -r requirements.txt -i https://pypi.tuna.tsinghua.edu.cn/simple
echo.

if errorlevel 1 (
    echo ❌ 依赖安装失败
    pause
    exit /b 1
)

echo ========================================
echo ✅ 虚拟环境配置完成！
echo ========================================
echo.
echo 📌 后续使用说明：
echo.
echo 1. 激活虚拟环境：
echo    venv\Scripts\activate.bat
echo.
echo 2. 运行分析（虚拟环境下）：
echo    python film_review_analysis.py
echo.
echo 3. 退出虚拟环境：
echo    deactivate
echo.
echo 💡 提示：已为您创建 activate_venv.bat 快捷启动脚本
echo.

pause
