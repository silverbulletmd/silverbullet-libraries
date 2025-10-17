---
command:  new person
confirmName: true
openIfExists: true
tags: meta/template/page
suggestedName: ${editor.prompt("page name",editor.getCurrentPage().."/")}
frontmatter: |
  tags: 
  - person
  person:
    first_name:   
    last_name: 
    image: 
    image_scale:
    job:
      position: 
      - 
      company: Scop And Co
      department: 
      - consulting
      - 
      domains: 
      - it   
      skills:
      - 
      tools:
      - 
      customers:
      - 
      needs:
      - 
    personal:
      hobbies:
      - 
      children:
      - 
pageDecoration:
  disableTOC: true
---
${person.insertImageFromFrontmatter()}
