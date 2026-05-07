from io import StringIO

from backend.database import insert_file

def initialize(session_id: str):
    write_gradle_build(session_id)
    write_game_class(session_id)
    write_app_class(session_id)
    write_web_socket_class(session_id)

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

def write_game_class(session_id: str):
    buf: StringIO = StringIO()
    buf.write("""package com.example;

import io.github.tmanbarton.ifengine.game.GameMap;

public class Game {
  final GameMap gameMap;
  
  public Game() {
    GameMap.Builder builder = new GameMap.Builder();
    new Map().createMap(builder);
    
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
