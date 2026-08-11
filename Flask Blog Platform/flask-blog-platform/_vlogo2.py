import urllib.request as u
r = u.urlopen('http://127.0.0.1:5000/')
b = r.read().decode()
# Find the navbar section
nav_start = b.find('<nav ')
nav_end = b.find('</nav>', nav_start) + 6
navbar_html = b[nav_start:nav_end]
print('=== Navbar brand section ===')
brand_start = navbar_html.find('navbar-brand')
print(navbar_html[brand_start:brand_start+300])
