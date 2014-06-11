for /f "delims=" %%a In ('dir /ad/b  "./" ') Do mklink /J ..\web2py\applications\%%a .\%%a
pause