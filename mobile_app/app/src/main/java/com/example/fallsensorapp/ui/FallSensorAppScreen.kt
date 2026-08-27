package com.example.fallsensorapp.ui

import androidx.compose.animation.animateColorAsState
import androidx.compose.animation.core.tween
import androidx.compose.foundation.background
import androidx.compose.foundation.border
import androidx.compose.foundation.layout.*
import androidx.compose.foundation.lazy.LazyColumn
import androidx.compose.foundation.lazy.items
import androidx.compose.foundation.lazy.rememberLazyListState
import androidx.compose.foundation.rememberScrollState
import androidx.compose.foundation.shape.CircleShape
import androidx.compose.foundation.shape.RoundedCornerShape
import androidx.compose.foundation.text.KeyboardOptions
import androidx.compose.foundation.verticalScroll
import androidx.compose.material3.*
import androidx.compose.runtime.*
import androidx.compose.ui.Alignment
import androidx.compose.ui.Modifier
import androidx.compose.ui.draw.clip
import androidx.compose.ui.draw.shadow
import androidx.compose.ui.graphics.Color
import androidx.compose.ui.text.font.FontFamily
import androidx.compose.ui.text.font.FontWeight
import androidx.compose.ui.text.input.KeyboardType
import androidx.compose.ui.text.style.TextAlign
import androidx.compose.ui.unit.dp
import androidx.compose.ui.unit.sp
import com.example.fallsensorapp.parser.SensorState
import com.example.fallsensorapp.viewmodel.LedState
import com.example.fallsensorapp.viewmodel.MainViewModel
import com.example.fallsensorapp.viewmodel.SensorSettings
import com.example.fallsensorapp.ui.theme.*

@OptIn(ExperimentalMaterial3Api::class)
@Composable
fun FallSensorAppScreen(viewModel: MainViewModel) {
    val uiState by viewModel.uiState.collectAsState()
    val connectionStatus by viewModel.connectionStatus.collectAsState()
    val logMessages by viewModel.messageLog.collectAsState()
    val ledState by viewModel.ledState.collectAsState()
    val distance by viewModel.distance.collectAsState()
    val batteryVoltage by viewModel.batteryVoltage.collectAsState()
    val batteryPercent by viewModel.batteryPercent.collectAsState()
    val pin25Raw by viewModel.pin25Raw.collectAsState()
    val pin26Raw by viewModel.pin26Raw.collectAsState()
    val uartPresence by viewModel.uartPresence.collectAsState()
    val otaIp by viewModel.otaIp.collectAsState()
    val isMoving by viewModel.isMoving.collectAsState()
    val isLoggingEnabled by viewModel.isLoggingEnabled.collectAsState()
    val uptimeMs by viewModel.uptimeMs.collectAsState()
    val estimatedDays by viewModel.estimatedDaysRemaining.collectAsState()
    val lowBatteryAlert by viewModel.lowBatteryAlert.collectAsState()
    val settings by viewModel.settings.collectAsState()

    var showSettingsDialog by remember { mutableStateOf(false) }

    val isDisconnected = connectionStatus == "Disconnected"

    Scaffold(
        topBar = {
            TopAppBar(
                title = {
                    Row(verticalAlignment = Alignment.CenterVertically) {
                        Text("Fall Sensor", fontWeight = FontWeight.Bold)
                        if (batteryVoltage != null) {
                            Spacer(modifier = Modifier.width(8.dp))
                            val battColor = when {
                                (batteryPercent ?: 100) <= 10 -> Color(0xFFFF1744)
                                (batteryPercent ?: 100) <= 20 -> Color(0xFFFFAB00)
                                else -> Color(0xFF81C784)
                            }
                            Surface(
                                color = Color(0xFF37474F),
                                shape = RoundedCornerShape(12.dp)
                            ) {
                                Text(
                                    text = "🔋 ${batteryPercent ?: "--"}% (${String.format("%.2f", batteryVoltage)}V)",
                                    color = battColor,
                                    fontSize = 11.sp,
                                    fontWeight = FontWeight.Bold,
                                    modifier = Modifier.padding(horizontal = 6.dp, vertical = 3.dp)
                                )
                            }
                        }
                    }
                },
                actions = {
                    // Settings gear button
                    IconButton(onClick = { showSettingsDialog = true }) {
                        Text("⚙", fontSize = 18.sp, color = Color.White)
                    }
                    Box(
                        modifier = Modifier
                            .padding(end = 4.dp)
                            .size(10.dp)
                            .clip(CircleShape)
                            .background(
                                when (connectionStatus) {
                                    "Connected" -> Color.Green
                                    "Scanning...", "Connecting...", "Retrying..." -> Color.Yellow
                                    else -> Color.Red
                                }
                            )
                    )
                    Text(
                        text = connectionStatus,
                        color = MaterialTheme.colorScheme.onPrimary,
                        fontSize = 11.sp,
                        modifier = Modifier.padding(end = 12.dp)
                    )
                },
                colors = TopAppBarDefaults.topAppBarColors(
                    containerColor = MaterialTheme.colorScheme.primary,
                    titleContentColor = MaterialTheme.colorScheme.onPrimary
                )
            )
        }
    ) { padding ->
        Box(modifier = Modifier.fillMaxSize().padding(padding)) {
            Column(
                modifier = Modifier
                    .fillMaxSize()
                    .padding(horizontal = 16.dp, vertical = 10.dp)
            ) {
                // ── LOW BATTERY ALERT ──
                if (lowBatteryAlert && batteryPercent != null) {
                    Card(
                        modifier = Modifier.fillMaxWidth(),
                        colors = CardDefaults.cardColors(
                            containerColor = if ((batteryPercent ?: 100) <= 10) Color(0xFFB71C1C) else Color(0xFFE65100)
                        ),
                        shape = RoundedCornerShape(10.dp)
                    ) {
                        Text(
                            text = if ((batteryPercent ?: 100) <= 10) "⚠ CRITICAL BATTERY! Charge immediately."
                                   else "🔋 Low Battery ($batteryPercent%). Please charge soon.",
                            color = Color.White,
                            fontSize = 12.sp,
                            fontWeight = FontWeight.Bold,
                            modifier = Modifier.padding(10.dp),
                            textAlign = TextAlign.Center
                        )
                    }
                    Spacer(modifier = Modifier.height(6.dp))
                }

                // ── 1. STATUS CARD ──
                StatusCard(
                    state = uiState.state,
                    rawText = uiState.rawText,
                    isFall = ledState.fallDetected,
                    onDismissFall = { viewModel.dismissFallAlarm() }
                )

                Spacer(modifier = Modifier.height(6.dp))

                // ── 2. UPTIME & BATTERY PREDICTION BAR ──
                Card(
                    modifier = Modifier.fillMaxWidth(),
                    colors = CardDefaults.cardColors(containerColor = Color(0xFF263238)),
                    shape = RoundedCornerShape(10.dp)
                ) {
                    Row(
                        modifier = Modifier
                            .fillMaxWidth()
                            .padding(horizontal = 12.dp, vertical = 6.dp),
                        horizontalArrangement = Arrangement.SpaceBetween,
                        verticalAlignment = Alignment.CenterVertically
                    ) {
                        Column {
                            Text(
                                text = "Uptime: ${viewModel.formatUptime(uptimeMs)}",
                                color = Color(0xFF80CBC4),
                                fontSize = 11.sp,
                                fontFamily = FontFamily.Monospace
                            )
                            Text(
                                text = "Pin25: ${pin25Raw ?: "--"} | Pin26: ${pin26Raw ?: "--"} | UART: ${if (uartPresence) "✓" else "✗"}",
                                color = Color(0xFF78909C),
                                fontSize = 10.sp,
                                fontFamily = FontFamily.Monospace
                            )
                        }
                        Column(horizontalAlignment = Alignment.End) {
                            Text(
                                text = if (estimatedDays != null && estimatedDays!! < 30f) "~${String.format("%.1f", estimatedDays)} days left"
                                       else if (estimatedDays != null) ">30 days left"
                                       else "Estimating...",
                                color = Color(0xFFFFAB40),
                                fontSize = 11.sp,
                                fontWeight = FontWeight.Bold
                            )
                            Button(
                                onClick = { viewModel.triggerOta() },
                                colors = ButtonDefaults.buttonColors(containerColor = Color(0xFF0288D1)),
                                contentPadding = PaddingValues(horizontal = 8.dp, vertical = 0.dp),
                                shape = RoundedCornerShape(8.dp),
                                modifier = Modifier.height(26.dp)
                            ) {
                                Text("OTA", fontSize = 10.sp, color = Color.White)
                            }
                        }
                    }
                }

                if (otaIp != null) {
                    Spacer(modifier = Modifier.height(4.dp))
                    Card(
                        modifier = Modifier.fillMaxWidth(),
                        colors = CardDefaults.cardColors(containerColor = Color(0xFF1B5E20)),
                        shape = RoundedCornerShape(8.dp)
                    ) {
                        Text(
                            text = "🌐 OTA Active at IP: $otaIp",
                            color = Color.White,
                            fontSize = 12.sp,
                            fontWeight = FontWeight.Bold,
                            modifier = Modifier.padding(8.dp),
                            textAlign = TextAlign.Center
                        )
                    }
                }

                Spacer(modifier = Modifier.height(8.dp))

                // ── 3. LED INDICATOR ROW ──
                LedIndicatorRow(ledState)

                Spacer(modifier = Modifier.height(10.dp))

                // ── 4. TELEMETRY ROW ──
                Row(
                    modifier = Modifier.fillMaxWidth(),
                    horizontalArrangement = Arrangement.spacedBy(10.dp)
                ) {
                    TelemetryCard(
                        title = "Distance",
                        value = distance?.toString() ?: "--",
                        unit = if (distance != null) "cm" else "",
                        modifier = Modifier.weight(1f)
                    )
                    TelemetryCard(
                        title = "Movement",
                        value = if (isMoving) "Moving" else "Still",
                        unit = "",
                        modifier = Modifier.weight(1f)
                    )
                    TelemetryCard(
                        title = "Battery",
                        value = if (batteryPercent != null) "$batteryPercent" else "--",
                        unit = if (batteryPercent != null) "%" else "",
                        modifier = Modifier.weight(1f)
                    )
                }

                Spacer(modifier = Modifier.height(10.dp))

                // ── 5. LOGGING SWITCH + LOG FEED ──
                Row(
                    modifier = Modifier.fillMaxWidth(),
                    verticalAlignment = Alignment.CenterVertically,
                    horizontalArrangement = Arrangement.SpaceBetween
                ) {
                    Text(
                        "Live Logging",
                        style = MaterialTheme.typography.titleMedium,
                        fontWeight = FontWeight.Bold
                    )
                    Switch(
                        checked = isLoggingEnabled,
                        onCheckedChange = { viewModel.toggleLogging(it) },
                        colors = SwitchDefaults.colors(
                            checkedThumbColor = NormalGreen,
                            checkedTrackColor = NormalGreen.copy(alpha = 0.4f)
                        )
                    )
                }

                Spacer(modifier = Modifier.height(6.dp))

                Card(
                    modifier = Modifier.fillMaxSize(),
                    colors = CardDefaults.cardColors(containerColor = CardDark),
                    shape = RoundedCornerShape(12.dp)
                ) {
                    if (logMessages.isNotEmpty()) {
                        val listState = rememberLazyListState()
                        LaunchedEffect(logMessages.size) {
                            if (logMessages.isNotEmpty()) {
                                listState.animateScrollToItem(0)
                            }
                        }
                        LazyColumn(
                            state = listState,
                            modifier = Modifier
                                .fillMaxSize()
                                .padding(10.dp)
                        ) {
                            items(logMessages.reversed()) { msg ->
                                val lineColor = when {
                                    msg.contains("ALERT") || msg.contains("FALL DETECTED") -> LedFallRed
                                    msg.contains("[WARN]") -> LedPirYellow
                                    msg.contains("[SYS]") -> Color(0xFF64B5F6)
                                    msg.contains("[RADAR]") -> LedRadarGreen
                                    msg.contains("[OTA]") -> Color(0xFFFFB74D)
                                    msg.contains("Battery") -> Color(0xFF81C784)
                                    else -> TerminalGreen
                                }
                                Text(
                                    text = "> $msg",
                                    color = lineColor,
                                    fontSize = 11.sp,
                                    fontFamily = FontFamily.Monospace,
                                    modifier = Modifier.padding(vertical = 1.dp)
                                )
                            }
                        }
                    } else {
                        Box(
                            modifier = Modifier.fillMaxSize(),
                            contentAlignment = Alignment.Center
                        ) {
                            Column(horizontalAlignment = Alignment.CenterHorizontally) {
                                Text("📡", fontSize = 36.sp)
                                Spacer(modifier = Modifier.height(6.dp))
                                Text(
                                    if (isLoggingEnabled) "Waiting for data..." else "Logging Disabled",
                                    color = Color.Gray,
                                    style = MaterialTheme.typography.titleMedium
                                )
                                Text(
                                    "Fall alerts always come through",
                                    color = Color.DarkGray,
                                    style = MaterialTheme.typography.bodySmall
                                )
                            }
                        }
                    }
                }
            }

            // Grey overlay when disconnected
            if (isDisconnected) {
                Box(
                    modifier = Modifier
                        .fillMaxSize()
                        .background(Color.Black.copy(alpha = 0.6f)),
                    contentAlignment = Alignment.Center
                ) {
                    Card(
                        colors = CardDefaults.cardColors(containerColor = Color(0xFF263238)),
                        shape = RoundedCornerShape(16.dp),
                        elevation = CardDefaults.cardElevation(defaultElevation = 8.dp)
                    ) {
                        Column(
                            modifier = Modifier.padding(24.dp),
                            horizontalAlignment = Alignment.CenterHorizontally
                        ) {
                            Text("📡", fontSize = 48.sp)
                            Spacer(modifier = Modifier.height(12.dp))
                            Text(
                                "No Sensor Connected",
                                color = Color.White,
                                style = MaterialTheme.typography.titleLarge,
                                fontWeight = FontWeight.Bold
                            )
                            Spacer(modifier = Modifier.height(8.dp))
                            Text(
                                "Make sure your Fall Sensor is powered on\nand Bluetooth is enabled on this phone.",
                                color = Color(0xFF90A4AE),
                                style = MaterialTheme.typography.bodyMedium,
                                textAlign = TextAlign.Center
                            )
                            Spacer(modifier = Modifier.height(16.dp))
                            Button(
                                onClick = { viewModel.startScanning() },
                                colors = ButtonDefaults.buttonColors(containerColor = Color(0xFF0288D1)),
                                shape = RoundedCornerShape(12.dp)
                            ) {
                                Text("Retry Scan", fontWeight = FontWeight.Bold)
                            }
                        }
                    }
                }
            }
        }
    }

    // ── SETTINGS DIALOG ──
    if (showSettingsDialog) {
        SettingsDialog(
            currentSettings = settings,
            onDismiss = { showSettingsDialog = false },
            onSave = { newSettings ->
                viewModel.updateSettings(newSettings)
                showSettingsDialog = false
            }
        )
    }
}

// ═══════════════════════════════════════════
// SETTINGS DIALOG
// ═══════════════════════════════════════════

@Composable
fun SettingsDialog(
    currentSettings: SensorSettings,
    onDismiss: () -> Unit,
    onSave: (SensorSettings) -> Unit
) {
    var battCapacity by remember { mutableStateOf(currentSettings.batteryCapacityMah.toString()) }
    var lowThreshold by remember { mutableStateOf(currentSettings.lowBatteryThresholdPercent.toString()) }
    var critThreshold by remember { mutableStateOf(currentSettings.criticalBatteryThresholdPercent.toString()) }
    var pirDuration by remember { mutableStateOf((currentSettings.pirLedDurationMs / 1000).toString()) }
    var micDuration by remember { mutableStateOf((currentSettings.micLedDurationMs / 1000).toString()) }
    var maxV by remember { mutableStateOf(currentSettings.maxVoltage.toString()) }
    var minV by remember { mutableStateOf(currentSettings.minVoltage.toString()) }
    var roomHeight by remember { mutableStateOf(currentSettings.roomHeightFeet.toString()) }

    AlertDialog(
        onDismissRequest = onDismiss,
        title = { Text("Sensor Settings", fontWeight = FontWeight.Bold) },
        text = {
            Column(
                modifier = Modifier.verticalScroll(rememberScrollState()),
                verticalArrangement = Arrangement.spacedBy(10.dp)
            ) {
                SettingsField("Ceiling / Room Height (feet)", roomHeight) { roomHeight = it }
                SettingsField("Battery Capacity (mAh)", battCapacity) { battCapacity = it }
                SettingsField("Low Battery Alert (%)", lowThreshold) { lowThreshold = it }
                SettingsField("Critical Battery Alert (%)", critThreshold) { critThreshold = it }
                SettingsField("PIR LED Duration (seconds)", pirDuration) { pirDuration = it }
                SettingsField("MIC LED Duration (seconds)", micDuration) { micDuration = it }
                SettingsField("Max Battery Voltage (V)", maxV) { maxV = it }
                SettingsField("Min Battery Voltage (V)", minV) { minV = it }
            }
        },
        confirmButton = {
            Button(
                onClick = {
                    onSave(SensorSettings(
                        batteryCapacityMah = battCapacity.toIntOrNull() ?: 2000,
                        lowBatteryThresholdPercent = lowThreshold.toIntOrNull() ?: 20,
                        criticalBatteryThresholdPercent = critThreshold.toIntOrNull() ?: 10,
                        pirLedDurationMs = (pirDuration.toLongOrNull() ?: 5) * 1000,
                        micLedDurationMs = (micDuration.toLongOrNull() ?: 5) * 1000,
                        maxVoltage = maxV.toFloatOrNull() ?: 4.2f,
                        minVoltage = minV.toFloatOrNull() ?: 3.0f,
                        roomHeightFeet = roomHeight.toFloatOrNull() ?: 9.0f
                    ))
                },
                colors = ButtonDefaults.buttonColors(containerColor = NormalGreen)
            ) { Text("Save") }
        },
        dismissButton = {
            TextButton(onClick = onDismiss) { Text("Cancel") }
        }
    )
}

@Composable
fun SettingsField(label: String, value: String, onValueChange: (String) -> Unit) {
    OutlinedTextField(
        value = value,
        onValueChange = onValueChange,
        label = { Text(label, fontSize = 12.sp) },
        singleLine = true,
        modifier = Modifier.fillMaxWidth(),
        keyboardOptions = KeyboardOptions(keyboardType = KeyboardType.Number)
    )
}

// ═══════════════════════════════════════════
// COMPONENTS
// ═══════════════════════════════════════════

@Composable
fun StatusCard(
    state: SensorState,
    rawText: String,
    isFall: Boolean,
    onDismissFall: () -> Unit
) {
    val (bgColor, textColor, title) = when {
        isFall || state == SensorState.ALERT -> Triple(AlertRed, Color.White, "🚨 FALL DETECTED!")
        state == SensorState.WARNING -> Triple(WarnYellow, Color.Black, "⏳ VERIFYING...")
        state == SensorState.INFO -> Triple(InfoBlue, Color.White, "SYSTEM STATUS")
        state == SensorState.NORMAL -> Triple(NormalGreen, Color.White, "ROOM OCCUPIED - MONITORING")
        state == SensorState.SCANNING -> Triple(Color(0xFF616161), Color.White, "SCANNING...")
        else -> Triple(Color(0xFF424242), Color.White, "DISCONNECTED")
    }

    val animatedBg by animateColorAsState(
        targetValue = bgColor,
        animationSpec = tween(durationMillis = 400),
        label = "statusBg"
    )

    Card(
        modifier = Modifier
            .fillMaxWidth()
            .height(if (isFall) 130.dp else 100.dp),
        colors = CardDefaults.cardColors(containerColor = animatedBg),
        elevation = CardDefaults.cardElevation(defaultElevation = 6.dp),
        shape = RoundedCornerShape(16.dp)
    ) {
        Column(
            modifier = Modifier
                .fillMaxSize()
                .padding(10.dp),
            verticalArrangement = Arrangement.Center,
            horizontalAlignment = Alignment.CenterHorizontally
        ) {
            Text(
                text = title,
                style = MaterialTheme.typography.titleMedium,
                fontWeight = FontWeight.ExtraBold,
                color = textColor
            )
            Spacer(modifier = Modifier.height(3.dp))
            Text(
                text = rawText,
                style = MaterialTheme.typography.bodySmall,
                color = textColor.copy(alpha = 0.9f),
                textAlign = TextAlign.Center,
                maxLines = 2,
                fontSize = 11.sp
            )
            if (isFall) {
                Spacer(modifier = Modifier.height(6.dp))
                Button(
                    onClick = onDismissFall,
                    colors = ButtonDefaults.buttonColors(containerColor = Color.White),
                    contentPadding = PaddingValues(horizontal = 16.dp, vertical = 3.dp),
                    shape = RoundedCornerShape(12.dp)
                ) {
                    Text("Clear Alarm", color = AlertRed, fontWeight = FontWeight.Bold, fontSize = 12.sp)
                }
            }
        }
    }
}

@Composable
fun LedIndicatorRow(ledState: LedState) {
    Card(
        modifier = Modifier.fillMaxWidth(),
        colors = CardDefaults.cardColors(containerColor = CardDark),
        shape = RoundedCornerShape(12.dp)
    ) {
        Row(
            modifier = Modifier
                .fillMaxWidth()
                .padding(vertical = 10.dp, horizontal = 8.dp),
            horizontalArrangement = Arrangement.SpaceEvenly
        ) {
            LedDot(label = "PIR", isActive = ledState.pirActive, activeColor = LedPirYellow)
            LedDot(label = "MIC", isActive = ledState.micActive, activeColor = LedMicCyan)
            LedDot(label = "RADAR", isActive = ledState.radarActive, activeColor = LedRadarGreen)
            LedDot(label = "FALL", isActive = ledState.fallDetected, activeColor = LedFallRed)
        }
    }
}

@Composable
fun LedDot(label: String, isActive: Boolean, activeColor: Color) {
    val color by animateColorAsState(
        targetValue = if (isActive) activeColor else LedOff,
        animationSpec = tween(durationMillis = 300),
        label = "led_$label"
    )
    Column(horizontalAlignment = Alignment.CenterHorizontally) {
        Box(
            modifier = Modifier
                .size(26.dp)
                .shadow(
                    elevation = if (isActive) 8.dp else 0.dp,
                    shape = CircleShape,
                    ambientColor = if (isActive) activeColor else Color.Transparent,
                    spotColor = if (isActive) activeColor else Color.Transparent
                )
                .clip(CircleShape)
                .background(color)
                .then(
                    if (isActive) Modifier.border(1.dp, activeColor.copy(alpha = 0.5f), CircleShape)
                    else Modifier
                )
        )
        Spacer(modifier = Modifier.height(3.dp))
        Text(
            text = label,
            color = if (isActive) activeColor else Color.Gray,
            fontSize = 10.sp,
            fontWeight = if (isActive) FontWeight.Bold else FontWeight.Normal
        )
    }
}

@Composable
fun TelemetryCard(title: String, value: String, unit: String, modifier: Modifier = Modifier) {
    Card(
        modifier = modifier.height(68.dp),
        elevation = CardDefaults.cardElevation(defaultElevation = 3.dp),
        shape = RoundedCornerShape(12.dp)
    ) {
        Column(
            modifier = Modifier
                .fillMaxSize()
                .padding(6.dp),
            verticalArrangement = Arrangement.Center,
            horizontalAlignment = Alignment.CenterHorizontally
        ) {
            Text(text = title, style = MaterialTheme.typography.labelSmall, color = Color.Gray)
            Spacer(modifier = Modifier.height(2.dp))
            Row(verticalAlignment = Alignment.Bottom) {
                Text(text = value, style = MaterialTheme.typography.titleMedium, fontWeight = FontWeight.Bold)
                if (unit.isNotEmpty()) {
                    Text(text = " $unit", style = MaterialTheme.typography.labelSmall, modifier = Modifier.padding(bottom = 2.dp))
                }
            }
        }
    }
}
