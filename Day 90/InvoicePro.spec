# -*- mode: python ; coding: utf-8 -*-
from PyInstaller.utils.hooks import collect_all

datas = [('C:/Users/HP/Desktop/invoice generator/app/resources', 'app/resources')]
binaries = []
hiddenimports = ['app', 'app.config', 'app.database', 'app.database.models', 'app.database.db', 'app.database.repositories', 'app.services', 'app.services.calculation_service', 'app.services.pdf_service', 'app.services.invoice_service', 'app.services.company_service', 'app.services.backup_service', 'app.ui', 'app.ui.main_window', 'app.ui.dashboard', 'app.ui.invoice_form', 'app.ui.invoice_history', 'app.ui.invoice_preview', 'app.ui.customer_management', 'app.ui.company_settings', 'app.ui.backup_restore', 'app.ui.about_dialog', 'app.ui.wizard', 'app.ui.components.badges', 'app.ui.components.cards', 'app.ui.components.items_table', 'app.ui.components.toast', 'app.ui.dialogs.customer_dialog', 'app.utils.formatters', 'app.utils.helpers', 'app.utils.num_to_words', 'app.utils.validators', 'PySide6', 'PySide6.QtCore', 'PySide6.QtGui', 'PySide6.QtWidgets', 'sqlalchemy', 'reportlab', 'num2words', 'PIL', 'pypdf']
tmp_ret = collect_all('app')
datas += tmp_ret[0]; binaries += tmp_ret[1]; hiddenimports += tmp_ret[2]


a = Analysis(
    ['C:/Users/HP/Desktop/invoice generator/app/main.py'],
    pathex=['C:/Users/HP/Desktop/invoice generator'],
    binaries=binaries,
    datas=datas,
    hiddenimports=hiddenimports,
    hookspath=[],
    hooksconfig={},
    runtime_hooks=[],
    excludes=[],
    noarchive=False,
    optimize=0,
)
pyz = PYZ(a.pure)

exe = EXE(
    pyz,
    a.scripts,
    [],
    exclude_binaries=True,
    name='InvoicePro',
    debug=False,
    bootloader_ignore_signals=False,
    strip=False,
    upx=True,
    console=False,
    disable_windowed_traceback=False,
    argv_emulation=False,
    target_arch=None,
    codesign_identity=None,
    entitlements_file=None,
)
coll = COLLECT(
    exe,
    a.binaries,
    a.datas,
    strip=False,
    upx=True,
    upx_exclude=[],
    name='InvoicePro',
)
