
Set CURRENTDIR=%~dp0
Set CURRENTDRIVE==%~d0
set anacondadir=C:\anaconda\envs\rpc
set anacondadrive=C:

cd %CURRENTDIR%rpctools
REM %anacondadir%\python setup.py build_ext --inplace

cd %anacondadir%\scripts
%anacondadrive%


SET SC=%CURRENTDIR%rpctools
sphinx-apidoc -f --separate -o %CURRENTDIR%docs\rpctools %SC%

cd %CURRENTDIR%
%CURRENTDRIVE%

