package com.example.fallsensorapp.viewmodel

import androidx.lifecycle.ViewModel
import androidx.lifecycle.viewModelScope
import com.example.fallsensorapp.ble.BleManager
import com.example.fallsensorapp.parser.MessageParser
import com.example.fallsensorapp.parser.ParsedMessage
import com.example.fallsensorapp.parser.SensorState
import kotlinx.coroutines.Job
import kotlinx.coroutines.delay
import kotlinx.coroutines.flow.MutableStateFlow
import kotlinx.coroutines.flow.StateFlow
import kotlinx.coroutines.flow.asStateFlow
import kotlinx.coroutines.launch

/**
 * Holds the visual state of the 4 LED indicators.
 */
data class LedState(
    val pirActive: Boolean = false,
    val micActive: Boolean = false,
    val radarActive: Boolean = false,
    val fallDetected: Boolean = false
)

/**
 * User-configurable settings with sensible defaults.
 */
data class SensorSettings(
    val batteryCapacityMah: Int = 2000,
    val lowBatteryThresholdPercent: Int = 20,
    val criticalBatteryThresholdPercent: Int = 10,
    val pirLedDurationMs: Long = 5000,
    val micLedDurationMs: Long = 5000,
    val maxVoltage: Float = 4.2f,
    val minVoltage: Float = 3.0f
)

/**
 * Battery telemetry tracking record.
 */
data class BatteryRecord(
    val voltage: Float,
    val timestampMs: Long
)

class MainViewModel(private val bleManager: BleManager) : ViewModel() {

    // --- UI State ---
    private val _uiState = MutableStateFlow(
        ParsedMessage("Waiting for connection...", SensorState.DISCONNECTED)
    )
    val uiState: StateFlow<ParsedMessage> = _uiState.asStateFlow()

    private val _connectionStatus = MutableStateFlow("Disconnected")
    val connectionStatus: StateFlow<String> = _connectionStatus.asStateFlow()

    val bleNamePrefix: String = bleManager.bleNamePrefix
    val serviceUuid: String = bleManager.serviceUuidString

    private val _messageLog = MutableStateFlow<List<String>>(emptyList())
    val messageLog: StateFlow<List<String>> = _messageLog.asStateFlow()

    // --- LED Indicators ---
    private val _ledState = MutableStateFlow(LedState())
    val ledState: StateFlow<LedState> = _ledState.asStateFlow()

    // --- Telemetry & Diagnostics ---
    private val _distance = MutableStateFlow<Int?>(null)
    val distance: StateFlow<Int?> = _distance.asStateFlow()

    private val _batteryVoltage = MutableStateFlow<Float?>(null)
    val batteryVoltage: StateFlow<Float?> = _batteryVoltage.asStateFlow()

    private val _batteryPercent = MutableStateFlow<Int?>(null)
    val batteryPercent: StateFlow<Int?> = _batteryPercent.asStateFlow()

    private val _pin25Raw = MutableStateFlow<Int?>(null)
    val pin25Raw: StateFlow<Int?> = _pin25Raw.asStateFlow()

    private val _pin26Raw = MutableStateFlow<Int?>(null)
    val pin26Raw: StateFlow<Int?> = _pin26Raw.asStateFlow()

    private val _uartPresence = MutableStateFlow(false)
    val uartPresence: StateFlow<Boolean> = _uartPresence.asStateFlow()

    private val _uartFall = MutableStateFlow(false)
    val uartFall: StateFlow<Boolean> = _uartFall.asStateFlow()

    private val _otaIp = MutableStateFlow<String?>(null)
    val otaIp: StateFlow<String?> = _otaIp.asStateFlow()

    private val _roomOccupied = MutableStateFlow(false)
    val roomOccupied: StateFlow<Boolean> = _roomOccupied.asStateFlow()

    private val _isMoving = MutableStateFlow(false)
    val isMoving: StateFlow<Boolean> = _isMoving.asStateFlow()

    // --- Battery Prediction ---
    private val _uptimeMs = MutableStateFlow(0L)
    val uptimeMs: StateFlow<Long> = _uptimeMs.asStateFlow()

    private val _estimatedDaysRemaining = MutableStateFlow<Float?>(null)
    val estimatedDaysRemaining: StateFlow<Float?> = _estimatedDaysRemaining.asStateFlow()

    private val _lowBatteryAlert = MutableStateFlow(false)
    val lowBatteryAlert: StateFlow<Boolean> = _lowBatteryAlert.asStateFlow()

    private val batteryHistory = mutableListOf<BatteryRecord>()
    private var connectionStartTime = 0L

    // --- Settings ---
    private val _settings = MutableStateFlow(SensorSettings())
    val settings: StateFlow<SensorSettings> = _settings.asStateFlow()

    // --- Master Logging Switch ---
    private val _isLoggingEnabled = MutableStateFlow(false)
    val isLoggingEnabled: StateFlow<Boolean> = _isLoggingEnabled.asStateFlow()

    // --- LED Auto-Off Coroutine Jobs ---
    private var pirLedJob: Job? = null
    private var micLedJob: Job? = null

    init {
        // Watch connection state
        viewModelScope.launch {
            bleManager.connectionState.collect { state ->
                _connectionStatus.value = state
                if (state == "Disconnected") {
                    _uiState.value = ParsedMessage("Disconnected", SensorState.DISCONNECTED)
                    _ledState.value = LedState()
                    _isLoggingEnabled.value = false
                } else if (state == "Scanning...") {
                    _uiState.value = ParsedMessage("Scanning for device...", SensorState.SCANNING)
                } else if (state == "Connected") {
                    connectionStartTime = System.currentTimeMillis()
                }
            }
        }

        // Uptime ticker
        viewModelScope.launch {
            while (true) {
                delay(1000)
                if (connectionStartTime > 0 && _connectionStatus.value == "Connected") {
                    _uptimeMs.value = System.currentTimeMillis() - connectionStartTime
                }
            }
        }

        // Watch incoming BLE messages
        viewModelScope.launch {
            bleManager.incomingMessages.collect { rawMsg ->
                val parsed = MessageParser.parse(rawMsg)

                // Update persistent fields from every message
                if (parsed.batteryVoltage != null) {
                    _batteryVoltage.value = parsed.batteryVoltage
                    val s = _settings.value
                    val pct = ((parsed.batteryVoltage - s.minVoltage) / (s.maxVoltage - s.minVoltage) * 100).coerceIn(0f, 100f).toInt()
                    _batteryPercent.value = pct
                    recordBattery(parsed.batteryVoltage)
                    updateBatteryPrediction()

                    // Low battery alert
                    if (pct <= s.criticalBatteryThresholdPercent) {
                        _lowBatteryAlert.value = true
                    } else if (pct <= s.lowBatteryThresholdPercent) {
                        _lowBatteryAlert.value = true
                    } else {
                        _lowBatteryAlert.value = false
                    }
                }
                if (parsed.distance != null) _distance.value = parsed.distance
                if (parsed.pin25Raw != null) _pin25Raw.value = parsed.pin25Raw
                if (parsed.pin26Raw != null) _pin26Raw.value = parsed.pin26Raw
                if (parsed.otaIp != null) _otaIp.value = parsed.otaIp

                _uartPresence.value = parsed.uartPresence
                _uartFall.value = parsed.uartFall
                if (parsed.roomOccupied) _roomOccupied.value = true

                // Always process ALERT (fall notification) regardless of logging switch
                if (parsed.isFallDetected) {
                    _uiState.value = parsed
                    _ledState.value = _ledState.value.copy(fallDetected = true, radarActive = false)
                    _messageLog.value = (_messageLog.value + parsed.rawText).takeLast(100)
                    return@collect
                }

                // If fall cleared
                if (parsed.rawText.contains("[FALL] Cleared")) {
                    _ledState.value = _ledState.value.copy(fallDetected = false)
                    _uiState.value = parsed
                    _messageLog.value = (_messageLog.value + parsed.rawText).takeLast(100)
                }

                // PIR trigger with auto-off timer
                if (parsed.isPirTriggered) {
                    _ledState.value = _ledState.value.copy(pirActive = true)
                    pirLedJob?.cancel()
                    pirLedJob = viewModelScope.launch {
                        delay(_settings.value.pirLedDurationMs)
                        _ledState.value = _ledState.value.copy(pirActive = false)
                    }
                }

                // MIC trigger with auto-off timer
                if (parsed.isMicTriggered) {
                    _ledState.value = _ledState.value.copy(micActive = true)
                    micLedJob?.cancel()
                    micLedJob = viewModelScope.launch {
                        delay(_settings.value.micLedDurationMs)
                        _ledState.value = _ledState.value.copy(micActive = false)
                    }
                }

                // Radar active state
                val currentLeds = _ledState.value
                if (parsed.isRadarOn) {
                    _ledState.value = currentLeds.copy(radarActive = true)
                }

                // Reset all LEDs when radar goes to sleep
                if (parsed.rawText.contains("Sleeping") || parsed.rawText.contains("Deep Sleep")) {
                    _ledState.value = _ledState.value.copy(radarActive = false)
                    _roomOccupied.value = parsed.rawText.contains("occupied")
                }

                // Room empty detection
                if (parsed.rawText.contains("Room empty") || parsed.rawText.contains("Person left")) {
                    _roomOccupied.value = false
                }

                // Always update main UI text and log feed (lightweight messages are fine)
                _uiState.value = parsed
                _isMoving.value = parsed.isMoving

                // Only add to terminal log if logging is enabled (heavy diagnostic lines)
                if (_isLoggingEnabled.value) {
                    _messageLog.value = (_messageLog.value + parsed.rawText).takeLast(100)
                } else {
                    // Without LOG_ON, still log critical messages to the feed
                    val isCritical = parsed.isFallDetected ||
                        parsed.rawText.contains("[FALL]") ||
                        parsed.rawText.contains("[WARN]") ||
                        parsed.rawText.contains("Battery") ||
                        parsed.rawText.contains("Person") ||
                        parsed.rawText.contains("Room") ||
                        parsed.rawText.contains("[OTA]")
                    if (isCritical) {
                        _messageLog.value = (_messageLog.value + parsed.rawText).takeLast(50)
                    }
                }
            }
        }
    }

    private fun recordBattery(voltage: Float) {
        batteryHistory.add(BatteryRecord(voltage, System.currentTimeMillis()))
        // Keep last 100 records
        if (batteryHistory.size > 100) {
            batteryHistory.removeAt(0)
        }
    }

    private fun updateBatteryPrediction() {
        if (batteryHistory.size < 2) {
            _estimatedDaysRemaining.value = null
            return
        }
        val first = batteryHistory.first()
        val last = batteryHistory.last()
        val elapsedHours = (last.timestampMs - first.timestampMs) / 3600000.0f
        if (elapsedHours < 0.01f) {
            _estimatedDaysRemaining.value = null
            return
        }
        val voltageDrop = first.voltage - last.voltage
        if (voltageDrop <= 0.001f) {
            // No measurable drain yet — show as >30 days
            _estimatedDaysRemaining.value = 30f
            return
        }
        val s = _settings.value
        val remainingVoltage = last.voltage - s.minVoltage
        if (remainingVoltage <= 0f) {
            _estimatedDaysRemaining.value = 0f
            return
        }
        val drainRatePerHour = voltageDrop / elapsedHours
        val hoursRemaining = remainingVoltage / drainRatePerHour
        _estimatedDaysRemaining.value = (hoursRemaining / 24f).coerceIn(0f, 365f)
    }

    fun startScanning() {
        bleManager.startScan()
    }

    fun toggleLogging(enabled: Boolean) {
        _isLoggingEnabled.value = enabled
        bleManager.sendLoggingState(enabled)
    }

    fun triggerOta() {
        bleManager.sendOtaOnCommand()
    }

    fun resetDevice() {
        bleManager.sendResetCommand()
    }

    fun dismissFallAlarm() {
        _ledState.value = _ledState.value.copy(fallDetected = false)
        _uiState.value = ParsedMessage("Alarm Dismissed by User", SensorState.NORMAL)
    }

    fun updateSettings(newSettings: SensorSettings) {
        _settings.value = newSettings
        // Recalculate battery percent with new thresholds
        _batteryVoltage.value?.let { v ->
            val pct = ((v - newSettings.minVoltage) / (newSettings.maxVoltage - newSettings.minVoltage) * 100).coerceIn(0f, 100f).toInt()
            _batteryPercent.value = pct
            _lowBatteryAlert.value = pct <= newSettings.lowBatteryThresholdPercent
        }
    }

    fun formatUptime(ms: Long): String {
        val totalSec = ms / 1000
        val hours = totalSec / 3600
        val minutes = (totalSec % 3600) / 60
        val seconds = totalSec % 60
        return if (hours > 0) "${hours}h ${minutes}m ${seconds}s"
        else if (minutes > 0) "${minutes}m ${seconds}s"
        else "${seconds}s"
    }
}
