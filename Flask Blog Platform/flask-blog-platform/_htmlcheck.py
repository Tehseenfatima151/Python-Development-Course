"""Check rendered HTML of each page for known markers."""
import urllib.request as req, urllib.error as err

checks = {
    '/': ['hero-title', 'hero-eyebrow', 'site-footer', 'navbar-brand', 'FlaskBlog'],
    '/login': ['auth-form-title', 'auth-left', 'togglePwd', 'form-label', 'site-footer'],
    '/register': ['auth-form-title', 'upload-area', 'showFileName', 'site-footer'],
}

all_ok = True
for path, markers in checks.items():
    try:
        body = req.urlopen('http://127.0.0.1:5000' + path).read().decode('utf-8', errors='replace')
        for m in markers:
            if m not in body:
                print(f'MISSING  {path}  [{m}]')
                all_ok = False
    except err.HTTPError as e:
        print(f'HTTP {e.code}  {path}')
        all_ok = False

if all_ok:
    print('ALL CHECKS PASSED')
