#!/usr/bin/env python3
from pathlib import Path
import subprocess, tempfile, shutil
ROOT=Path(__file__).resolve().parents[1]
# Music only: keep short SFX untouched.
roots=[ROOT/'assets/music', ROOT/'assets/songs', ROOT/'assets/shared/music']
files=[p for r in roots if r.exists() for p in r.rglob('*.mp3')]
orig=0; new=0; changed=0
for p in files:
    orig += p.stat().st_size
    fd,tmp=tempfile.mkstemp(suffix='.mp3',dir=p.parent); Path(tmp).unlink()
    try:
        subprocess.run(['ffmpeg','-y','-loglevel','error','-i',str(p),'-map_metadata','0','-c:a','libmp3lame','-b:a','96k','-ar','44100','-ac','2',tmp],check=True)
        size=Path(tmp).stat().st_size
        if size < p.stat().st_size:
            shutil.copystat(p,tmp)
            Path(tmp).replace(p); changed+=1; new+=size
        else:
            Path(tmp).unlink(missing_ok=True); new+=p.stat().st_size
    except Exception:
        Path(tmp).unlink(missing_ok=True); raise
print(f'files={len(files)} changed={changed}')
print(f'bytes={orig} -> {new} ({new/orig:.1%}, saved={(orig-new)/1048576:.1f} MiB)')
