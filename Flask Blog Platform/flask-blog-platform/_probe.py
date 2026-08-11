"""Probe all public routes for HTTP errors."""
import urllib.request as req
import urllib.error as err

routes = [
    ('GET', '/'),
    ('GET', '/login'),
    ('GET', '/register'),
    ('GET', '/post/9999'),      # should 404
    ('GET', '/user/9999'),      # should 404
    ('GET', '/create-post'),    # should redirect to login (302 -> 200 on /login)
    ('GET', '/profile'),        # should redirect to login
    ('GET', '/edit-post/9999'), # should redirect to login
]

for method, path in routes:
    url = 'http://127.0.0.1:5000' + path
    try:
        r = req.urlopen(url)
        # if we land here urllib followed a redirect
        final = r.url.replace('http://127.0.0.1:5000', '')
        print(f'200  {path}  (final: {final})')
    except err.HTTPError as e:
        print(f'{e.code}  {path}')
    except Exception as e:
        print(f'ERR  {path}  {e}')
