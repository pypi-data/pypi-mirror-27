# NSIS script for creating the City Energy Analyst installer


; include the modern UI stuff
!include "MUI2.nsh"

# download miniconda from here:
!define MINICONDA "https://repo.continuum.io/miniconda/Miniconda2-latest-Windows-x86_64.exe"

!define CEA "City Energy Analyst"

# figure out the version based on cea\__init__.py
!system "get_version.exe"
!include "cea_version.txt"

Name "${CEA} ${VER}"
!define MUI_FILE "savefile"
!define MUI_BRANDINGTEXT "City Energy Analyst ${VER}"
CRCCheck On


OutFile "Output\Setup_CityEnergyAnalyst_${VER}.exe"


;--------------------------------
;Folder selection page

InstallDir "$LOCALAPPDATA\${CEA}"

;Request application privileges for Windows Vista
RequestExecutionLevel user

;--------------------------------
;Interface Settings

!define MUI_ABORTWARNING

;--------------------------------
;Pages

!insertmacro MUI_PAGE_LICENSE "..\LICENSE"
!insertmacro MUI_PAGE_INSTFILES

!insertmacro MUI_UNPAGE_CONFIRM
!insertmacro MUI_UNPAGE_INSTFILES

;--------------------------------
;Languages

  !insertmacro MUI_LANGUAGE "English"

;--------------------------------
;Installer Sections

Section "Dummy Section" SecDummy

SetOutPath "$INSTDIR"

;ADD YOUR OWN FILES HERE...
inetc::get ${MINICONDA} miniconda.exe
Pop $R0 ;Get the return value
StrCmp $R0 "OK" download_ok
    MessageBox MB_OK "Download failed: $R0"
    Quit
download_ok:
    # get on with life...
# install miniconda...
nsExec::ExecToLog '"$INSTDIR\miniconda.exe" /S /AddToPath=0 /RegisterPython=0 /NoRegistry=1 /D=$INSTDIR'
# use conda to install some stuff
nsExec::ExecToLog '"$INSTDIR\Scripts\conda.exe" install -c conda-forge geopandas ephem "pandas<0.20" scikit-learn'
nsExec::ExecToLog '"$INSTDIR\Scripts\conda.exe" install -c dlr-sc tbb freeimageplus gl2ps'
nsExec::ExecToLog '"$INSTDIR\Scripts\conda.exe" install -c oce -c pythonocc pythonocc-core=0.17.3'
nsExec::ExecToLog '"$INSTDIR\Scripts\conda.exe" install -c omnia cvxopt'
nsExec::ExecToLog '"$INSTDIR\Scripts\pip.exe" install cityenergyanalyst==${VER}'
nsExec::ExecToLog '"$INSTDIR\Scripts\cea.exe" install-toolbox'


# next, copy the *.pyd files, as they are not provided by pypi
# SetOutPath "$INSTDIR\Lib\site-packages\cea\demand"
# File "..\cea\demand\rc_model_sia_cc.pyd"
# SetOutPath "$INSTDIR\Lib\site-packages\cea\technologies"
# File "..\cea\technologies\calc_radiator.pyd"
# File "..\cea\technologies\storagetank_cc.pyd"
# SetOutPath "$INSTDIR"

;Create uninstaller
WriteUninstaller "$INSTDIR\Uninstall.exe"

SectionEnd

;--------------------------------
;Descriptions

;Language strings
;  LangString DESC_SecDummy ${LANG_ENGLISH} "A test section."

  ;Assign language strings to sections
;  !insertmacro MUI_FUNCTION_DESCRIPTION_BEGIN
;    !insertmacro MUI_DESCRIPTION_TEXT ${SecDummy} $(DESC_SecDummy)
;  !insertmacro MUI_FUNCTION_DESCRIPTION_END

;--------------------------------
;Uninstaller Section

Section "Uninstall"

  ;ADD YOUR OWN FILES HERE...

  Delete "$INSTDIR\Uninstall.exe"

  RMDir "$INSTDIR"

  DeleteRegKey /ifempty HKCU "Software\Modern UI Test"

SectionEnd