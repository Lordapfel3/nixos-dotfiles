{ config, lib, pkgs, ... }:

let
  home-manager = builtins.fetchTarball "https://github.com/nix-community/home-manager/archive/release-25.11.tar.gz";
in
{
  imports = [
    ./hardware-configuration.nix
    (import "${home-manager}/nixos")
  ];

  hardware.bluetooth.enable = true;
  hardware.bluetooth.powerOnBoot = true;
  hardware.enableAllFirmware = true;

  home-manager.useUserPackages = true;
  home-manager.useGlobalPkgs = true;
  home-manager.backupFileExtension = "backup";
  home-manager.users.leon = import ./home.nix;
  
  boot.loader.systemd-boot.enable = true;
  boot.loader.efi.canTouchEfiVariables = true;

  networking.hostName = "nix";
  networking.networkmanager.enable = true;

  time.timeZone = "Europe/Berlin";
  i18n.defaultLocale = "de_DE.UTF-8";
  console.keyMap = "de";

  services.xserver = {
    enable = true;
    xkb.layout = "de";
    xkb.variant = "";
    windowManager.qtile.enable = true;
    displayManager.sessionCommands = ''
      xset r rate 200 35 &
    '';
  };

  services.picom = {
    enable = true;
    backend = "glx";
    fade = true;
  };

  services.blueman.enable = true;

  services.libinput = {
    enable = true;
    touchpad = {
      tapping = true;
      naturalScrolling = true;
      disableWhileTyping = true;
    };
  };

  security.rtkit.enable = true;
  services.pipewire = {
    enable = true;
    alsa.enable = true;
    alsa.support32Bit = true;
    pulse.enable = true;
  };

  users.users.leon = {
    isNormalUser = true;
    extraGroups = [ "wheel" "networkmanager" "video" "audio" ];
    packages = with pkgs; [
      tree
    ];
  };

  programs.firefox.enable = true;
  nixpkgs.config.allowUnfree = true;

  environment.systemPackages = with pkgs; [
    vim
    neovim
    gedit
    vscode
    wget
    git
    btop
    pfetch
    alacritty
    pcmanfm
    feh
    rofi
    dunst
    libnotify
    vlc
    xournalpp
    inkscape-with-extensions
    kdePackages.okular
    brightnessctl
    pamixer
    pavucontrol
    networkmanagerapplet
    blueman
    intel-compute-runtime
    steam
    flameshot
  ];

  fonts.packages = with pkgs; [
    jetbrains-mono
    nerd-fonts.jetbrains-mono
  ];

  system.stateVersion = "25.11";
}
