#Requires -Version 7
<#
.SYNOPSIS
    Ascendant Impact - session preflight. Run this before you start working.
.DESCRIPTION
    Checks the six things that have to be true before an agent session can do
    editor work, then prints exactly what to type next. Read-only: it changes
    nothing, it only tells you what is wrong.
.EXAMPLE
    pwsh -File sprint\start-session.ps1
#>
[CmdletBinding()]
param()

$ErrorActionPreference = 'Stop'
$Repo = Split-Path -Parent $PSScriptRoot
$script:Blockers = @()
$script:Warnings = @()

function Line($state, $text) {
    $color = switch ($state) { 'OK' {'Green'} 'WARN' {'Yellow'} 'STOP' {'Red'} default {'Gray'} }
    $tag   = switch ($state) { 'OK' {'[ OK ]'} 'WARN' {'[WARN]'} 'STOP' {'[STOP]'} default {'      '} }
    Write-Host "$tag " -ForegroundColor $color -NoNewline
    Write-Host $text
}
function Head($text) {
    Write-Host ''
    Write-Host $text -ForegroundColor Cyan
    Write-Host ('-' * $text.Length) -ForegroundColor DarkGray
}

Write-Host ''
Write-Host '  ASCENDANT IMPACT - session preflight' -ForegroundColor White
Write-Host "  $Repo" -ForegroundColor DarkGray
Write-Host "  $(Get-Date -Format 'yyyy-MM-dd HH:mm')" -ForegroundColor DarkGray

# ---------------------------------------------------------------- 1. the folder
Head '1. Working folder'
if (Test-Path (Join-Path $Repo 'game\AscendantImpact.uproject')) {
    Line OK 'game\AscendantImpact.uproject found - this is the one copy.'
} else {
    Line STOP 'No game\AscendantImpact.uproject here. Wrong folder.'
    $script:Blockers += 'Open a shell in C:\Users\athet\Documents\FightGame and re-run.'
}

# ------------------------------------------------------------------- 2. git
Head '2. Git'
Push-Location $Repo
try {
    $branch = (git rev-parse --abbrev-ref HEAD).Trim()
    if ($branch -eq 'main') { Line OK "On branch main." }
    else { Line WARN "On branch '$branch', not main. The sprint works on main."; $script:Warnings += "You are on '$branch'." }

    $dirty = @(git status --porcelain)
    if ($dirty.Count -eq 0) {
        Line OK 'Working tree clean.'
    } else {
        Line WARN "$($dirty.Count) uncommitted change(s). Commit before moving or deleting assets."
        $script:Warnings += "$($dirty.Count) uncommitted file(s) - see 'git status'."
    }

    git fetch --quiet origin 2>$null
    $counts = (git rev-list --left-right --count 'origin/main...HEAD' 2>$null)
    if ($counts) {
        $behind, $ahead = $counts -split '\s+'
        if ([int]$ahead -gt 0) {
            Line WARN "$ahead local commit(s) not pushed to origin."
            $script:Warnings += "$ahead commit(s) unpushed - 'git push origin main'."
        } else { Line OK 'Nothing unpushed.' }
        if ([int]$behind -gt 0) {
            Line WARN "$behind commit(s) on origin you do not have. Pull first."
            $script:Warnings += "$behind commit(s) behind origin - 'git pull'."
        } else { Line OK 'Up to date with origin.' }
    }
} finally { Pop-Location }

# --------------------------------------------------------------- 3. the editor
Head '3. Unreal editor'
$editors = @(Get-Process 'UnrealEditor' -ErrorAction SilentlyContinue)
$mine = @()
foreach ($e in $editors) {
    $cl = (Get-CimInstance Win32_Process -Filter "ProcessId=$($e.Id)" -ErrorAction SilentlyContinue).CommandLine
    if ($cl -match 'AscendantImpact\.uproject') { $mine += $e } 
}
if ($mine.Count -eq 1) {
    Line OK "Editor running on AscendantImpact (PID $($mine[0].Id))."
} elseif ($mine.Count -eq 0) {
    Line STOP 'Editor is not open on AscendantImpact.'
    $script:Blockers += 'Open game\AscendantImpact.uproject and wait for it to finish loading.'
} else {
    Line STOP "$($mine.Count) editors open on this project. One at a time - the MCP port is single-owner."
    $script:Blockers += 'Close all but one editor.'
}

# ------------------------------------------------------------------ 4. the MCP
Head '4. MCP server (port 8000)'
$listening = @(Get-NetTCPConnection -LocalPort 8000 -State Listen -ErrorAction SilentlyContinue)
if ($listening.Count -gt 0) {
    Line OK 'Something is listening on 127.0.0.1:8000.'
} else {
    Line STOP 'Nothing on port 8000 - the MCP server is not started.'
    $script:Blockers += 'In the editor console (Output Log -> Cmd box) type:  ModelContextProtocol.StartServer'
}
Line INFO 'Never enable bAutoStartServer - it makes the cook fail. Type the command.'

# ------------------------------------------------------- 5. what you are doing
Head '5. Next task'
$board = Get-Content (Join-Path $Repo 'sprint\BOARD.md') -Raw
$nextId = $null
if ($board -match '(?m)^\|\s*\*\*G\s*[^|]*\|\s*\*\*`(G\d+)`') { $nextId = $Matches[1] }
if ($nextId) {
    $file = Get-ChildItem (Join-Path $Repo 'sprint\tasks') -Filter "$nextId-*.md" | Select-Object -First 1
    $title = ((Get-Content $file.FullName | Select-String '^title:' | Select-Object -First 1) -replace '^title:\s*','').Trim()
    Line OK "NEXT UP (G track): $nextId - $title"
    Line INFO "  sprint\tasks\$($file.Name)"
} else {
    Line WARN 'Could not parse NEXT UP from sprint\BOARD.md - read it yourself.'
}

$inprog = @()
foreach ($t in Get-ChildItem (Join-Path $Repo 'sprint\tasks') -Filter '*.md') {
    if ((Get-Content $t.FullName -TotalCount 12) -match '^status:\s*in-progress') { $inprog += $t.BaseName }
}
if ($inprog.Count -gt 0) {
    Line WARN "Left open mid-task: $($inprog -join ', ')"
    Line INFO '  Read its Log block - the last line says where the previous session stopped.'
}

# ------------------------------------------------------------------- 6. verdict
Head 'Verdict'
if ($script:Blockers.Count -eq 0) {
    Line OK 'Preflight green. Start the session:'
    Write-Host ''
    Write-Host '      cd C:\Users\athet\Documents\FightGame' -ForegroundColor White
    Write-Host '      claude' -ForegroundColor White
    Write-Host ''
    Write-Host '  then type:  ' -NoNewline; Write-Host 'work the next task' -ForegroundColor White
    Write-Host '  Order matters: the MCP attaches when the session opens. Editor and server FIRST.' -ForegroundColor DarkGray
} else {
    Line STOP 'Do these first, in order, then re-run this script:'
    Write-Host ''
    $i = 1
    foreach ($b in $script:Blockers) { Write-Host "      $i. $b" -ForegroundColor White; $i++ }
    Write-Host ''
    Write-Host '  Do NOT open the Claude session until this comes back green -' -ForegroundColor DarkGray
    Write-Host '  a session opened before port 8000 is listening cannot see the editor tools.' -ForegroundColor DarkGray
}
if ($script:Warnings.Count -gt 0) {
    Write-Host ''
    Write-Host '  Worth knowing (not blocking):' -ForegroundColor Yellow
    foreach ($w in $script:Warnings) { Write-Host "      - $w" -ForegroundColor Gray }
}
Write-Host ''
exit ($script:Blockers.Count -gt 0 ? 1 : 0)
