from prmp_lib.prmp_miscs.prmp_setup import PRMP_Setup

# d = PRMP_Setup('pyinstaller', name='PRMP Keeper', scripts=['app/main.py'], console=0)
d = PRMP_Setup('inno_setup', script='PRMP_Keeper.iss')
d.build()