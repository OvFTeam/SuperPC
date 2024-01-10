SetTitleMatchMode, 2
#SingleInstance force

FileInstall, config.ini, %A_AppData%\config.ini, 1
if (ProcessExist("chrome.exe"))
{
    WinActivate, ahk_exe chrome.exe
}
else
{
    configFile := A_AppData . "\config.ini"
    file := FileOpen(configFile, "r")
    if IsObject(file)
    {
        fileContents := file.Read()
        file.Close()
    }
    else
    {
        return
    }
    lines := StrSplit(fileContents, "`n")
    Loop, % lines.Length()
    {
        line := lines[A_Index]
        if (line <> "")
        {
            parts := StrSplit(line, "=")
            if (parts.Length() > 1)
            {
                linkName := Trim(parts[1])
                linkURL := Trim(parts[2])
                linkURL := StrReplace(linkURL, "`r", "")
                if (linkURL <> "")
                {
                    Run, chrome.exe "%linkURL%"
                }
            }
        }
    }
}

ProcessExist(processName) {
    processExist := false
    for process in ComObjGet("winmgmts:").ExecQuery("Select * from Win32_Process") {
        If (process.Name = processName) {
            processExist := true
            break
        }
    }
    return processExist
}