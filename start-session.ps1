#Requires -Version 7
<#
.SYNOPSIS
    Ascendant Impact - session preflight. Run this before you start working.
.DESCRIPTION
    Checks the five things that have to be true before a session can do editor work,
    then prints exactly what to type next. Read-only: it changes nothing, it only
    tells you what is wrong.
.EXAMPLE
    pwsh -File start-session.ps1
#>
[CmdletBinding()]
param()

$ErrorActionPreference = 'Stop'
$Repo = $PSScriptRoot
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
    if ($branch -eq 'main') { Line OK 'On branch main.' }
    else {
        Line WARN "On branch '$branch', not main."
        $script:Warnings += "You are on '$branch'."
    }

    $dirty = @(git status --porcelain)
    $assets = @($dirty | Where-Object { $_ -match '\.(uasset|umap)$' })
    $other  = @($dirty | Where-Object { $_ -notmatch '\.(uasset|umap)$' })

    if ($dirty.Count -eq 0) {
        Line OK 'Working tree clean.'
    } else {
        if ($other.Count -gt 0) {
            Line WARN "$($other.Count) uncommitted non-asset change(s)."
            $script:Warnings += "$($other.Count) uncommitted file(s) - see 'git status'."
        }
        if ($assets.Count -gt 0) {
            Line INFO "$($assets.Count) changed Blueprint/map asset(s) - agents must NOT commit these."
            Line INFO '  Binary + LFS. Commit them by hand if you want them saved.'
        }
    }

    git fetch --quiet origin 2>$null
    $counts = (git rev-list --left-right --count 'origin/main...HEAD' 2>$null)
    if ($counts) {
        $behind, $ahead = $counts -split '\s+'
        if ([int]$ahead  -gt 0) { Line WARN "$ahead local commit(s) not pushed."; $script:Warnings += "$ahead commit(s) unpushed - 'git push origin main'." }
        else { Line OK 'Nothing unpushed.' }
        if ([int]$behind -gt 0) { Line WARN "$behind commit(s) on origin you do not have."; $script:Warnings += "$behind behind origin - 'git pull'." }
        else { Line OK 'Up to date with origin.' }
    }
} finally { Pop-Location }

# --------------------------------------------------------------- 3. the editor
Head '3. Unreal editor'
$mine = @()
foreach ($e in @(Get-Process 'UnrealEditor' -ErrorAction SilentlyContinue)) {
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
if (@(Get-NetTCPConnection -LocalPort 8000 -State Listen -ErrorAction SilentlyContinue).Count -gt 0) {
    Line OK 'Something is listening on 127.0.0.1:8000.'
} else {
    Line STOP 'Nothing on port 8000 - the MCP server is not started.'
    $script:Blockers += 'In the editor console (Output Log -> Cmd box) type:  ModelContextProtocol.StartServer'
}
Line INFO 'Never enable bAutoStartServer - it breaks packaging. Type the command.'

# ------------------------------------------------------- 5. what you are doing
Head '5. Next step'
$planPath = Join-Path $Repo 'FINISH-PLAN.md'
if (-not (Test-Path $planPath)) {
    Line STOP 'FINISH-PLAN.md is missing. That file is the plan.'
    $script:Blockers += 'Restore FINISH-PLAN.md.'
} else {
    $rows = Select-String -Path $planPath -Pattern '^\|\s*(\d{1,2})\s*\|\s*([^|]+?)\s*\|\s*`(todo|in-progress|done|cut)`\s*\|'
    $steps = foreach ($r in $rows) {
        [pscustomobject]@{
            N      = [int]$r.Matches[0].Groups[1].Value
            Title  = $r.Matches[0].Groups[2].Value.Trim()
            Status = $r.Matches[0].Groups[3].Value
        }
    }
    if (-not $steps) {
        Line WARN 'Could not read the status table in FINISH-PLAN.md - open it yourself.'
    } else {
        $done = @($steps | Where-Object Status -in 'done','cut').Count
        $wip  = @($steps | Where-Object Status -eq 'in-progress')
        $next = $steps | Where-Object Status -eq 'todo' | Sort-Object N | Select-Object -First 1

        Line OK "$done of $($steps.Count) steps closed."
        foreach ($w in $wip) { Line WARN "IN PROGRESS - Step $($w.N): $($w.Title)" }
        if ($next) { Line OK "NEXT - Step $($next.N): $($next.Title)" }
        else { Line OK 'No steps left in todo. Check the plan.' }
        Line INFO '  Full detail: FINISH-PLAN.md'
    }
}

# ------------------------------------------------------------------- 6. verdict
Head 'Verdict'
if ($script:Blockers.Count -eq 0) {
    Line OK 'Preflight green. Start the session:'
    Write-Host ''
    Write-Host '      claude' -ForegroundColor White
    Write-Host ''
    Write-Host '  then type:  ' -NoNewline; Write-Host 'work the next step' -ForegroundColor White
    Write-Host '  Order matters: MCP attaches when the session opens. Editor and server FIRST.' -ForegroundColor DarkGray
} else {
    Line STOP 'Do these first, in order, then re-run this script:'
    Write-Host ''
    $i = 1
    foreach ($b in $script:Blockers) { Write-Host "      $i. $b" -ForegroundColor White; $i++ }
    Write-Host ''
    Write-Host '  Do NOT open the Claude session until this is green - a session opened' -ForegroundColor DarkGray
    Write-Host '  before port 8000 is listening cannot see the editor tools.' -ForegroundColor DarkGray
}
if ($script:Warnings.Count -gt 0) {
    Write-Host ''
    Write-Host '  Worth knowing (not blocking):' -ForegroundColor Yellow
    foreach ($w in $script:Warnings) { Write-Host "      - $w" -ForegroundColor Gray }
}
Write-Host ''
exit ($script:Blockers.Count -gt 0 ? 1 : 0)
