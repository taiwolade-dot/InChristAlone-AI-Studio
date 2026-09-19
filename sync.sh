#!/data/data/com.termux/files/usr/bin/bash
echo "sync.sh is disabled: its source folder is older than this project. Remove the next line to re-enable." >&2
exit 1
cp -r "/storage/emulated/0/Nest Project/InChristAlone AI/"*.py ~/InChristAlone-AI/ 2>/dev/null
cp -r "/storage/emulated/0/Nest Project/InChristAlone AI/templates/"* ~/InChristAlone-AI/templates/ 2>/dev/null
cp -r "/storage/emulated/0/Nest Project/InChristAlone AI/static/"* ~/InChristAlone-AI/static/ 2>/dev/null
cp -r "/storage/emulated/0/Nest Project/InChristAlone AI/modules/"* ~/InChristAlone-AI/modules/ 2>/dev/null
echo "Synced!"#!/data/data/com.termux/files/usr/bin/bash
cp -r "/storage/emulated/0/Nest Project/InChristAlone AI/"*.py ~/InChristAlone-AI/ 2>/dev/null
cp -r "/storage/emulated/0/Nest Project/InChristAlone AI/templates/"* ~/InChristAlone-AI/templates/ 2>/dev/null
cp -r "/storage/emulated/0/Nest Project/InChristAlone AI/static/"* ~/InChristAlone-AI/static/ 2>/dev/null
echo "Synced!"
