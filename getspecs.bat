msinfo32 /nfo %TEMP%\%computername%_sysinfo.xml /categories +all -loadedmodules
wmic MemoryChip get /format:csv > %TEMP%\%computername%_mem.csv
wmic BaseBoard get /format:csv > %TEMP%\%computername%_mb.csv
tar -czf info.tar.gz -C %TEMP% %computername%_mem.csv %computername%_mb.csv %computername%_sysinfo.xml
del %TEMP%\%computername%_mem.csv
del %TEMP%\%computername%_mb.csv
del %TEMP%\%computername%_sysinfo.xml
:: del info.tar.gz
pause
