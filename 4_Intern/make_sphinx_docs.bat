Set CURRENTDIR=%~dp0
Set CURRENTDRIVE==%~d0
set anacondadir=C:\anaconda\envs\rpc
set anacondadrive=C:

cd %CURRENTDIR%\docs
call make.bat clear
call make.bat html

cd %CURRENTDIR%
%CURRENTDRIVE%


