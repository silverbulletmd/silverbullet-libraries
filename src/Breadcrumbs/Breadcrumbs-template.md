---
description: Adds breadcrumbs
tags: template
hooks.top:
  where: 'not pageDecoration.disableTOC'
  # Show all the way at the top
  order: -1
---
${yg.bc()}