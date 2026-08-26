plugins {
    id("com.android.application")
    id("org.jetbrains.kotlin.android")
}

android {
    namespace = "com.example.fallsensorapp"
    compileSdk = 34

    defaultConfig {
        applicationId = "com.example.fallsensorapp"
        minSdk = 24
        targetSdk = 34
        versionCode = 1
        versionName = "1.0"
        vectorDrawables {
            useSupportLibrary = true
        }
    }

    flavorDimensions += "sensor"
    productFlavors {
        create("ld2410") {
            dimension = "sensor"
            applicationIdSuffix = ".ld2410"
            versionNameSuffix = "-LD2410"
            resValue("string", "app_name", "Fall Sensor LD2410")
            buildConfigField("String", "BLE_NAME_PREFIX", "\"Fall_Sensor_LD2410\"")
            buildConfigField("String", "SENSOR_TYPE", "\"LD2410\"")
        }
        create("c1001") {
            dimension = "sensor"
            applicationIdSuffix = ".c1001"
            versionNameSuffix = "-C1001"
            resValue("string", "app_name", "Fall Sensor C1001")
            buildConfigField("String", "BLE_NAME_PREFIX", "\"Fall_Sensor_C1001\"")
            buildConfigField("String", "SENSOR_TYPE", "\"C1001\"")
        }
    }

    buildTypes {
        release {
            isMinifyEnabled = false
            proguardFiles(getDefaultProguardFile("proguard-android-optimize.txt"), "proguard-rules.pro")
            signingConfig = signingConfigs.getByName("debug")
        }
    }
    compileOptions {
        sourceCompatibility = JavaVersion.VERSION_17
        targetCompatibility = JavaVersion.VERSION_17
    }
    kotlinOptions {
        jvmTarget = "17"
    }
    buildFeatures {
        compose = true
        buildConfig = true
    }
    composeOptions {
        kotlinCompilerExtensionVersion = "1.5.1"
    }
}

dependencies {
    implementation("androidx.core:core-ktx:1.12.0")
    implementation("androidx.lifecycle:lifecycle-runtime-ktx:2.7.0")
    implementation("androidx.activity:activity-compose:1.8.2")
    implementation(platform("androidx.compose:compose-bom:2023.10.01"))
    implementation("androidx.compose.ui:ui")
    implementation("androidx.compose.ui:ui-graphics")
    implementation("androidx.compose.ui:ui-tooling-preview")
    implementation("androidx.compose.material3:material3")
    implementation("androidx.lifecycle:lifecycle-viewmodel-compose:2.7.0")
    
    implementation("org.jetbrains.kotlinx:kotlinx-coroutines-android:1.7.3")
}
