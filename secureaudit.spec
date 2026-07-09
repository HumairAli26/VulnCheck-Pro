# secureaudit.spec
# Build with:  pyinstaller secureaudit.spec
# Run this ON each target OS (Windows/macOS/Linux) — PyInstaller does not cross-compile.

import sys
from PyInstaller.utils.hooks import collect_submodules

block_cipher = None
is_mac = sys.platform == "darwin"
is_win = sys.platform.startswith("win")

hidden_imports = (
    collect_submodules("sqlalchemy.dialects.sqlite")
    + collect_submodules("reportlab")
)

a = Analysis(
    ["app.py"],
    pathex=["."],
    binaries=[],
    datas=[
        ("src/config", "src/config"),   # theme/colors/fonts assets if any non-.py files added
    ],
    hiddenimports=hidden_imports,
    hookspath=[],
    runtime_hooks=[],
    excludes=[],
    cipher=block_cipher,
    noarchive=False,
)

pyz = PYZ(a.pure, a.zipped_data, cipher=block_cipher)

exe = EXE(
    pyz,
    a.scripts,
    [],
    exclude_binaries=True,
    name="SecureAudit",
    debug=False,
    strip=False,
    upx=True,
    console=False,          # windowed app, no terminal popup
    icon="assets/icon.ico" if is_win else ("assets/icon.icns" if is_mac else None),
)

coll = COLLECT(
    exe,
    a.binaries,
    a.zipfiles,
    a.datas,
    strip=False,
    upx=True,
    name="SecureAudit",
)

if is_mac:
    app = BUNDLE(
        coll,
        name="SecureAudit.app",
        icon="assets/icon.icns",
        bundle_identifier="com.humairali.secureaudit",
        info_plist={
            "NSHighResolutionCapable": "True",
            "CFBundleShortVersionString": "0.4.0",
            "NSHumanReadableCopyright": "MIT License",
            # SecureAudit inspects firewall/encryption state — declare intent so
            # macOS doesn't silently block it under future privacy prompts.
            "LSApplicationCategoryType": "public.app-category.utilities",
        },
    )
