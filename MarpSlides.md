# Marp Preview

This library provides a way to preview your Marp slides in a panel while you are editing your space.

With Marp Preview, you can:
- Preview your slides without leaving the context of your space
- See how your slides look in real-time as you modify your markdown
- Use the Marp Preview panel to navigate through your slides and see them in action

See [source](https://community.silverbullet.md/t/marp-preview-plugin/741)

```space-lua
local LOG_ENABLE = false

local function debug_log(message)
  if LOG_ENABLE then
    js.log("[DEBUG] " .. message)
  end
end

local is_panel_visible = false
local current_panel_id = "rhs"

-- Function to render Marp slides
local function render_marp_slides(mode)  
    debug_log(mode)
    if (not is_panel_visible and mode) or (not mode and is_panel_visible) then
      -- Get the current page content
      local page_content = editor.getText()
      debug_log(page_content)
      local panel_html =  '<div id="render" style="flex: 1; overflow-y: auto"></div>'
      local contentBase64=encoding.base64Encode(page_content)
      local marp_js = [[
const script = document.createElement("script");
script.type = "module";
script.textContent = `
     
import { Marp } from 'https://esm.sh/@marp-team/marp-core?bundle'
function b64DecodeUnicode(str) {
// Going backwards: from bytestream, to percent-encoding, to original string.
return decodeURIComponent(atob(str).split('').map(function(c) {
    return '%' + ('00' + c.charCodeAt(0).toString(16)).slice(-2);
}).join(''));
}
 
const marp =  new Marp();
const { html, css } = marp.render(b64DecodeUnicode("]]..contentBase64..[["));
render.innerHTML = \`\${html}<style>\${css}</style>\`;
`
 document.documentElement.appendChild(script);       
    ]]
       debug_log(marp_js)
       editor.showPanel(current_panel_id,1,  panel_html, marp_js)
       is_panel_visible = true
    else
        -- Hide the panel if it's visible
        editor.hidePanel(current_panel_id)
        is_panel_visible = false
    end
end

-- Define the command
command.define({
    name = "Marp Preview: Toggle",
    description = "Toggle Marp slides render in a panel",
    run = function(e)
      render_marp_slides(true)
    end
})

-- Listen for page modifications
event.listen({
    name = "editor:pageModified",
    run = function(e)
      render_marp_slides(false)
    end
})

```
