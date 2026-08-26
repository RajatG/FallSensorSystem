package com.example.fallsensorapp.parser

/**
 * Represents the overall system alert level derived from ESP32 messages.
 */
enum class SensorState {
    NORMAL,        // Active monitoring, room occupied, all good
    WARNING,       // Verification or warning
    ALERT,         // Confirmed Fall Alarm
    INFO,          // System state changes (boot, sleep, room empty)
    DISCONNECTED,  // No BLE connection
    SCANNING       // Scanning for device
}

/**
 * Holds the full parsed state extracted from a single BLE message.
 */
data class ParsedMessage(
    val rawText: String,
    val state: SensorState,
    val distance: Int? = null,
    val heartRate: Int? = null,
    val isMoving: Boolean = false,
    val isPirTriggered: Boolean = false,
    val isMicTriggered: Boolean = false,
    val isRadarOn: Boolean = false,
    val isFallDetected: Boolean = false,
    val batteryVoltage: Float? = null,
    val pin25Raw: Int? = null,
    val pin26Raw: Int? = null,
    val uartPresence: Boolean = false,
    val uartFall: Boolean = false,
    val otaIp: String? = null,
    val roomOccupied: Boolean = false
)

/**
 * Stateless parser that converts raw BLE strings from the ESP32 (v4.16) into typed state.
 */
object MessageParser {

    private val distRegex = Regex("""Dist:\s*(\d+)\s*cm""")
    private val alertDistRegex = Regex("""at\s+(\d+)\s*cm""")
    private val battRegex = Regex("""Battery:\s*([\d\.]+)\s*V""")
    private val pin25Regex = Regex("""Pin25_RAW:\s*(\d+)""")
    private val pin26Regex = Regex("""Pin26_RAW:\s*(\d+)""")
    private val uartPresRegex = Regex("""UART Pres:\s*(\d+)""")
    private val uartFallRegex = Regex("""UART Fall:\s*(\d+)""")
    private val otaIpRegex = Regex("""Ready at:\s*([\d\.]+)""")

    fun parse(raw: String): ParsedMessage {
        val clean = raw.replace("\r", "").replace("\n", "").trim()

        // --- Extract numeric telemetry & diagnostics ---
        val dist = distRegex.find(clean)?.groupValues?.get(1)?.toIntOrNull()
            ?: alertDistRegex.find(clean)?.groupValues?.get(1)?.toIntOrNull()
        val batt = battRegex.find(clean)?.groupValues?.get(1)?.toFloatOrNull()
        val pin25 = pin25Regex.find(clean)?.groupValues?.get(1)?.toIntOrNull()
        val pin26 = pin26Regex.find(clean)?.groupValues?.get(1)?.toIntOrNull()
        val uartPres = uartPresRegex.find(clean)?.groupValues?.get(1)?.toIntOrNull() == 1
        val uartFall = uartFallRegex.find(clean)?.groupValues?.get(1)?.toIntOrNull() == 1
        val otaIp = otaIpRegex.find(clean)?.groupValues?.get(1)

        // --- Determine alert level ---
        val isFall = clean.contains("ALERT: FALL") || clean.contains("[ALERT]") || clean.contains("FALL DETECTED")
        val isWarn = clean.contains("[WARN]")
        val isCleared = clean.contains("[FALL] Cleared")

        val state = when {
            isFall -> SensorState.ALERT
            isWarn -> SensorState.WARNING
            clean.contains("Room occupied") -> SensorState.NORMAL
            clean.contains("Room empty") || clean.contains("Person left") -> SensorState.INFO
            clean.contains("[SYS]") || clean.contains("[OTA]") -> SensorState.INFO
            clean.contains("[RADAR]") -> SensorState.NORMAL
            else -> SensorState.INFO
        }

        // --- Trigger flags ---
        val isPir = clean.contains("PIR Triggered") || clean.contains("PIR_WALK_IN")
        val isMic = clean.contains("MIC Triggered") || clean.contains("MIC_THUD")
        val isRadarOn = clean.contains("[RADAR]") || clean.contains("Boot")
        val isOccupied = clean.contains("Room occupied") || clean.contains("Person Entered")

        // --- Movement ---
        val isMoving = clean.contains("MOVING") || (dist != null && dist > 0)

        return ParsedMessage(
            rawText = clean,
            state = state,
            distance = dist,
            isMoving = isMoving,
            isPirTriggered = isPir,
            isMicTriggered = isMic,
            isRadarOn = isRadarOn,
            isFallDetected = isFall && !isCleared,
            batteryVoltage = batt,
            pin25Raw = pin25,
            pin26Raw = pin26,
            uartPresence = uartPres,
            uartFall = uartFall,
            otaIp = otaIp,
            roomOccupied = isOccupied
        )
    }
}
