Param()

$ErrorActionPreference = 'Stop'
$root = Split-Path -Parent $PSScriptRoot
Set-Location $root

git config core.hooksPath .githooks
Write-Host "[OK] git hooks path set to .githooks"

$hook = Join-Path $root '.githooks\pre-commit'
if (Test-Path $hook) {
    Write-Host "[OK] pre-commit hook exists: $hook"
} else {
    Write-Host "[ERROR] pre-commit hook missing: $hook"
    exit 1
}
