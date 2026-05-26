from io import StringIO

from backend.database import insert_file

def initialize(session_id: str):
    write_gradle_build(session_id)
    write_settings_gradle(session_id)
    write_game_class(session_id)
    write_app_class(session_id)
    write_web_socket_class(session_id)
    write_html(session_id)
    write_css(session_id)
    write_game_client_js(session_id)
    write_terminal_js(session_id)
    write_build_scripts(session_id)

def write_gradle_build(session_id: str):
    buf: StringIO = StringIO()
    buf.write("""plugins {
    id 'java'
    id 'application'
}

group = 'com.example'
version = '1.0'

java {
    toolchain {
        languageVersion = JavaLanguageVersion.of(24)
    }
}

repositories {
    mavenCentral()
    mavenLocal()
}

dependencies {
    implementation 'io.github.tmanbarton.ifengine:if-engine:1.0.0'
    implementation 'org.java-websocket:Java-WebSocket:1.5.4'
}

application {
    mainClass = 'com.example.App'
}

jar {
    manifest {
        attributes 'Main-Class': application.mainClass
    }
    from {
        configurations.runtimeClasspath.collect { it.isDirectory() ? it : zipTree(it) }
    }
    duplicatesStrategy = DuplicatesStrategy.EXCLUDE
}
""")
    insert_file(session_id, "build.gradle", buf.getvalue())

def write_settings_gradle(session_id: str):
    buf: StringIO = StringIO()
    buf.write("""
rootProject.name = 'game'
""")
    insert_file(session_id, "settings.gradle", buf.getvalue())

def write_game_class(session_id: str):
    buf: StringIO = StringIO()
    buf.write("""package com.example;

import io.github.tmanbarton.ifengine.game.GameMap;

public class Game {
  final GameMap gameMap;
  
  public Game() {
    GameMap.Builder builder = new GameMap.Builder();
    new Map().createMap(builder);
    new Intro().createIntro(builder);
    
    gameMap = builder.build();
  }
}
""")
    insert_file(session_id, "Game.java", buf.getvalue())

def write_app_class(session_id: str):
    buf: StringIO = StringIO()
    buf.write("""package com.example;

public class App {
  public static void main(String[] args) {
    int port = 8080;
    GameWebSocketServer server = new GameWebSocketServer(port);
    server.start();
  }
}
""")
    insert_file(session_id, "App.java", buf.getvalue())

def write_web_socket_class(session_id: str):
    buf: StringIO = StringIO()
    buf.write("""package com.example;

import io.github.tmanbarton.ifengine.game.GameEngine;
import org.java_websocket.WebSocket;
import org.java_websocket.handshake.ClientHandshake;
import org.java_websocket.server.WebSocketServer;

import java.net.InetSocketAddress;
import java.util.concurrent.ConcurrentHashMap;

public class GameWebSocketServer extends WebSocketServer {

  private final GameEngine engine;
  private static final ConcurrentHashMap<WebSocket, String> sessions = new ConcurrentHashMap<>();

  public GameWebSocketServer(int port) {
    super(new InetSocketAddress(port));
    setReuseAddr(true);
    Game game = new Game();
    engine = new GameEngine(game.gameMap);
  }

  @Override
  public void onOpen(WebSocket conn, ClientHandshake handshake) {
    String sessionId = conn.getRemoteSocketAddress().toString();
    sessions.put(conn, sessionId);
  }

  @Override
  public void onClose(WebSocket conn, int code, String reason, boolean remote) {
    System.out.println("WebSocket connection closed: " + conn.getRemoteSocketAddress());
    sessions.remove(conn);
  }

  @Override
  public void onMessage(WebSocket conn, final String message) {
    String sessionId = sessions.get(conn);
    final String response = engine.processCommand(sessionId, message);
    conn.send(response);
  }

  @Override
  public void onError(WebSocket conn, Exception ex) {
    System.err.println("Error: " + ex.getMessage());
  }

  @Override
  public void onStart() {
    System.out.println("WebSocket server started on port " + getPort());
  }
}""")
    insert_file(session_id, "GameWebSocketServer.java", buf.getvalue())

def write_html(session_id: str):
    buf: StringIO = StringIO()
    buf.write("""<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>Interactive Fiction Builder</title>
    <link rel="stylesheet" href="styles.css">
</head>
<body>
    <div id="terminal-container">
        <div id="terminal">
            <div id="terminal-output-container">
                <div id="terminal-output" class="terminal-output">
                    <p class="welcome-message">Have you played before?</p>
                    <div class="input-line">
                        <span class="prompt">&gt;</span>
                        <input type="text" class="terminal-input" id="terminal-input" autocomplete="off" spellcheck="false">
                        <div class="input-display" id="input-display">
                            <span id="input-text"></span><span class="cursor" id="cursor"></span>
                        </div>
                    </div>
                </div>
            </div>
        </div>
    </div>

    <script src="game-client.js"></script>
    <script src="terminal.js"></script>
</body>
</html>
""")
    insert_file(session_id, "index.html", buf.getvalue())

def write_css(session_id: str):
    buf: StringIO = StringIO()
    buf.write("""* {
    margin: 0;
    padding: 0;
    box-sizing: border-box;
}

html, body {
    height: 100vh;
    overflow: hidden;
    font-size: 1em;
    line-height: 1.4;
}

#terminal-container {
    width: 90%;
    height: 75vh;
    max-width: 880px;
    min-width: 320px;
    margin: auto;
    position: absolute;
    top: 50%;
    left: 50%;
    transform: translate(-50%, -50%);
    display: flex;
    flex-direction: column;
    box-shadow: 0 4px 20px rgba(0, 0, 0, 0.3);
    border: 2px solid #333;
}

#terminal {
    flex: 1;
    display: flex;
    flex-direction: column;
    height: 100%;
    overflow: hidden;
    padding: 10px;
}

#terminal-output-container {
    flex: 1;
    overflow-y: auto;
    overflow-x: hidden;
}

#terminal-output {
    min-height: 100%;
    display: flex;
    flex-direction: column;
    justify-content: flex-end;
}

.welcome-message {
    margin-bottom: 20px;
}

.terminal-line {
    margin-bottom: 5px;
    word-wrap: break-word;
    overflow-wrap: break-word;
    white-space: pre-wrap;
}

.input-line {
    display: flex;
    align-items: center;
    margin-top: 5px;
}

.terminal-input {
    border: none;
    outline: none;
    flex: 1;
    font: inherit;
}

@media (max-width: 880px) {
    #terminal-container {
        border: none;
    }
    body {
        font-size: 0.9em;
    }
}

@media (max-width: 480px) {
    body {
        font-size: 0.8em;
    }
    #terminal {
        padding: 8px;
    }
}
""")
    insert_file(session_id, "styles.css", buf.getvalue())

def write_game_client_js(session_id: str):
    buf: StringIO = StringIO()
    buf.write("""class GameClient {
    constructor() {
        this.socket = null;
        this.listeners = { connect: [], message: [], error: [] };
    }

    connect() {
        const host = window.location.hostname || 'localhost';
        const port = (host === 'localhost' || host === '127.0.0.1') ? '8080' : (window.location.port || '80');
        this.socket = new WebSocket(`ws://${host}:${port}/game`);

        this.socket.onopen = () => this.emit('connect');
        this.socket.onclose = () => this.emit('error', 'Disconnected from server.');
        this.socket.onerror = () => this.emit('error', 'Connection error.');
        this.socket.onmessage = (event) => {
            try {
                this.emit('message', JSON.parse(event.data));
            } catch {
                this.emit('message', { type: 'text', message: event.data });
            }
        };
    }

    send(message) {
        if (this.socket && this.socket.readyState === WebSocket.OPEN) {
            this.socket.send(message);
        }
    }

    on(event, callback) {
        if (this.listeners[event]) this.listeners[event].push(callback);
    }

    emit(event, data) {
        (this.listeners[event] || []).forEach(cb => cb(data));
    }
}
""")
    insert_file(session_id, "game-client.js", buf.getvalue())

def write_terminal_js(session_id: str):
    buf: StringIO = StringIO()
    buf.write("""document.addEventListener('DOMContentLoaded', () => {
    const input = document.getElementById('terminal-input');
    const output = document.getElementById('terminal-output');
    const outputContainer = document.getElementById('terminal-output-container');
    const history = [];
    let historyIndex = -1;

    const client = new GameClient();

    client.on('message', (data) => {
        addOutput(data.message || JSON.stringify(data));
    });

    client.on('error', (msg) => {
        addOutput(msg, 'error-line');
    });

    client.connect();

    document.getElementById('terminal-container').addEventListener('click', () => {
        input.focus();
    });

    input.addEventListener('keydown', (e) => {
        if (e.key === 'Enter') {
            const command = input.value.trim();
            if (command) {
                history.push(command);
                historyIndex = history.length;
                addOutput('> ' + command, 'command-line');
                client.send(command);
            }
            input.value = '';
        } else if (e.key === 'ArrowUp') {
            e.preventDefault();
            if (historyIndex > 0) input.value = history[--historyIndex];
        } else if (e.key === 'ArrowDown') {
            e.preventDefault();
            if (historyIndex < history.length - 1) input.value = history[++historyIndex];
            else { historyIndex = history.length; input.value = ''; }
        }
    });

    function addOutput(text, className = 'output-line') {
        const inputLine = output.querySelector('.input-line');
        text.split('\\n').forEach(part => {
            const line = document.createElement('div');
            line.className = className;
            line.textContent = part;
            output.insertBefore(line, inputLine);
        });
        outputContainer.scrollTop = outputContainer.scrollHeight;
    }
});
""")

    insert_file(session_id, "terminal.js", buf.getvalue())

def write_build_scripts(session_id: str):
    bash_buf: StringIO = StringIO()
    bash_buf.write("""
    #!/usr/bin/env bash
set -e

# Initialize Gradle wrapper if not present
if [ ! -f "gradlew" ]; then
  gradle wrapper
fi

# Build and run
./gradlew run""")
    insert_file(session_id, "run.sh", bash_buf.getvalue())

    bat_buf: StringIO = StringIO()
    bat_buf.write("""@echo off
if not exist gradlew.bat (
    gradle wrapper
)
gradlew.bat run""")
    insert_file(session_id, "run.bat", bat_buf.getvalue())