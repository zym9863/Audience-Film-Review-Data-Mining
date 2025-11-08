@echo off
chcp 65001 >nul
echo ========================================
echo 🎬 影评数据挖掘分析系统（虚拟环境版）
echo ========================================
echo.

if not exist "venv\Scripts\activate.bat" (
    echo ❌ 虚拟环境不存在！
    echo 请先运行 setup_venv.bat 创建虚拟环境
    echo.
    pause
    exit /b 1
)

echo [1/2] 激活虚拟环境...
call venv\Scripts\activate.bat
echo ✅ 虚拟环境已激活
echo.

echo [2/2] 开始运行分析程序...
echo.

python film_review_analysis.py

if errorlevel 1 (
    echo.
    echo ❌ 分析过程中出现错误
    echo.
) else (
    echo.
    echo ========================================
    echo ✅ 分析完成！
    echo ========================================
    echo.
    echo 📁 结果已保存在 analysis_results 目录
    echo.
)

call deactivate
echo.
echo ✅ 虚拟环境已退出
echo.

pause
