
  !include "MUI2.nsh"

;--------------------------------
;General

  ;Name and file
  Name "RPC Profi"
  OutFile "rpc-profi-installer.exe"

  ;Default installation folder
  InstallDir "$PROGRAMFILES\RPC Profi"

  ;Get installation folder from registry if available
  InstallDirRegKey HKCU "Software\RPC PROFI" ""

  ;Request application privileges for Windows Vista
  ;RequestExecutionLevel user

  !define MUI_ABORTWARNING
  !define MUI_FINISHPAGE_NOAUTOCLOSE

;Pages

  !insertmacro MUI_PAGE_WELCOME
  !insertmacro MUI_PAGE_COMPONENTS
  !insertmacro MUI_PAGE_DIRECTORY
  !insertmacro MUI_PAGE_INSTFILES
  !insertmacro MUI_PAGE_FINISH

  !insertmacro MUI_UNPAGE_WELCOME
  !insertmacro MUI_UNPAGE_CONFIRM
  !insertmacro MUI_UNPAGE_INSTFILES
  !insertmacro MUI_UNPAGE_FINISH

;Languages
  !insertmacro MUI_LANGUAGE "German"
 
;Files reserved
  ReserveFile "python27.dll"
  ReserveFile "rpc-installer.py"


  Function .onInit
	;Extract Install Options files
	;$PLUGINSDIR will automatically be removed when the installer closes
	InitPluginsDir
	
	File "/oname=$PLUGINSDIR\python27.dll" "python27.dll"
	File "/oname=$PLUGINSDIR\rpc-installer.py" "rpc-installer.py"
  FunctionEnd

  Function .onGUIEnd
	nsPython::Finalize
  FunctionEnd

  Section "Projektcheck-Tools installieren"
    SetOutPath "$INSTDIR" 
	;relative path 
	File /r  /x *.exe /x .git /x .gitignore /x "3 Benutzerdefinierte Projekte" /x rpctools.egg-info /x *.pyc "..\..\*"
	CreateDirectory "$INSTDIR\3 Benutzerdefinierte Projekte"
	;Store installation folder
	WriteRegStr HKCU "Software\RPC Profi" "" $INSTDIR
	
    ;Create uninstaller
    WriteUninstaller "$INSTDIR\Uninstall.exe"
  SectionEnd

  Section "Bibliotheken installieren"
    
    nsPython::execFile "$PLUGINSDIR\rpc-installer.py"
    Pop $0
    DetailPrint "Result: $0"
  SectionEnd

  Section "AddIn installieren"
	ExecShell "" "$INSTDIR\4 Programminterne Daten\addin\addin.esriaddin"
  SectionEnd
  
Section "Uninstall"

  Delete "$INSTDIR\Uninstall.exe"

  RMDir /r "$INSTDIR"

  DeleteRegKey /ifempty HKCU "Software\RPC Profi"

SectionEnd

