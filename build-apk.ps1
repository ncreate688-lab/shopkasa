# ============================================================
# build-apk.ps1  --  Build MpesaListener APK (command-line only)
# No Android Studio UI is launched. Run from PowerShell:
#   .\build-apk.ps1
# ============================================================

$ProjectDir = "$PSScriptRoot\MpesaListenerApp"
$OutputApk  = "$PSScriptRoot\MpesaListener_Secure.apk"
$BuiltApk   = "$ProjectDir\app\build\outputs\apk\debug\app-debug.apk"

# -- 1. Find a Java runtime (standalone preferred, JBR as last resort) --
$JavaCandidates = @(
    "C:\Program Files\Microsoft\jdk-17*\bin\java.exe",
    "C:\Program Files\Eclipse Adoptium\jdk-17*\bin\java.exe",
    "C:\Program Files\Java\jdk-17*\bin\java.exe",
    "$env:USERPROFILE\scoop\apps\openjdk17\current\bin\java.exe",
    "$env:USERPROFILE\scoop\apps\temurin17\current\bin\java.exe",
    # Android Studio JBR - just a Java runtime, no UI is launched
    "C:\Program Files\Android\Android Studio\jbr\bin\java.exe"
)

$JavaExe = $null
foreach ($pattern in $JavaCandidates) {
    $match = Get-Item $pattern -ErrorAction SilentlyContinue | Select-Object -First 1
    if ($match) { $JavaExe = $match.FullName; break }
}

if (-not $JavaExe) {
    Write-Host "ERROR: No Java runtime found." -ForegroundColor Red
    Write-Host "Install with: winget install --id Microsoft.OpenJDK.17 --accept-source-agreements --accept-package-agreements" -ForegroundColor Yellow
    exit 1
}

$JavaHome = Split-Path (Split-Path $JavaExe)
Write-Host "Java: $JavaExe" -ForegroundColor Cyan

$env:JAVA_HOME = $JavaHome
$env:PATH      = "$JavaHome\bin;$env:PATH"

# -- 2. Build (stderr merged so SDK warnings don't cause exit-code confusion) --
Write-Host "Building APK..." -ForegroundColor Cyan
Push-Location $ProjectDir
try {
    cmd /c "gradlew.bat assembleDebug 2>&1"
} finally {
    Pop-Location
}

# -- 3. Check output APK exists --
if (Test-Path $BuiltApk) {
    Copy-Item $BuiltApk $OutputApk -Force
    $size = [math]::Round((Get-Item $OutputApk).Length / 1MB, 2)
    Write-Host "
✓ APK ready: $OutputApk ($size MB)" -ForegroundColor Green
} else {
    Write-Host "ERROR: Build failed - APK not found." -ForegroundColor Red
    exit 1
}
