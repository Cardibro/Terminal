{ pkgs, lib, config, inputs, ... }:

{
  languages.python = {
    enable = true;
  };

  # https://devenv.sh/git-hooks/
  # git-hooks.hooks.shellcheck.enable = true;
}
