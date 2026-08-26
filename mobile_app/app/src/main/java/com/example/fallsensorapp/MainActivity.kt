package com.example.fallsensorapp

import android.Manifest
import android.bluetooth.BluetoothAdapter
import android.bluetooth.BluetoothManager
import android.content.Context
import android.content.Intent
import android.content.pm.PackageManager
import android.os.Build
import android.os.Bundle
import android.util.Log
import androidx.activity.ComponentActivity
import androidx.activity.compose.setContent
import androidx.activity.result.contract.ActivityResultContracts
import androidx.compose.foundation.layout.fillMaxSize
import androidx.compose.material3.MaterialTheme
import androidx.compose.material3.Surface
import androidx.compose.ui.Modifier
import androidx.core.content.ContextCompat
import com.example.fallsensorapp.ui.FallSensorAppScreen
import com.example.fallsensorapp.ui.theme.FallSensorAppTheme
import com.example.fallsensorapp.ble.BleManager
import com.example.fallsensorapp.viewmodel.MainViewModel

class MainActivity : ComponentActivity() {

    private val TAG = "FallSensorApp"

    private val requestPermissionLauncher =
        registerForActivityResult(ActivityResultContracts.RequestMultiplePermissions()) { permissions ->
            val granted = permissions.filterValues { it }.keys
            val denied = permissions.filterValues { !it }.keys
            Log.d(TAG, "Permissions granted: $granted")
            Log.d(TAG, "Permissions denied: $denied")
            
            // After permissions, check if Bluetooth is enabled
            checkBluetoothAndScan()
        }

    // Bluetooth enable request launcher
    private val enableBluetoothLauncher =
        registerForActivityResult(ActivityResultContracts.StartActivityForResult()) { result ->
            if (result.resultCode == RESULT_OK) {
                Log.i(TAG, "Bluetooth enabled by user. Starting scan.")
                viewModel.startScanning()
            } else {
                Log.w(TAG, "User declined to enable Bluetooth.")
                // App will show the disconnected overlay with retry button
            }
        }

    private lateinit var bleManager: BleManager
    private lateinit var viewModel: MainViewModel

    override fun onCreate(savedInstanceState: Bundle?) {
        super.onCreate(savedInstanceState)
        
        val bluetoothManager = getSystemService(Context.BLUETOOTH_SERVICE) as BluetoothManager
        val bluetoothAdapter = bluetoothManager.adapter
        
        bleManager = BleManager(this, bluetoothAdapter)
        viewModel = MainViewModel(bleManager)
        
        setContent {
            FallSensorAppTheme {
                Surface(
                    modifier = Modifier.fillMaxSize(),
                    color = MaterialTheme.colorScheme.background
                ) {
                    FallSensorAppScreen(viewModel)
                }
            }
        }
        
        requestBlePermissions()
    }
    
    private fun requestBlePermissions() {
        val requiredPermissions = mutableListOf<String>()
        
        if (Build.VERSION.SDK_INT >= Build.VERSION_CODES.S) {
            requiredPermissions.add(Manifest.permission.BLUETOOTH_SCAN)
            requiredPermissions.add(Manifest.permission.BLUETOOTH_CONNECT)
            requiredPermissions.add(Manifest.permission.ACCESS_FINE_LOCATION)
        } else {
            requiredPermissions.add(Manifest.permission.ACCESS_FINE_LOCATION)
            requiredPermissions.add(Manifest.permission.ACCESS_COARSE_LOCATION)
        }
        
        val missingPermissions = requiredPermissions.filter {
            ContextCompat.checkSelfPermission(this, it) != PackageManager.PERMISSION_GRANTED
        }
        
        Log.d(TAG, "Missing permissions: $missingPermissions")
        
        if (missingPermissions.isNotEmpty()) {
            requestPermissionLauncher.launch(missingPermissions.toTypedArray())
        } else {
            Log.d(TAG, "All permissions already granted.")
            checkBluetoothAndScan()
        }
    }

    private fun checkBluetoothAndScan() {
        val bluetoothManager = getSystemService(Context.BLUETOOTH_SERVICE) as BluetoothManager
        val bluetoothAdapter = bluetoothManager.adapter

        if (bluetoothAdapter == null) {
            Log.e(TAG, "Device does not support Bluetooth.")
            return
        }

        if (!bluetoothAdapter.isEnabled) {
            Log.w(TAG, "Bluetooth is disabled. Requesting user to enable it.")
            val enableBtIntent = Intent(BluetoothAdapter.ACTION_REQUEST_ENABLE)
            enableBluetoothLauncher.launch(enableBtIntent)
        } else {
            Log.d(TAG, "Bluetooth is enabled. Starting scan.")
            viewModel.startScanning()
        }
    }
}
