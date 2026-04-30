return {
  "nvim-tree/nvim-tree.lua",
  dependencies = { "nvim-tree/nvim-web-devicons" },
  keys = {
    { "<leader>ee", "<cmd>NvimTreeToggle<CR>", desc = "Toggle file explorer" },
    { "<leader>ef", "<cmd>NvimTreeFindFile<CR>", desc = "Focus on current file in file explorer" },
    { "<leader>ec", "<cmd>NvimTreeCollapse<CR>", desc = "Collapse all in file explorer" },
    { "<leader>er", "<cmd>NvimTreeRefresh<CR>", desc = "Refresh file explorer" },
  },
  config = function()
    local function my_on_attach(bufnr)
      local api = require("nvim-tree.api")

      -- Generate options for key mappings
      local function opts(desc)
        return { desc = "nvim-tree: " .. desc, buffer = bufnr, noremap = true, silent = true, nowait = true }
      end

      -- Default mappings
      api.config.mappings.default_on_attach(bufnr)

      -- Custom mappings
      local keymap = vim.keymap.set
      keymap("n", "h", api.node.navigate.parent_close, opts("Close Parent"))
      keymap("n", "l", api.node.open.no_window_picker, opts("Open File No Window Picker"))
      keymap("n", "<C-v>", api.node.open.horizontal, opts("Open: Horizontal Split"))
      keymap("n", "<C-h>", api.node.open.vertical, opts("Open: Vertical Split"))
    end

    -- Nvim-tree setup
    require("nvim-tree").setup({
      sort_by = "case_sensitive", -- Case-sensitive sorting
      view = {
        width = 40,
        relativenumber = false,
      },
      renderer = {
        indent_markers = { enable = false },
        icons = {
          glyphs = {
            folder = {
              arrow_closed = "", -- Icon for closed folder
              arrow_open = "", -- Icon for open folder
            },
          },
        },
      },
      filters = { custom = { ".DS_Store" } },
      git = { ignore = false },
      on_attach = my_on_attach,
    })
  end,
}
