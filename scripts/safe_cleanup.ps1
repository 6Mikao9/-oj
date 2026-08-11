Param(
    [switch]$IncludeRootTempText
)

$ErrorActionPreference = 'Stop'

# Safety guard: run from repository root
$root = Split-Path -Parent $PSScriptRoot
Set-Location $root

Write-Host "[INFO] Repository root: $root"

# Never touch these data directories
$protected = @(
    'oj\\problems',
    'oj\\data',
    'oj\\submissions'
)

Write-Host "[INFO] Protected paths:"
$protected | ForEach-Object { Write-Host "  - $_" }

$rootFiles = @(
    'debug_test.exe',
    'debug_v2.exe',
    'test2017_1.exe',
    'test2017_2.exe',
    'test2017_3.exe',
    'test2018_1.exe',
    'test2018_2.exe',
    'test2019_1.exe',
    'test2019_2.exe',
    'test2022_1.exe',
    'test2022_2.exe',
    'test_user.exe'
)

$ojFiles = @(
    'oj\\test.exe',
    'oj\\test_sol.exe',
    'oj\\test_user.exe',
    'oj\\temp_out.txt',
    'oj\\desktop.ini'
)

if ($IncludeRootTempText) {
    $rootFiles += 'test_out.txt'
}

foreach ($item in $rootFiles + $ojFiles) {
    if (Test-Path $item) {
        Remove-Item $item -Force
        Write-Host "[DEL] $item"
    }
}

if (Test-Path '__pycache__') {
    Remove-Item '__pycache__' -Recurse -Force
    Write-Host '[DEL] __pycache__/'
}
if (Test-Path 'oj\\__pycache__') {
    Remove-Item 'oj\\__pycache__' -Recurse -Force
    Write-Host '[DEL] oj/__pycache__/'
}

Write-Host '[OK] Safe cleanup finished.'
