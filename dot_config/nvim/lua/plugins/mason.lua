return {
  {
    "williamboman/mason.nvim",
    opts = function(_, opts)
      opts.ensure_installed = opts.ensure_installed or {}

      vim.list_extend(opts.ensure_installed, {
        -- LSPs
        "angular-language-server",
        "astro-language-server",
        "bash-language-server",
        "biome",
        "cmake-language-server",
        "css-variables-language-server",
        "cssmodules-language-server",
        "deno",
        "docker-compose-language-service",
        "docker-language-server",
        "dockerfile-language-server",
        "eslint-lsp",
        "gh-actions-language-server",
        "glsl_analyzer",
        "gopls",
        "helm-ls",
        "html-lsp",
        "json-lsp",
        "lua-language-server",
        "marksman",
        "neocmakelsp",
        "oxlint",
        "pyright",
        "rust-analyzer",

        -- Debug adapters
        "bash-debug-adapter",
        "go-debug-adapter",
        "js-debug-adapter",

        -- Linters
        "cmakelint",
        "commitlint",
        "dotenv-linter",
        "golangci-lint",
        "hadolint",
        "markdownlint-cli2",

        -- Formatters
        "gitui",
        "gofumpt",
        "goimports",
        "goimports-reviser",
        "markdown-toc",
        "pgformatter",
        "prettierd",
        "shfmt",
        "stylua",

        -- Extra tools
        "codeql",
        "jsonlint",
        "pylint",
        "ruff",
      })
    end,
  },
}
