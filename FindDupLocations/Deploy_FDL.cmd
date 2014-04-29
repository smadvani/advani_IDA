if EXIST "C:\iDBanalyst" goto nomkdir
mkdir "C:\iDBanalyst"
mkdir "C:\iDBanalyst\Styles"
mkdir "C:\iDBanalyst\Styles\concentration\"
mkdir "C:\iDBanalyst\projects"
:nomkdir

if EXIST "%USERPROFILE%\.qgis2" goto foundit
REM C:\Users\jesse\.qgis2\python\plugins
echo "%USERPROFILE%\.qgis2 not found"
goto notfound
:foundit
echo "Found user folder %USERPROFILE%\.qgis2"
C:\Users\jesse\.qgis2\python\plugins
rem xcopy /S/Y ".\*.db" "%USERPROFILE%\.qgis2\python\plugins\FindDupLocations\*.db"
xcopy /S/Y ".\*.py" "%USERPROFILE%\.qgis2\python\plugins\FindDupLocations\*.py"
xcopy /S/Y ".\*.qrc" "%USERPROFILE%\.qgis2\python\plugins\FindDupLocations\*.qrc"
xcopy /S/Y ".\*.txt" "%USERPROFILE%\.qgis2\python\plugins\FindDupLocations\*.txt"
xcopy /S/Y/I ".\icons\*.png" "%USERPROFILE%\.qgis2\python\plugins\FindDupLocations\icons\"
xcopy /S/Y/I ".\tools\*.py" "%USERPROFILE%\.qgis2\python\plugins\FindDupLocations\tools\"
ECHO iDBanalyst Deployed to %USERPROFILE%\.qgis2
exit
:notfound
ECHO iDBanalyst Deployed.
exit