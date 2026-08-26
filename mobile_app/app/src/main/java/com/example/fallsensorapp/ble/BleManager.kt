package com.example.fallsensorapp.ble

import android.annotation.SuppressLint
import android.bluetooth.*
import android.bluetooth.le.ScanCallback
import android.bluetooth.le.ScanResult
import android.content.Context
import android.util.Log
import com.example.fallsensorapp.BuildConfig
import kotlinx.coroutines.flow.MutableSharedFlow
import kotlinx.coroutines.flow.MutableStateFlow
import kotlinx.coroutines.flow.SharedFlow
import kotlinx.coroutines.flow.StateFlow
import java.util.UUID

@SuppressLint("MissingPermission")
class BleManager(private val context: Context, private val bluetoothAdapter: BluetoothAdapter?) {

    private val TAG = "BleManager"

    private val SERVICE_UUID = UUID.fromString("4fafc201-1fb5-459e-8fcc-c5c9c331914b")
    private val CHAR_UUID = UUID.fromString("beb5483e-36e1-4688-b7f5-ea07361b26a8")
    private val CCCD_UUID = UUID.fromString("00002902-0000-1000-8000-00805f9b34fb")

    // Read from BuildConfig so each flavor auto-targets the correct device
    val bleNamePrefix: String = BuildConfig.BLE_NAME_PREFIX
    val serviceUuidString: String = SERVICE_UUID.toString()

    private var bluetoothGatt: BluetoothGatt? = null

    private val _connectionState = MutableStateFlow("Disconnected")
    val connectionState: StateFlow<String> = _connectionState

    private val _incomingMessages = MutableSharedFlow<String>(extraBufferCapacity = 10)
    val incomingMessages: SharedFlow<String> = _incomingMessages

    private val scanCallback = object : ScanCallback() {
        override fun onScanResult(callbackType: Int, result: ScanResult) {
            val device = result.device
            val deviceName = device.name ?: ""
            val uuids = result.scanRecord?.serviceUuids?.map { it.toString() } ?: emptyList()
            
            // Log EVERY device we see for debugging
            if (deviceName.isNotEmpty()) {
                Log.d(TAG, "Found device: '$deviceName' | UUIDs: $uuids")
            }
            
            // Prefix match: "Fall_Sensor_LD2410" matches "Fall_Sensor_LD2410_v1.0", etc.
            val nameMatch = deviceName.startsWith(bleNamePrefix)
            val uuidMatch = result.scanRecord?.serviceUuids?.contains(android.os.ParcelUuid(SERVICE_UUID)) == true
            
            if (nameMatch || uuidMatch) {
                Log.i(TAG, "TARGET FOUND! Name='$deviceName' nameMatch=$nameMatch uuidMatch=$uuidMatch")
                stopScan()
                connectToDevice(device)
            }
        }
        
        override fun onScanFailed(errorCode: Int) {
            Log.e(TAG, "BLE Scan FAILED with error code: $errorCode")
            _connectionState.value = "Scan Failed ($errorCode)"
        }
    }

    private val gattCallback = object : BluetoothGattCallback() {
        override fun onConnectionStateChange(gatt: BluetoothGatt, status: Int, newState: Int) {
            Log.d(TAG, "onConnectionStateChange: status=$status newState=$newState")
            
            if (status == BluetoothGatt.GATT_SUCCESS && newState == BluetoothProfile.STATE_CONNECTED) {
                Log.i(TAG, "GATT Connected! Discovering services...")
                _connectionState.value = "Connected"
                gatt.discoverServices()
            } else if (newState == BluetoothProfile.STATE_DISCONNECTED) {
                Log.w(TAG, "GATT Disconnected. Status=$status (133=bond issue, 8=timeout, 19=remote disconnect)")
                _connectionState.value = "Disconnected"
                gatt.close()
                bluetoothGatt = null
                
                // Auto-retry on ALL disconnect reasons — this is a safety device
                // that must always try to stay connected
                Log.i(TAG, "Auto-reconnecting in 2 seconds...")
                _connectionState.value = "Retrying..."
                android.os.Handler(android.os.Looper.getMainLooper()).postDelayed({
                    startScan()
                }, 2000)
            }
        }

        override fun onServicesDiscovered(gatt: BluetoothGatt, status: Int) {
            Log.d(TAG, "onServicesDiscovered: status=$status")
            if (status == BluetoothGatt.GATT_SUCCESS) {
                val service = gatt.getService(SERVICE_UUID)
                Log.d(TAG, "Service found: ${service != null}")
                val characteristic = service?.getCharacteristic(CHAR_UUID)
                Log.d(TAG, "Characteristic found: ${characteristic != null}")

                if (characteristic != null) {
                    gatt.setCharacteristicNotification(characteristic, true)

                    val descriptor = characteristic.getDescriptor(CCCD_UUID)
                    if (descriptor != null) {
                        descriptor.value = BluetoothGattDescriptor.ENABLE_NOTIFICATION_VALUE
                        gatt.writeDescriptor(descriptor)
                        Log.i(TAG, "Subscribed to notifications!")
                    }
                }
            } else {
                Log.e(TAG, "Service discovery FAILED with status: $status")
            }
        }

        override fun onCharacteristicChanged(gatt: BluetoothGatt, characteristic: BluetoothGattCharacteristic) {
            if (characteristic.uuid == CHAR_UUID) {
                val message = characteristic.value.toString(Charsets.UTF_8)
                Log.d(TAG, "BLE RX: $message")
                _incomingMessages.tryEmit(message)
            }
        }
    }

    fun startScan() {
        if (bluetoothAdapter == null || !bluetoothAdapter.isEnabled) return
        _connectionState.value = "Scanning..."
        bluetoothAdapter.bluetoothLeScanner?.startScan(scanCallback)
    }

    fun stopScan() {
        bluetoothAdapter?.bluetoothLeScanner?.stopScan(scanCallback)
    }

    private fun connectToDevice(device: BluetoothDevice) {
        _connectionState.value = "Connecting..."
        Log.d(TAG, "Connecting to ${device.name} [${device.address}] with TRANSPORT_LE...")
        // TRANSPORT_LE forces BLE transport — without this, Android may try
        // Classic Bluetooth which instantly fails on BLE-only ESP32 devices.
        // Also run on main thread as required by some OEM BLE stacks.
        android.os.Handler(android.os.Looper.getMainLooper()).postDelayed({
            bluetoothGatt = device.connectGatt(context, false, gattCallback, BluetoothDevice.TRANSPORT_LE)
        }, 200)
    }

    /**
     * Writes the logging state to the BLE characteristic.
     * The ESP32 can read this value when its push button is pressed
     * to decide whether to stream data or stay silent.
     */
    fun sendLoggingState(enabled: Boolean) {
        val gatt = bluetoothGatt ?: return
        val service = gatt.getService(SERVICE_UUID) ?: return
        val characteristic = service.getCharacteristic(CHAR_UUID) ?: return

        val command = if (enabled) "LOG_ON" else "LOG_OFF"
        characteristic.value = command.toByteArray(Charsets.UTF_8)
        gatt.writeCharacteristic(characteristic)
    }

    /**
     * Sends the RESET command to reboot the ESP32.
     */
    fun sendResetCommand() {
        val gatt = bluetoothGatt ?: return
        val service = gatt.getService(SERVICE_UUID) ?: return
        val characteristic = service.getCharacteristic(CHAR_UUID) ?: return

        characteristic.value = "RESET".toByteArray(Charsets.UTF_8)
        gatt.writeCharacteristic(characteristic)
    }

    /**
     * Sends the OTA_ON command to initiate firmware update mode over WiFi.
     */
    fun sendOtaOnCommand() {
        val gatt = bluetoothGatt ?: return
        val service = gatt.getService(SERVICE_UUID) ?: return
        val characteristic = service.getCharacteristic(CHAR_UUID) ?: return

        characteristic.value = "OTA_ON".toByteArray(Charsets.UTF_8)
        gatt.writeCharacteristic(characteristic)
    }
}
