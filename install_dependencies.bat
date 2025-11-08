@echo off
chcp 65001 >nul
echo ========================================
echo 影评数据挖掘系统 - 依赖安装脚本
echo ========================================
echo.

echo [1/3] 检查Python环境...
python --version
if errorlevel 1 (
    echo ❌ 错误：未找到Python！请先安装Python 3.8+
    pause
    exit /b 1
)
echo ✅ Python环境正常
echo.

echo [2/3] 升级pip...
python -m pip install --upgrade pip
echo ✅ pip升级完成
echo.

echo [3/3] 安装依赖包...
pip install -r requirements.txt -i https://pypi.tuna.tsinghua.edu.cn/simple
echo.

if errorlevel 1 (
    echo ❌ 安装过程中出现错误，请检查网络连接
    pause
    exit /b 1
) else (
    echo ========================================
    echo ✅ 所有依赖安装完成！
    echo ========================================
    echo.
    echo 现在可以运行 run_analysis.bat 开始分析
    echo.
)

pause
