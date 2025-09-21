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
      company: 
      department: 
      - 
      domains: 
      -    
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
