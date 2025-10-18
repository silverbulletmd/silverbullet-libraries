# Taiga 
[Taiga](https://taiga.io/): *The* free and open-source project management tool

```toml
# Check network queries in browser to define userId &  projectId
# Configuration
    taiga ={
      user="user account",
      userId="userid",
      password="password",
      projectId="default project id"
  }
```
```lua
# Default query
${template.each(
  query[[
    from getTaigaTasks() 
    where status_extra_info.name != 'Done'
    order by status_extra_info.name
  ]], templates.taigaRecurringTasks
)}
# Custom query
${template.each(
  query[[
    from getTaigaTasks("/userstories?project=xxxx&status__is_archived=false") 
    where status_extra_info.name != 'Done' and status_extra_info.name != 'New'
    order by status_extra_info.name
  ]], templates.taigaRecurringTasks
)}

```


```space-lua
TAIGA_TOKENS=nil
LOG_ENABLE=false
local baseUrl = "https://api.taiga.io/api/v1"

-- Basic token mangement
local function getToken()
  if TAIGA_TOKENS == nil then 
    local apiUrl = (baseUrl .. "/auth")
    local body='{ "type": "normal", "username":"'.. config.get("taiga").user..'", "password": "'..config.get("taiga").password..'"}'
    debug_log(body)
    local response = http.request(
      apiUrl, {
      method = "POST",
      headers = {
        Accept = "application/json",
        ["content-type"] = "application/json",
      },
      body=  body
    })
    debug_log(response)
    if response.ok then 
      return { refresh_token=response.body.refresh,  access_token=response.body.auth_token }
    else 
      TAIGA_TOKENS=nil
      return "Not OK response"
    end
  else
    return TAIGA_TOKENS
  end
end 

-- Get User stories
function getTaigaTasks(filter)
  if filter == nil then 
     filter="/userstories?project="..config.get("taiga").projectId.."&status__is_archived=false"
  --"/userstories/filters_data?assigned_users="..env["TAIGA_USER_ID"].."&project="..config.get("taiga").projectid)    
  end
  local tokens=getToken()
  debug_log(tokens)  
  local token = tokens["access_token"]
  debug_log(token)
  local apiUrl = (baseUrl .. filter)
  debug_log(apiUrl)
  local response = http.request(
    apiUrl, {
    method = "GET",
    headers = {
      Authorization = "Bearer " .. token,
      Accept = "application/json",
      ["content-type"] = "application/json",
    }
  })
  debug_log(response)
  if response.ok then 
    return response.body
  else 
    TAIGA_TOKENS=nil
    return "Not OK response"
  end
end

-- query template
templates.taigaRecurringTasks = function(t)
  local ui_url="https://tree.taiga.io/project/"..t.project_extra_info.slug.."/us/"..t.ref  
  return string.format("* [Link](" .. ui_url .. ") [%s] %s", t.status_extra_info.name, t.subject ) .. "\n"
end
```


