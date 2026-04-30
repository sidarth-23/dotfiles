return {
  {
    "projekt0n/github-nvim-theme",
    name = "github-theme",
    lazy = false,
    priority = 1000,
    config = function()
      require("github-theme").setup({
        options = {
          transparent = true,
        },
      })
      vim.cmd("colorscheme github_dark_default")
    end,
  },
  {
    "catppuccin/nvim",
    name = "catppuccin",
    config = function()
      require("catppuccin").setup({
        transparent_background = true,
        float = {
          transparent = true,
          solid = false,
        },
      })
      -- You can switch manually with :colorscheme catppuccin
    end,
  },
  {
    "folke/tokyonight.nvim",
    name = "tokyonight",
    config = function()
      require("tokyonight").setup({
        transparent = true,
      })
      -- You can switch manually with :colorscheme tokyonight
    end,
  },
  { "ellisonleao/gruvbox.nvim" },
}
