import os
import django
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'config.settings')
django.setup()

from django.test import Client
from django.urls import get_resolver
from django.urls import URLPattern, URLResolver

def get_all_urls(urlpatterns, prefix=""):
    urls = []
    for pattern in urlpatterns:
        if isinstance(pattern, URLPattern):
            # Try to build a valid viewable url. We might not be able to if there are args
            if "<" not in str(pattern.pattern):
                urls.append(prefix + str(pattern.pattern))
        elif isinstance(pattern, URLResolver):
            urls.extend(get_all_urls(pattern.url_patterns, prefix + str(pattern.pattern)))
    return urls

urls = get_all_urls(get_resolver().url_patterns)
c = Client()
failures = []
for url in urls:
    if url.startswith('admin/') or 'media/' in url or '^' in url:
        continue
    path = f"/{url}"
    print(f"Testing {path}...")
    try:
        response = c.get(path)
        if response.status_code >= 500:
            failures.append((path, response.status_code))
    except Exception as e:
        failures.append((path, str(e)))

if failures:
    print("\nFAILURES:")
    for path, err in failures:
        print(f"{path}: {err}")
else:
    print("\nALL OK")
