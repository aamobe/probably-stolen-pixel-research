$ErrorActionPreference='Stop'
Add-Type -AssemblyName System.Drawing
$paths=@('../../inputs/private/furnace.png','furnace-a-original-template.png','furnace-b-github-template.png')
$results=foreach($p in $paths){
 $full=[IO.Path]::GetFullPath((Join-Path $PSScriptRoot $p))
 $b=[Drawing.Bitmap]::FromFile($full)
 try {
  $colors=[Collections.Generic.HashSet[int]]::new()
  $alphas=[Collections.Generic.HashSet[int]]::new()
  $n=0;$green=0
  for($y=0;$y -lt $b.Height;$y++){for($x=0;$x -lt $b.Width;$x++){
   $c=$b.GetPixel($x,$y);[void]$alphas.Add($c.A)
   if($c.R -eq 0 -and $c.G -eq 255 -and $c.B -eq 0){$green++}
   if($c.A -ge 128 -and -not ($c.G -gt 150 -and $c.G -gt $c.R*1.6 -and $c.G -gt $c.B*1.6)){[void]$colors.Add($c.ToArgb() -band 16777215);$n++}
  }}
  [ordered]@{file=$p;width=$b.Width;height=$b.Height;foregroundRgb=$colors.Count;alphaValueCount=$alphas.Count;foregroundPixels=$n;exactGreenPixels=$green;sha256=(Get-FileHash -LiteralPath $full).Hash;targetWidth=48;targetHeight=48;nativeSizeMatches=($b.Width -eq 48 -and $b.Height -eq 48)}
 }finally{$b.Dispose()}
}
$results|ConvertTo-Json -Depth 6|Set-Content -LiteralPath (Join-Path $PSScriptRoot 'metrics.json') -Encoding utf8
$results|ConvertTo-Json -Depth 6
