Set objShell = CreateObject("WScript.Shell")
Set objFSO = CreateObject("Scripting.FileSystemObject")

' Get current folder
currentFolder = objFSO.GetParentFolderName(WScript.ScriptFullName)

' Construct full path to the .bat file
batPath = Chr(34) & currentFolder & "\model.bat" & Chr(34)

' Run hidden (0 = hidden, False = don't wait)
objShell.Run batPath, 0, False
