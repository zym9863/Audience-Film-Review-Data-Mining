@echo off
chcp 65001 >nul
echo ========================================
echo 🎬 影评数据挖掘分析系统
echo ========================================
echo.

echo 开始运行分析程序...
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

pause
