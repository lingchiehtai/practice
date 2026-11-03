cd /d "%~dp0"

echo.
echo === running rename photo files===
echo.

call python rename_photos_by_date.py
call python rename_photos_keywords.py

echo.
echo === finish ===
pause