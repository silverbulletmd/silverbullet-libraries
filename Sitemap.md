# Sitemap Generation

The Sitemap Generation feature allows you to generate a sitemap for your space. The sitemap is an XML file that lists all the pages in your space along with their URLs and other metadata.

By using the Sitemap Generation feature, you can:
- Make your space discoverable by search engines
- Improve the visibility of your pages in search results
- Optimize your site's performance by providing a comprehensive list of all its pages

```space-lua
do
  local defaults = {
    domain = "o.stag.lol"; -- base absolute domain (fallback if not in http header)
    cf = "weekly"; -- default for <changefreq>
    cfname = "changefreq"; -- frontmatter attribute to be used
  }

  -- js: export default encodeURIComponent
  local encodeURI = js.import("data:text/javascript,export%20default%20encodeURIComponent")

  local function gensitemap(host)
    local sitemap = ""
  
    for page in each(space.listPages()) do
      if not (
        page.name:startsWith("Library/") or
        page.name == page.name:upper()
      ) then
        sitemap = sitemap + spacelua.interpolate([[
          <url>
            <loc>https://${host}/${encodeURI(page.name)}</loc>
            <lastmod>${page.lastModified}</lastmod>
            <changefreq>${page[defaults.cfname] or defaults.cf}</changefreq>
          </url>
        ]], {host=host;encodeURI=encodeURI;page=page;defaults=defaults})
      end
    end
  
    return spacelua.interpolate([[
      <?xml version="1.0" encoding="UTF-8"?>
      <urlset xmlns="http://www.sitemaps.org/schemas/sitemap/0.9">
        ${sitemap}
      </urlset>
    ]], {sitemap=sitemap})
  end
  
  event.listen {
    name = "http:request:/sitemap.xml";
    run = function(event)
      local stat, res = pcall(function()
        return gensitemap(event.data.headers.host or defaults.domain)
      end)
      
      return {
        status = 200;
        headers = {
          ["Content-Type"] = stat and "application/xml" or "text/plain";
        };
        body = stat and res or "Error: " .. res;
      }
    end;
  }
 end
```