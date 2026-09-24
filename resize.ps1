Add-Type -AssemblyName System.Drawing
$imagePath = 'C:\Users\JOHN\.gemini\antigravity-ide\brain\becb504a-1e42-4385-ae0d-e7fe2b3c38aa\media__1784180976887.jpg'
$img = [System.Drawing.Image]::FromFile($imagePath)

$sizes = @{
    'mipmap-mdpi' = 48
    'mipmap-hdpi' = 72
    'mipmap-xhdpi' = 96
    'mipmap-xxhdpi' = 144
    'mipmap-xxxhdpi' = 192
}

$baseDir = 'c:\Softly built updates\MpesaListenerApp\app\src\main\res'

foreach ($key in $sizes.Keys) {
    $size = $sizes[$key]
    $dest = Join-Path $baseDir $key
    if (!(Test-Path $dest)) {
        New-Item -ItemType Directory -Force -Path $dest | Out-Null
    }
    
    $destFile = Join-Path $dest 'ic_launcher.png'
    $bitmap = New-Object System.Drawing.Bitmap $size, $size
    $graphics = [System.Drawing.Graphics]::FromImage($bitmap)
    $graphics.InterpolationMode = [System.Drawing.Drawing2D.InterpolationMode]::HighQualityBicubic
    $graphics.DrawImage($img, 0, 0, $size, $size)
    $graphics.Dispose()
    
    $bitmap.Save($destFile, [System.Drawing.Imaging.ImageFormat]::Png)
    $bitmap.Dispose()
    Write-Host "Saved $destFile"
}

$img.Dispose()
