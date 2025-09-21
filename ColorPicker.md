# Color Picker

The color picker is a widget that allows you to easily select colors from a variety of options. You can use it to change the color of text, backgrounds, borders, or any other color-related CSS property.

The color picker provides a range of color options, including preset colors, a color picker, and a color wheel. You can also enter a color value manually by typing a hex code.

To use the color picker:
1. Open the color picker widget by clicking on the color picker icon in the toolbar.
2. Select a color from the options provided or enter a hex code in the input field.
3. Click on the color you want to use.
4. The selected color will be applied to the selected element.

Note: The color picker only works with CSS properties that support color values.


```space-lua
local function getSelectedtext()
  local text = space.readPage(editor.getCurrentPage())
  local cursorSelectionRange = editor.getSelection()

  local extractedText = string.sub(text, cursorSelectionRange.from + 1, cursorSelectionRange.to)
  
  return extractedText
end


-- Check if a string is a valid 3- or 6-digit hex color (with or without a leading '#')
local function isHex(s)
  local txtMatch = (string.match(s, '^#?[A-Za-z0-9][A-Za-z0-9][A-Za-z0-9]$') or string.match(s, '^#?[A-Za-z0-9][A-Za-z0-9][A-Za-z0-9][A-Za-z0-9][A-Za-z0-9][A-Za-z0-9]$')) ~= nil
  return txtMatch
end

local function expandHex36(hex)
  -- Duplicate each character to form the 6-digit code
  local r = string.sub(hex, 1, 1)
  local g = string.sub(hex, 2, 2)
  local b = string.sub(hex, 3, 3)
  
  return r .. r .. g .. g .. b .. b
end



local function openSidePanelWContent(htmlContent)
  -- js script to update color value on change
  local jsScript = [[
  const CP_ROOT = "colorp"
  const CP_ID = "First"

  const COLOR_PICKER_ID = `${CP_ROOT}${CP_ID}`
  const COLOR_PICKER_LBL_ID = `${CP_ROOT}${CP_ID}Lbl`
  const COLOR_PICKER_ADD_BTN_ID = `${CP_ROOT}AddColor`
  const COLOR_PICKER_OL_ID = `${CP_ROOT}List`
  
  const colorPicker = document.getElementById(COLOR_PICKER_ID)
  const colorPickerLbl = document.getElementById(COLOR_PICKER_LBL_ID)
  const colorPickerList = document.getElementById(COLOR_PICKER_OL_ID)
  const addColorBtn = document.getElementById(COLOR_PICKER_ADD_BTN_ID)

  var currentColorIndex = 0;
  var lastSetColor = colorPickerLbl.innerText;
  
  colorPicker.addEventListener("input", watchColorPicker, false);
  colorPicker.addEventListener("change", watchColorPicker, false);
  addColorBtn.addEventListener("click", addNewColor, false);
  
  function watchColorPicker(event) {
    colorPickerLbl.innerText = event.target.value;
    lastSetColor = event.target.value
  }

  function watchColorPickerAll(event) {
    const colorLabelID = event.target.id + "Lbl";
    document.getElementById(colorLabelID).innerHTML = " " + event.target.value;
    lastSetColor = event.target.value;
  }



  function addNewColor(event) {
    const newColorID = `${CP_ROOT}Li${currentColorIndex}`;
    // create list item 
    var li = document.createElement("li");
    var odiv = document.createElement("div");
    var colorBtn = document.createElement("input");

    colorBtn.type = "color";
    colorBtn.id = newColorID;
    colorBtn.name = newColorID;
    colorBtn.value = lastSetColor;
    colorBtn.oninput = watchColorPickerAll;

    var colorLbl = document.createElement("label");
    colorLbl.id = `${newColorID}Lbl`;
    colorLbl.for = newColorID;
    colorLbl.innerHTML = " " + lastSetColor;

    odiv.appendChild(colorBtn);
    odiv.appendChild(colorLbl);

    // append div to list item object and update list
    li.appendChild(odiv)
    colorPickerList.appendChild(li);
    currentColorIndex++;
  }

  ]]
  -- Inject script and show the html content in the panl 
  editor.showPanel("rhs", 1, htmlContent, jsScript)
end



local function closeSidePanelWContent()
  editor.hidePanel("rhs")
end


local function buildHTMLColorPicker(hex)
  local html = "<div>" ..
  "<input type='color' id='colorpFirst' value=#" .. hex .. ">" ..
  "<label id='colorpFirstLbl' for='colorpFirst'>#" .. hex .. "</label>" ..
  "<div>" ..
  "<button id='colorpAddColor'>Add Color</button>" ..
  "<hr/>" ..
  "<ol id='colorpList'>" ..
  "</ol>" ..
  "</div>" ..
  "</div>"
  return html
end



command.define {
  name = "ColorPicker - Show",
  key = "Alt-p",
  run = function()
    local txt = getSelectedtext()
    if isHex(txt) then
      local hexVal = string.gsub(txt, '^#', '')
      
      if string.len(hexVal) == 3 then
        hexVal = expandHex36(hexVal)
      end
      
      local html = buildHTMLColorPicker(hexVal)
      openSidePanelWContent(html)
      editor.flashNotification(hexVal)
    else
      local defaultHex = "000000"
      local html = buildHTMLColorPicker(defaultHex)
      openSidePanelWContent(html)
      editor.flashNotification(defaultHex)
    end
  end
}


command.define {
  name = "ColorPicker - Hide",
  key = "Escape",
  run = function()
    closeSidePanelWContent()
  end
}

```