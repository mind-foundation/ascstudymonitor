""" Provide sitemap template as string """

sitemap_template = """
<?xml version="1.0" encoding="utf-8"?>
<urlset xmlns="http://www.sitemaps.org/schemas/sitemap/0.9" xmlns:xsi="http://www.w3.org/2001/XMLSchema-instance" xsi:schemaLocation="http://www.sitemaps.org/schemas/sitemap/0.9 http://www.sitemaps.org/schemas/sitemap/0.9/sitemap.xsd">
    <url>
        <loc>https://asc-studymonitor.mind-foundation.org/index.html</loc>
    </url>
  {%- for url in urlset %}
    <url>
        <loc>{{ url["loc"] }}</loc>
        {%- if "lastmod" in url %}
        <lastmod>{{ url["lastmod"] }}</lastmod>
        {%- endif %}
        {%- if "changefreq" in url %}
        <changefreq>{{ url["changefreq"] }}</changefreq>
        {%- endif %}
        {%- if "priority" in url %}
        <priority>{{ url["priority"] }}</priority>
        {%- endif %}
    </url>
  {%- endfor %}
</urlset>
"""
