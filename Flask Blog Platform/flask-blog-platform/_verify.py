"""Full verification of the running Flask app."""
import urllib.request as ur
import urllib.error as ue
import re

base = "http://127.0.0.1:5000"

def get(path):
    try:
        r = ur.urlopen(base + path)
        return r.status, r.read().decode("utf-8", errors="replace")
    except ue.HTTPError as e:
        return e.code, ""

results = []

# ---- HOMEPAGE ----
status, body = get("/")
results.append(("Homepage HTTP", status, status == 200))
results.append(("Both articles present", None,
    ("My Journey" in body) and ("Why I Love" in body)))
results.append(("My Journey present", None, "My Journey" in body))
results.append(("Why I Love present", None, "Why I Love" in body))
results.append(("post-card grid rendered", None, "post-card" in body))
results.append(("Empty state NOT shown", None, "No articles yet" not in body))

# Check image URLs actually serve
imgs = re.findall(r'src="(/static/uploads/post_images/[^"]+)"', body)
results.append(("Image URLs found in page", len(imgs), len(imgs) > 0))
for img_url in set(imgs):
    s, _ = get(img_url)
    results.append((f"Image HTTP {img_url[-20:]}", s, s == 200))

# ---- POST PAGES ----
s1, b1 = get("/post/1")
results.append(("Post 1 HTTP", s1, s1 == 200))
results.append(("Post 1 has title", None, "My Journey" in b1 or "Why I Love" in b1))

s2, b2 = get("/post/2")
results.append(("Post 2 HTTP", s2, s2 == 200))

# ---- AUTH PAGES ----
s3, _ = get("/login")
s4, _ = get("/register")
results.append(("Login HTTP", s3, s3 == 200))
results.append(("Register HTTP", s4, s4 == 200))

# ---- PRINT RESULTS ----
all_pass = True
print("\n=== VERIFICATION RESULTS ===")
for name, val, ok in results:
    status_str = "PASS" if ok else "FAIL"
    if not ok:
        all_pass = False
    print(f"  [{status_str}] {name}" + (f" = {val}" if val is not None else ""))

print(f"\n{'ALL CHECKS PASSED' if all_pass else 'SOME CHECKS FAILED'}")
