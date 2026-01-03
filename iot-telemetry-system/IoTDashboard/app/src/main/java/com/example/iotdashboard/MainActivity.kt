package com.example.iotdashboard

import android.os.Bundle
import androidx.activity.ComponentActivity
import androidx.activity.compose.setContent
import androidx.compose.foundation.layout.*
import androidx.compose.material3.*
import androidx.compose.runtime.*
import androidx.compose.ui.Modifier
import androidx.compose.ui.unit.dp
import okhttp3.OkHttpClient
import okhttp3.Request
import org.json.JSONObject

class MainActivity : ComponentActivity() {

    private val client = OkHttpClient()

    private val TELEMETRY_URL =
        "https://prototype-8cd99-default-rtdb.firebaseio.com/telemetry/latest.json"

    override fun onCreate(savedInstanceState: Bundle?) {
        super.onCreate(savedInstanceState)

        setContent {
            MaterialTheme {
                TelemetryScreen()
            }
        }
    }

    @Composable
    fun TelemetryScreen() {
        var output by remember { mutableStateOf("Loading telemetry...") }

        fun loadTelemetry() {
            output = "Loading..."
            Thread {
                try {
                    val req = Request.Builder().url(TELEMETRY_URL).build()
                    val res = client.newCall(req).execute()
                    val body = res.body?.string() ?: "{}"

                    val json = JSONObject(body)
                    val deviceId = json.optString("device_id", "N/A")
                    val temp = json.optDouble("temperature_c", Double.NaN)
                    val batt = json.optInt("battery_pct", -1)
                    val rssi = json.optInt("rssi_dbm", 0)

                    val alerts = mutableListOf<String>()
                    if (!temp.isNaN() && temp > 30.0) alerts.add("High temp")
                    if (batt in 0..20) alerts.add("Low battery")
                    if (rssi < -80) alerts.add("Weak signal")

                    output = """
                        Device: $deviceId
                        Temp: $temp °C
                        Battery: $batt %
                        RSSI: $rssi dBm
                        
                        Alerts: ${if (alerts.isEmpty()) "None" else alerts.joinToString(", ")}
                    """.trimIndent()

                } catch (e: Exception) {
                    output = "Error: ${e.message}"
                }
            }.start()
        }

        LaunchedEffect(Unit) {
            loadTelemetry()
        }

        Column(
            modifier = Modifier
                .fillMaxSize()
                .padding(16.dp)
        ) {
            Button(onClick = { loadTelemetry() }) {
                Text("Refresh Telemetry")
            }

            Spacer(modifier = Modifier.height(16.dp))

            Text(output)
        }
    }
}
