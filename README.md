# dotfiles

Portable Codex and shared agent configuration.

## Restore

```sh
git clone https://github.com/francescoalbanese/dotfiles.git ~/dotfiles
brew install stow
cd ~/dotfiles
cp codex/.codex/config.toml.example codex/.codex/config.toml
stow codex agents
```

`codex/.codex/config.toml` is ignored because Codex writes local runtime state into it. Keep portable defaults in `config.toml.example`.

## Packages

- `codex`: Codex config, hooks, agents, and rules
- `agents`: shared agent skills
