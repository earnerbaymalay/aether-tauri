#!/bin/bash
# 🌌 Aether-Tauri Launcher

# Ensure Ollama is running
if ! pgrep -x "ollama" > /dev/null; then
    echo "Starting Ollama..."
    if command -v systemctl &>/dev/null; then
        sudo systemctl start ollama
    else
        ollama serve &
    fi
    sleep 5
fi

# Compatibility Setup for Modern Linux (WebKitGTK 4.1 support)
if [ "$(uname)" == "Linux" ]; then
    echo "Setting up Linux compatibility environment..."
    mkdir -p pkgconfig lib
    
    # Symlink pkg-config files if missing
    [ ! -f pkgconfig/javascriptcoregtk-4.0.pc ] && ln -s /usr/lib/x86_64-linux-gnu/pkgconfig/javascriptcoregtk-4.1.pc pkgconfig/javascriptcoregtk-4.0.pc
    [ ! -f pkgconfig/libsoup-2.4.pc ] && ln -s /usr/lib/x86_64-linux-gnu/pkgconfig/libsoup-3.0.pc pkgconfig/libsoup-2.4.pc
    [ ! -f pkgconfig/webkit2gtk-4.0.pc ] && ln -s /usr/lib/x86_64-linux-gnu/pkgconfig/webkit2gtk-4.1.pc pkgconfig/webkit2gtk-4.0.pc
    [ ! -f pkgconfig/webkit2gtk-web-extension-4.0.pc ] && ln -s /usr/lib/x86_64-linux-gnu/pkgconfig/webkit2gtk-web-extension-4.1.pc pkgconfig/webkit2gtk-web-extension-4.0.pc
    
    # Symlink library files if missing
    [ ! -f lib/libwebkit2gtk-4.0.so ] && ln -s /usr/lib/x86_64-linux-gnu/libwebkit2gtk-4.1.so lib/libwebkit2gtk-4.0.so
    [ ! -f lib/libjavascriptcoregtk-4.0.so ] && ln -s /usr/lib/x86_64-linux-gnu/libjavascriptcoregtk-4.1.so lib/libjavascriptcoregtk-4.0.so
    [ ! -f lib/libsoup-2.4.so ] && ln -s /usr/lib/x86_64-linux-gnu/libsoup-3.0.so lib/libsoup-2.4.so
    
    export PKG_CONFIG_PATH="$PWD/pkgconfig:$PKG_CONFIG_PATH"
    export LIBRARY_PATH="$PWD/lib:$LIBRARY_PATH"
    export LD_LIBRARY_PATH="$PWD/lib:$LD_LIBRARY_PATH"
    export WRY_USE_4_1=1
fi

# Launch Tauri App in Dev Mode
echo "Launching Aether Neural Interface..."
npm run tauri dev
