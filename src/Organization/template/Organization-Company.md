---
command:  new company
confirmName: true
openIfExists: true
suggestedName: ${editor.prompt("page name",editor.getCurrentPage().."/")}
tags: meta/template/page
frontmatter: |
  tags: 
  - company
  company:
    name: 
    customer: 
    site: 
    image:
    image_scale:
    size:
    city:
    status: 
    action: 
    domains:
    - 
    services:
    - 
    valeurs:
    - 
    references:
    - 
pageDecoration:
  disableTOC: true
---
${person.insertImageFromFrontmatter()}
