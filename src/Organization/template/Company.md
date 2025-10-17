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
    customer: true
    site: 
    image:
    image_scale:
    size:
    city:
    status: scop
    action: todo
    domains:
    - infogérance
    services:
    - logiciel libre
    valeurs:
    - ecologie
    references:
    - SNCF
pageDecoration:
  disableTOC: true
---
${person.insertImageFromFrontmatter()}
