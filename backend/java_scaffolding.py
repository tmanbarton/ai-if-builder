from io import StringIO

from backend.database import insert_file

def initialize(session_id: str):
    write_gradle_build(session_id)
    write_game_class(session_id)

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
  private final GameMap gameMap;
  
  public Game() {
    GameMap.Builder builder = new GameMap.Builder();
    new Map().createMap(builder);
    
    gameMap = builder.build();
  }
}
""")
    insert_file(session_id, "Game.java", buf.getvalue())