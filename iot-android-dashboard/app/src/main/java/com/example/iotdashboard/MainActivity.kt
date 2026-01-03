package com.example.iotdashboard

import android.os.Bundle
import android.widget.Button
import android.widget.TextView
import androidx.appcompat.app.AppCompatActivity
import okhttp3.OkHttpClient
import okhttp3.Request
import org.json.JSONObject

class MainActivity : AppCompatActivity() {

    private val client = OkHttpClient()

    // Replace this with your Firebase base URL
    private val TELEMETRY_URL =
        "https://prototype-8cd99-default-rtdb.firebaseio.com/telemetry/latest.json"

    override fun onCreate(savedInstanceState: Bundle?) {
        super.onCreate(savedInstanceState)
        setContentView(R.layout.activity_main)

        val output = findViewById<TextView>(R.id.output)
        val refreshBtn = findViewById<Button>(R.id.refreshBtn)

        fun loadTelemetry() {
            output.text = "Loading..."
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

                    val text = buildString {
                        appendLine("Device: $deviceId")
                        appendLine("Temp: $temp °C")
                        appendLine("Battery: $batt %")
                        appendLine("RSSI: $rssi dBm")
                        appendLine()
                        appendLine("Alerts: " + if (alerts.isEmpty()) "None" else alerts.joinToString(", "))
                    }

                    runOnUiThread { output.text = text }
                } catch (e: Exception) {
                    runOnUiThread { output.text = "Error: ${e.message}" }
                }
            }.start()
        }

        refreshBtn.setOnClickListener { loadTelemetry() }
        loadTelemetry()
    }
}
