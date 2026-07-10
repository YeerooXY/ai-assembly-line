param(
    [string]$PlanningRun = "",
    [switch]$SkipPlanningRun,
    [switch]$StrictPlanningRun,
    [switch]$NoPull
)

$ErrorActionPreference = "Stop"

function Invoke-NativeChecked {
    param(
        [string]$Label,
        [scriptblock]$Command,
        [switch]$AllowFailure
    )

    Write-Host "`n== $Label =="
    $global:LASTEXITCODE = 0
    & $Command
    $exitCode = $LASTEXITCODE

    if ($exitCode -ne 0) {
        if ($AllowFailure) {
            Write-Host "WARN: $Label returned exit code $exitCode. Continuing because this step is allowed to fail."
        } else {
            throw "$Label failed with exit code $exitCode"
        }
    }
}

function Get-GitHead {
    $global:LASTEXITCODE = 0
    $head = (git rev-parse HEAD).Trim()
    if ($LASTEXITCODE -ne 0) {
        throw "git rev-parse HEAD failed with exit code $LASTEXITCODE"
    }
    return $head
}

Write-Host "== AI Assembly Line: sync and check =="

Invoke-NativeChecked "Current branch" { git branch --show-current }
Invoke-NativeChecked "Current HEAD before pull" { git log --oneline -1 }

$Before = Get-GitHead

if (-not $NoPull) {
    Invoke-NativeChecked "Pull latest" { git pull --ff-only }
} else {
    Write-Host "`n== Pull latest =="
    Write-Host "Skipped because -NoPull was supplied."
}

$After = Get-GitHead

Invoke-NativeChecked "Current HEAD after pull" { git log --oneline -1 }

if ($Before -ne $After) {
    Invoke-NativeChecked "Changed commits" { git log --oneline "$Before..$After" }
    Invoke-NativeChecked "Changed files" { git diff --name-status "$Before..$After" }
} else {
    Write-Host "`n== No new commits pulled =="
}

Invoke-NativeChecked "Build planning runs index" { python tools\build_planning_runs_index.py }
Invoke-NativeChecked "Validate AI entrypoints" { python tools\validate_agent_entrypoints.py }
Invoke-NativeChecked "Validate seed" { python tools\validate_seed.py }
Invoke-NativeChecked "Validate task batches" { python tools\validate_task_batches.py }
Invoke-NativeChecked "Validate collaboration state" { python tools\validate_collaboration_state.py }
Invoke-NativeChecked "Validate project workspaces" { python tools\validate_project_workspaces.py }

Invoke-NativeChecked "JavaScript syntax checks" {
    Get-ChildItem web -Filter *.js | Sort-Object Name | ForEach-Object {
        Write-Host (">>> node --check " + $_.Name)
        node --check $_.FullName
        if ($LASTEXITCODE -ne 0) {
            throw "node --check failed for $($_.FullName) with exit code $LASTEXITCODE"
        }
    }
}

if (-not $SkipPlanningRun -and $PlanningRun) {
    $allowPlanningFailure = -not $StrictPlanningRun
    Invoke-NativeChecked "Validate planning run: $PlanningRun" { python tools\validate_planning_run.py $PlanningRun } -AllowFailure:$allowPlanningFailure

    if ($allowPlanningFailure) {
        Write-Host "Planning run validation is allowed to fail by default because draft runs may intentionally omit generated outputs. Use -StrictPlanningRun to make this a hard failure."
    }
} else {
    Write-Host "`n== Validate planning run =="
    if ($SkipPlanningRun) {
        Write-Host "Skipped because -SkipPlanningRun was supplied."
    } else {
        Write-Host "Skipped because no -PlanningRun path was supplied."
        Write-Host "To validate one run, pass -PlanningRun planning_runs\<run-slug>."
    }
}

Invoke-NativeChecked "Git status" { git status --short }

Write-Host "`n== Done =="
