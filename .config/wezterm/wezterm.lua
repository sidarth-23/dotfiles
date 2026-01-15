local wezterm = require "wezterm"
local config = wezterm.config_builder()
local action = wezterm.action

-- Theme based on system preference
local function get_appearance()
  if wezterm.gui then
    return wezterm.gui.get_appearance()
  end
  return 'Dark'
end
local function scheme_for_appearance(appearance)
  if appearance:find('Dark') then
    return 'GitHub Dark'
  else
    return 'Github'
  end
end
 
 -- Appearance
config.window_background_opacity = 0.95
config.window_decorations = "RESIZE"
config.color_scheme = scheme_for_appearance(get_appearance())
config.default_cursor_style = 'BlinkingBar'
config.tab_bar_at_bottom = true

-- Graphics
config.max_fps = 120

-- Tabs
config.show_tab_index_in_tab_bar = false

-- Spawn a fish shell in login mode
config.default_prog = { '/usr/bin/fish', '-l' }
 
return config
