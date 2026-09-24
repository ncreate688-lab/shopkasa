const fs = require('fs');
const path = require('path');

const projectDir = path.join(__dirname, 'MpesaListenerApp');

const dirs = [
  'app/src/main/java/com/softbuild/mpesalistener',
  'app/src/main/res/layout',
  'app/src/main/res/values',
];

dirs.forEach(d => fs.mkdirSync(path.join(projectDir, d), { recursive: true }));

const files = {
  'build.gradle': `
buildscript {
    ext.kotlin_version = "1.8.0"
    repositories {
        google()
        mavenCentral()
    }
    dependencies {
        classpath "com.android.tools.build:gradle:8.0.2"
        classpath "org.jetbrains.kotlin:kotlin-gradle-plugin:$kotlin_version"
    }
}
allprojects {
    repositories {
        google()
        mavenCentral()
    }
}
`,
  'settings.gradle': `
pluginManagement {
    repositories {
        google()
        mavenCentral()
        gradlePluginPortal()
    }
}
dependencyResolutionManagement {
    repositoriesMode.set(RepositoriesMode.FAIL_ON_PROJECT_REPOS)
    repositories {
        google()
        mavenCentral()
    }
}
rootProject.name = "MpesaListenerApp"
include ':app'
`,
  'app/build.gradle': `
plugins {
    id 'com.android.application'
    id 'org.jetbrains.kotlin.android'
}
android {
    namespace 'com.softbuild.mpesalistener'
    compileSdk 33
    defaultConfig {
        applicationId "com.softbuild.mpesalistener"
        minSdk 24
        targetSdk 33
        versionCode 1
        versionName "1.0"
    }
    buildTypes {
        release {
            minifyEnabled false
            proguardFiles getDefaultProguardFile('proguard-android-optimize.txt'), 'proguard-rules.pro'
        }
    }
    compileOptions {
        sourceCompatibility JavaVersion.VERSION_1_8
        targetCompatibility JavaVersion.VERSION_1_8
    }
    kotlinOptions {
        jvmTarget = '1.8'
    }
}
dependencies {
    implementation 'androidx.core:core-ktx:1.10.1'
    implementation 'androidx.appcompat:appcompat:1.6.1'
    implementation 'com.google.android.material:material:1.9.0'
    implementation 'androidx.constraintlayout:constraintlayout:2.1.4'
    implementation 'com.squareup.okhttp3:okhttp:4.10.0'
}
`,
  'app/src/main/AndroidManifest.xml': `<?xml version="1.0" encoding="utf-8"?>
<manifest xmlns:android="http://schemas.android.com/apk/res/android"
    package="com.softbuild.mpesalistener">

    <uses-permission android:name="android.permission.INTERNET" />
    <uses-permission android:name="android.permission.FOREGROUND_SERVICE" />

    <application
        android:allowBackup="true"
        android:icon="@mipmap/ic_launcher"
        android:label="M-Pesa Auto Verify"
        android:roundIcon="@mipmap/ic_launcher_round"
        android:supportsRtl="true"
        android:theme="@style/Theme.AppCompat.Light.DarkActionBar">

        <activity
            android:name=".MainActivity"
            android:exported="true">
            <intent-filter>
                <action android:name="android.intent.action.MAIN" />
                <category android:name="android.intent.category.LAUNCHER" />
            </intent-filter>
        </activity>
    </application>
</manifest>
`,
  'app/src/main/res/layout/activity_main.xml': `<?xml version="1.0" encoding="utf-8"?>
<LinearLayout xmlns:android="http://schemas.android.com/apk/res/android"
    android:layout_width="match_parent"
    android:layout_height="match_parent"
    android:orientation="vertical"
    android:padding="16dp">

    <TextView
        android:layout_width="match_parent"
        android:layout_height="wrap_content"
        android:text="M-Pesa Auto-Verify Setup"
        android:textSize="24sp"
        android:textStyle="bold"
        android:layout_marginBottom="16dp"/>

    <EditText
        android:id="@+id/etDbUrl"
        android:layout_width="match_parent"
        android:layout_height="wrap_content"
        android:hint="Turso Database URL (https://...)"
        android:inputType="textUri"/>

    <EditText
        android:id="@+id/etDbToken"
        android:layout_width="match_parent"
        android:layout_height="wrap_content"
        android:hint="Turso Auth Token"
        android:inputType="textPassword"/>

    <Button
        android:id="@+id/btnSave"
        android:layout_width="match_parent"
        android:layout_height="wrap_content"
        android:text="Save Settings"
        android:layout_marginTop="16dp"/>
        
    <TextView
        android:id="@+id/tvStatus"
        android:layout_width="match_parent"
        android:layout_height="wrap_content"
        android:layout_marginTop="16dp"
        android:text="Status: Ready"/>

</LinearLayout>
`,
  'app/src/main/java/com/softbuild/mpesalistener/MainActivity.kt': `package com.softbuild.mpesalistener

import android.Manifest
import android.content.Context
import android.content.pm.PackageManager
import android.os.Bundle
import android.widget.Button
import android.widget.EditText
import android.widget.TextView
import android.widget.Toast
import androidx.appcompat.app.AppCompatActivity
import androidx.core.app.ActivityCompat
import androidx.core.content.ContextCompat

class MainActivity : AppCompatActivity() {

    override fun onCreate(savedInstanceState: Bundle?) {
        super.onCreate(savedInstanceState)
        setContentView(R.layout.activity_main)

        val etDbUrl = findViewById<EditText>(R.id.etDbUrl)
        val etDbToken = findViewById<EditText>(R.id.etDbToken)
        val btnSave = findViewById<Button>(R.id.btnSave)
        val tvStatus = findViewById<TextView>(R.id.tvStatus)

        val prefs = getSharedPreferences("AppPrefs", Context.MODE_PRIVATE)
        etDbUrl.setText(prefs.getString("TURSO_URL", ""))
        etDbToken.setText(prefs.getString("TURSO_TOKEN", ""))

        btnSave.setOnClickListener {
            val editor = prefs.edit()
            editor.putString("TURSO_URL", etDbUrl.text.toString().trim())
            editor.putString("TURSO_TOKEN", etDbToken.text.toString().trim())
            editor.apply()
            Toast.makeText(this, "Settings Saved!", Toast.LENGTH_SHORT).show()
        }
    }
}`
};

for (const [filePath, content] of Object.entries(files)) {
  fs.writeFileSync(path.join(projectDir, filePath), content);
}
console.log('Android project generated at ' + projectDir);
