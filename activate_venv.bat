@echo off
chcp 65001 >nul
echo ========================================
echo 🚀 激活虚拟环境
echo ========================================
echo.

if not exist "venv\Scripts\activate.bat" (
    echo ❌ 虚拟环境不存在！
    echo 请先运行 setup_venv.bat 创建虚拟环境
    echo.
    pause
    exit /b 1
)

call venv\Scripts\activate.bat
echo ✅ 虚拟环境已激活
echo.
echo 📌 现在可以运行：
echo    python film_review_analysis.py
echo.
echo 💡 退出虚拟环境请输入：deactivate
echo.

cmd /k
