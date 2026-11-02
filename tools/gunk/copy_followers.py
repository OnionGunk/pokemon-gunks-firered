"""Copy pokeemerald-expansion's follower sprites for FireRed's species into graphics/gunk_followers/<species>/."""
import os, re, shutil, sys
repo, exp = sys.argv[1], sys.argv[2]
src = open(os.path.join(repo, 'include/constants/species.h')).read()
species = re.findall(r'#define SPECIES_(\w+) (\d+)', src)
missing, n = [], 0
for name, num in species:
    num = int(num)
    if num == 0 or name.startswith('OLD_UNOWN') or name in ('EGG',) or num > 411:
        continue
    folder = name.lower()
    d = os.path.join(exp, 'graphics/pokemon', folder)
    if not os.path.exists(os.path.join(d, 'overworld.png')):
        missing.append(name); continue
    out = os.path.join(repo, 'graphics/gunk_followers', folder)
    os.makedirs(out, exist_ok=True)
    for f in ('overworld.png', 'overworld_normal.pal', 'overworld_shiny.pal'):
        shutil.copyfile(os.path.join(d, f), os.path.join(out, f))
    n += 1
print(n, 'copied; missing:', missing)
