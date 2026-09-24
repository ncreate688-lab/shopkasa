package com.softbuild.mpesalistener

import android.Manifest
import android.content.BroadcastReceiver
import android.content.Context
import android.content.Intent
import android.content.IntentFilter
import android.content.pm.PackageManager
import android.os.Build
import android.os.Bundle
import android.os.Handler
import android.os.Looper
import android.view.View
import android.widget.Button
import android.widget.EditText
import android.widget.LinearLayout
import android.widget.ScrollView
import android.widget.TextView
import android.widget.Toast
import androidx.appcompat.app.AppCompatActivity
import androidx.core.app.ActivityCompat
import androidx.core.content.ContextCompat
import okhttp3.*
import okhttp3.MediaType.Companion.toMediaType
import okhttp3.RequestBody.Companion.toRequestBody
import java.io.IOException
import java.text.SimpleDateFormat
import java.util.Date
import java.util.Locale

class MainActivity : AppCompatActivity() {

    companion object {
        const val LOG_ACTION = "com.softbuild.mpesalistener.LOG"
        const val SMS_PERMISSION_CODE = 100
        const val INACTIVITY_TIMEOUT = 600000L // 10 minutes
    }

    private var tvLogs: TextView? = null
    private var tvStatus: TextView? = null
    private var scrollLogs: ScrollView? = null
    private var etApiUrl: EditText? = null
    private var etStoreId: EditText? = null
    private var etAuthToken: EditText? = null
    private var etDbUrl: EditText? = null
    private var etDbToken: EditText? = null

    private var lockContainer: LinearLayout? = null
    private var mainContainer: ScrollView? = null
    private var etUsername: EditText? = null
    private var etPassword: EditText? = null
    private var btnUnlock: Button? = null
    private var pinContainer: LinearLayout? = null
    private var etUnlockPin: EditText? = null
    private var btnUnlockPin: Button? = null
    private var btnManualLock: Button? = null
    private var etSetPin: EditText? = null
    private var btnSetPin: Button? = null
    private var btnLogout: Button? = null
    private var tvLockMessage: TextView? = null
    private var packagesContainer: LinearLayout? = null
    private var tvPackagesLoading: TextView? = null
    
    private var lastPauseTime: Long = 0
    private var isPinLocked = false

    private val mainHandler = Handler(Looper.getMainLooper())
    private val inactivityHandler = Handler(Looper.getMainLooper())
    private val lockRunnable = Runnable { lockAppPin() } // Lock to PIN instead of full logout
    
    // Polling logic
    private val pollHandler = Handler(Looper.getMainLooper())
    private val pollRunnable = object : Runnable {
        override fun run() {
            val isActivated = getSharedPreferences("AppPrefs", Context.MODE_PRIVATE).getBoolean("IS_ACTIVATED", false)
            if (isActivated && !isPinLocked) {
                checkRemoteLockStatus()
            }
            pollHandler.postDelayed(this, 15000L) // poll every 15s
        }
    }
    
    private var isLocked = false // refers to full lock out (unactivated)

    private val logReceiver = object : BroadcastReceiver() {
        override fun onReceive(context: Context?, intent: Intent?) {
            try {
                val msg = intent?.getStringExtra("log") ?: return
                appendLog(msg)
            } catch (e: Exception) { /* ignore */ }
        }
    }

    override fun onCreate(savedInstanceState: Bundle?) {
        super.onCreate(savedInstanceState)
        try {
            setContentView(R.layout.activity_main)

            tvLogs        = findViewById(R.id.tvLogs)
            tvStatus      = findViewById(R.id.tvStatus)
            scrollLogs    = findViewById(R.id.scrollLogs)
            etApiUrl      = findViewById(R.id.etApiUrl)
            etStoreId     = findViewById(R.id.etStoreId)
            etAuthToken   = findViewById(R.id.etAuthToken)
            etDbUrl       = findViewById(R.id.etDbUrl)
            etDbToken     = findViewById(R.id.etDbToken)

            lockContainer = findViewById(R.id.lockContainer)
            mainContainer = findViewById(R.id.mainContainer)
            etUsername    = findViewById(R.id.etUsername)
            etPassword    = findViewById(R.id.etPassword)
            btnUnlock     = findViewById(R.id.btnUnlock)
            pinContainer  = findViewById(R.id.pinContainer)
            etUnlockPin   = findViewById(R.id.etUnlockPin)
            btnUnlockPin  = findViewById(R.id.btnUnlockPin)
            btnManualLock = findViewById(R.id.btnManualLock)
            etSetPin      = findViewById(R.id.etSetPin)
            btnSetPin     = findViewById(R.id.btnSetPin)
            btnLogout     = findViewById(R.id.btnLogout)
            tvLockMessage = findViewById(R.id.tvLockMessage)
            packagesContainer = findViewById(R.id.packagesContainer)
            tvPackagesLoading = findViewById(R.id.tvPackagesLoading)

            val btnSave  = findViewById<Button>(R.id.btnSave)
            val btnTest  = findViewById<Button>(R.id.btnTest)
            val btnClear = findViewById<Button>(R.id.btnClearLogs)

            val prefs = getSharedPreferences("AppPrefs", Context.MODE_PRIVATE)
            etApiUrl?.setText(prefs.getString("API_URL", ""))
            etStoreId?.setText(prefs.getString("STORE_ID", ""))
            etAuthToken?.setText(prefs.getString("AUTH_TOKEN", ""))
            etDbUrl?.setText(prefs.getString("TURSO_URL", ""))
            etDbToken?.setText(prefs.getString("TURSO_TOKEN", ""))

            btnSave.setOnClickListener {
                try {
                    prefs.edit()
                        .putString("API_URL",     etApiUrl?.text.toString().trim())
                        .putString("STORE_ID",    etStoreId?.text.toString().trim())
                        .putString("AUTH_TOKEN",  etAuthToken?.text.toString().trim())
                        .putString("TURSO_URL",   etDbUrl?.text.toString().trim())
                        .putString("TURSO_TOKEN", etDbToken?.text.toString().trim())
                        .apply()
                    Toast.makeText(this, "Settings Saved!", Toast.LENGTH_SHORT).show()
                    appendLog("Settings saved OK.")
                } catch (e: Exception) {
                    appendLog("Save error: ${e.message}")
                }
            }

            btnTest.setOnClickListener {
                try { testConnection() }
                catch (e: Exception) { appendLog("Error: ${e.message}") }
            }

            btnManualLock?.setOnClickListener {
                showPinLock()
            }
            
            btnSetPin?.setOnClickListener {
                val newPin = etSetPin?.text.toString().trim()
                if (newPin.length == 4) {
                    prefs.edit().putString("LOCK_PIN", newPin).apply()
                    Toast.makeText(this, "PIN Saved successfully", Toast.LENGTH_SHORT).show()
                    etSetPin?.setText("")
                } else {
                    Toast.makeText(this, "PIN must be 4 digits", Toast.LENGTH_SHORT).show()
                }
            }
            
            btnLogout?.setOnClickListener {
                prefs.edit().putBoolean("IS_ACTIVATED", false).apply()
                lockApp()
                Toast.makeText(this, "Logged out", Toast.LENGTH_SHORT).show()
            }
            
            btnUnlockPin?.setOnClickListener {
                val pin = etUnlockPin?.text.toString().trim()
                var savedPin = getSharedPreferences("AppPrefs", Context.MODE_PRIVATE).getString("LOCK_PIN", "") ?: ""
                if (savedPin.isEmpty()) {
                    savedPin = getSharedPreferences("AppPrefs", Context.MODE_PRIVATE).getString("PROFILE_PASS", "") ?: ""
                }
                
                if (pin == savedPin) {
                    hidePinLock()
                    Toast.makeText(this, "App Unlocked", Toast.LENGTH_SHORT).show()
                } else {
                    Toast.makeText(this, "Incorrect PIN", Toast.LENGTH_SHORT).show()
                }
            }

            btnClear.setOnClickListener {
                tvLogs?.text = "Logs cleared.\n"
            }

            btnUnlock?.setOnClickListener {
                val user = etUsername?.text.toString().trim()
                val pass = etPassword?.text.toString().trim()
                val deviceId = android.provider.Settings.Secure.getString(contentResolver, android.provider.Settings.Secure.ANDROID_ID)
                
                if (user.isEmpty() || pass.isEmpty()) {
                    Toast.makeText(this, "Enter username and password", Toast.LENGTH_SHORT).show()
                    return@setOnClickListener
                }
                
                val dbUrl = "libsql://sms-forwarder-pos-success.aws-ap-northeast-1.turso.io"
                val dbToken = "eyJhbGciOiJFZERTQSIsInR5cCI6IkpXVCJ9.eyJhIjoicnciLCJpYXQiOjE3ODQxNjU1OTQsImlkIjoiMDE5ZjY4OGUtNWEwMS03ZTRmLTk3ZDUtN2UyNTQ3M2EwMzkyIiwia2lkIjoia05aTnBZOWg1QldlX0FHdzU4RG40RFNCbllDWWZPWUJWLTFTZ3V5NE5XOCIsInJpZCI6IjBiYTY0YzQxLWM1YjMtNDc5OS05MDBmLTFiNWU3ZmFkYWQ0NiJ9.aHdrwvBjrlGV49sXTViHqCDUI7lvmZrriUQXenim6Bv-YWT1JzrEW-hgE2aV1blsbM2Rw3nzVZDwEh9v9WfGDQ"
                val finalUrl = "https://softlybuiltserverpos.netlify.app/.netlify/functions/verify-license"
                
                btnUnlock?.text = "Activating..."
                btnUnlock?.isEnabled = false
                
                try {
                    val payload = org.json.JSONObject().apply {
                        put("username", user)
                        put("password", pass)
                        put("device_id", deviceId)
                        put("db_url", dbUrl)
                        put("db_token", dbToken)
                    }
                    val req = okhttp3.Request.Builder()
                        .url(finalUrl)
                        .post(payload.toString().toRequestBody("application/json".toMediaType()))
                        .build()
                        
                    okhttp3.OkHttpClient().newCall(req).enqueue(object : okhttp3.Callback {
                        override fun onFailure(call: okhttp3.Call, e: java.io.IOException) {
                            runOnUiThread {
                                btnUnlock?.text = "Activate Device"
                                btnUnlock?.isEnabled = true
                                Toast.makeText(this@MainActivity, "Network Error: ${e.message}", Toast.LENGTH_LONG).show()
                            }
                        }
                        override fun onResponse(call: okhttp3.Call, response: okhttp3.Response) {
                            val respStr = response.body?.string() ?: ""
                            runOnUiThread {
                                btnUnlock?.text = "Activate Device"
                                btnUnlock?.isEnabled = true
                                if (response.isSuccessful && respStr.contains("\"success\":true")) {
                                    getSharedPreferences("AppPrefs", android.content.Context.MODE_PRIVATE).edit()
                                        .putBoolean("IS_ACTIVATED", true)
                                        .putString("PROFILE_USER", user)
                                        .putString("PROFILE_PASS", pass)
                                        .apply()
                                    unlockApp()
                                    Toast.makeText(this@MainActivity, "Activated Successfully!", Toast.LENGTH_LONG).show()
                                } else {
                                    Toast.makeText(this@MainActivity, "Activation Failed: $respStr", Toast.LENGTH_LONG).show()
                                }
                            }
                        }
                    })
                } catch(e: Exception) {
                    btnUnlock?.text = "Activate Device"
                    btnUnlock?.isEnabled = true
                    Toast.makeText(this, "Error: ${e.message}", Toast.LENGTH_LONG).show()
                }
            }

            val filter = IntentFilter(LOG_ACTION)
            if (Build.VERSION.SDK_INT >= Build.VERSION_CODES.TIRAMISU) {
                registerReceiver(logReceiver, filter, RECEIVER_NOT_EXPORTED)
            } else {
                registerReceiver(logReceiver, filter)
            }

            checkSmsPermissions()
            resetInactivityTimer()

            if (prefs.getBoolean("IS_ACTIVATED", false)) {
                unlockApp()
                checkRemoteLockStatus()
            } else {
                lockApp()
            }

        } catch (e: Exception) {
            try { Toast.makeText(this, "Startup error: ${e.message}", Toast.LENGTH_LONG).show() }
            catch (_: Exception) {}
        }
    }

    override fun onUserInteraction() {
        super.onUserInteraction()
        if (!isLocked && !isPinLocked) {
            resetInactivityTimer()
        }
    }

    private fun resetInactivityTimer() {
        inactivityHandler.removeCallbacks(lockRunnable)
        inactivityHandler.postDelayed(lockRunnable, INACTIVITY_TIMEOUT)
    }

    private fun lockAppPin() {
        showPinLock()
    }

    private fun lockApp(msg: String = "Verification Required") {
        tvLockMessage?.text = msg
        isLocked = true
        isPinLocked = false
        mainContainer?.visibility = View.GONE
        pinContainer?.visibility = View.GONE
        lockContainer?.visibility = View.VISIBLE
        etUsername?.setText("")
        etPassword?.setText("")
        pollHandler.removeCallbacks(pollRunnable)
        displayPackages()
    }

    private fun displayPackages() {
        packagesContainer?.visibility = View.VISIBLE
        tvPackagesLoading?.visibility = View.GONE
        
        val childCount = packagesContainer?.childCount ?: 0
        if (childCount > 1) {
            packagesContainer?.removeViews(1, childCount - 1)
        }

        val packagesList = listOf(
            mapOf("name" to "1 Device", "price" to "Ksh 300/mo", "desc" to "Perfect for single shops"),
            mapOf("name" to "5 Devices", "price" to "Ksh 500/mo", "desc" to "Best for multiple branches"),
            mapOf("name" to "3 Devices Lifetime", "price" to "Contact for pricing", "desc" to "Pay once, use forever"),
            mapOf("name" to "5 Devices Lifetime", "price" to "Contact for pricing", "desc" to "Pay once, use forever"),
            mapOf("name" to "Up to 10 Devices Lifetime", "price" to "Contact for pricing", "desc" to "For medium enterprises"),
            mapOf("name" to "Up to 20 Devices Lifetime", "price" to "Contact for pricing", "desc" to "For large enterprises")
        )

        for (pkg in packagesList) {
            val name = pkg["name"] ?: ""
            val price = pkg["price"] ?: ""
            val desc = pkg["desc"] ?: ""
            
            val card = LinearLayout(this@MainActivity).apply {
                orientation = LinearLayout.VERTICAL
                layoutParams = LinearLayout.LayoutParams(
                    LinearLayout.LayoutParams.MATCH_PARENT,
                    LinearLayout.LayoutParams.WRAP_CONTENT
                ).apply {
                    setMargins(0, 0, 0, 32)
                }
                
                val shape = android.graphics.drawable.GradientDrawable()
                shape.shape = android.graphics.drawable.GradientDrawable.RECTANGLE
                shape.setColor(android.graphics.Color.WHITE)
                shape.cornerRadius = 24f
                shape.setStroke(2, android.graphics.Color.parseColor("#E5E7EB"))
                background = shape
                
                elevation = 8f
                setPadding(48, 48, 48, 48)
            }

            val tvName = TextView(this@MainActivity).apply {
                text = name
                textSize = 18f
                setTypeface(null, android.graphics.Typeface.BOLD)
                setTextColor(android.graphics.Color.parseColor("#111827"))
            }
            val tvPrice = TextView(this@MainActivity).apply {
                text = price
                textSize = 16f
                setTypeface(null, android.graphics.Typeface.BOLD)
                setTextColor(android.graphics.Color.parseColor("#059669"))
                setPadding(0, 12, 0, 12)
            }
            val tvDesc = TextView(this@MainActivity).apply {
                text = desc
                textSize = 14f
                setTextColor(android.graphics.Color.parseColor("#6B7280"))
            }

            card.addView(tvName)
            card.addView(tvPrice)
            card.addView(tvDesc)

            packagesContainer?.addView(card)
        }
    }

    private fun unlockApp() {
        isLocked = false
        isPinLocked = false
        lockContainer?.visibility = View.GONE
        pinContainer?.visibility = View.GONE
        mainContainer?.visibility = View.VISIBLE
        resetInactivityTimer()
        pollHandler.postDelayed(pollRunnable, 15000L) // Start polling
    }

    private fun checkSmsPermissions() {
        val granted = ContextCompat.checkSelfPermission(
            this, Manifest.permission.RECEIVE_SMS
        ) == PackageManager.PERMISSION_GRANTED

        if (granted) {
            tvStatus?.text = "Status: Listening for M-Pesa SMS 🟢"
            appendLog("SMS permission granted. Ready to listen.")
        } else {
            tvStatus?.text = "Status: Requesting SMS permission..."
            ActivityCompat.requestPermissions(
                this,
                arrayOf(Manifest.permission.RECEIVE_SMS, Manifest.permission.READ_SMS),
                SMS_PERMISSION_CODE
            )
        }
    }

    override fun onRequestPermissionsResult(
        requestCode: Int,
        permissions: Array<out String>,
        grantResults: IntArray
    ) {
        super.onRequestPermissionsResult(requestCode, permissions, grantResults)
        if (requestCode == SMS_PERMISSION_CODE) {
            if (grantResults.isNotEmpty() && grantResults[0] == PackageManager.PERMISSION_GRANTED) {
                tvStatus?.text = "Status: Listening for M-Pesa SMS 🟢"
                appendLog("SMS permission granted.")
            } else {
                tvStatus?.text = "Status: SMS Permission DENIED 🔴"
                appendLog("ERROR: SMS permission was denied! App cannot work without it.")
            }
        }
    }

    fun appendLog(msg: String) {
        try {
            val time = SimpleDateFormat("HH:mm:ss", Locale.US).format(Date())
            runOnUiThread {
                try {
                    tvLogs?.append("[$time] $msg\n")
                    scrollLogs?.post { scrollLogs?.fullScroll(ScrollView.FOCUS_DOWN) }
                } catch (_: Exception) {}
            }
        } catch (_: Exception) {}
    }

    private fun testConnection() {
        val prefs   = getSharedPreferences("AppPrefs", Context.MODE_PRIVATE)
        val apiUrl  = prefs.getString("API_URL", "")?.trim() ?: ""
        val storeId = prefs.getString("STORE_ID", "")?.trim() ?: ""
        val token   = prefs.getString("AUTH_TOKEN", "")?.trim() ?: ""
        var dbUrl   = prefs.getString("TURSO_URL", "")?.trim() ?: ""
        val dbToken = prefs.getString("TURSO_TOKEN", "")?.trim() ?: ""

        if (apiUrl.isNotEmpty()) {
            var endpoint = apiUrl
                .replace("/api/mpesa-notify", "")
                .replace("/api/sync-sms", "")
                .trimEnd('/')
            endpoint += "/api/mpesa-notify"
            appendLog("Testing POS API: $endpoint")

            val jsonObj = org.json.JSONObject().apply {
                put("transaction_code", "TEST" + (1000..9999).random())
                put("amount", 100)
                put("sender", "Test User")
                put("phone", "0700000000")
                put("store_id", storeId)
                put("token", token)
                put("url", dbUrl)
                put("db_token", dbToken)
                put("test", true)
            }
            sendHttpPost(endpoint, jsonObj.toString(), "POS API", secureExit = true)
            return
        }

        if (dbUrl.isEmpty()) {
            appendLog("ERROR: Enter a Payment API URL (or Turso URL) and save first.")
            return
        }
        dbUrl = dbUrl.replace("libsql://", "https://")
        if (!dbUrl.startsWith("http")) dbUrl = "https://$dbUrl"

        appendLog("Testing Turso direct: $dbUrl")
        val body = """{"requests":[{"type":"execute","stmt":{"sql":"SELECT 1"}}]}"""
        sendHttpPost("$dbUrl/v2/pipeline", body, "Turso", secureExit = true, authHeader = "Bearer $dbToken")
    }

    private fun sendHttpPost(
        url: String,
        body: String,
        label: String,
        secureExit: Boolean = false,
        authHeader: String = ""
    ) {
        try {
            val reqBuilder = Request.Builder()
                .url(url)
                .post(body.toRequestBody("application/json".toMediaType()))
            if (authHeader.isNotEmpty()) reqBuilder.addHeader("Authorization", authHeader)

            OkHttpClient().newCall(reqBuilder.build()).enqueue(object : Callback {
                override fun onFailure(call: Call, e: IOException) {
                    appendLog("$label FAILED: ${e.message}")
                }

                override fun onResponse(call: Call, response: Response) {
                    val respBody = response.body?.string() ?: "(empty)"
                    response.close()

                    if (response.isSuccessful) {
                        appendLog("$label SUCCESS 🟢 (HTTP ${response.code})")
                        appendLog("Response: $respBody")

                        if (secureExit) {
                            runOnUiThread {
                                Toast.makeText(
                                    this@MainActivity,
                                    "🟢 Connected!",
                                    Toast.LENGTH_LONG
                                ).show()
                            }
                        }
                    } else {
                        appendLog("$label ERROR HTTP ${response.code}: $respBody")
                    }
                }
            })
        } catch (e: Exception) {
            appendLog("$label request error: ${e.message}")
        }
    }

    private fun showPinLock() {
        if (!getSharedPreferences("AppPrefs", Context.MODE_PRIVATE).getBoolean("IS_ACTIVATED", false)) return
        isPinLocked = true
        mainContainer?.visibility = View.GONE
        lockContainer?.visibility = View.GONE
        pinContainer?.visibility = View.VISIBLE
        etUnlockPin?.setText("")
    }

    private fun hidePinLock() {
        isPinLocked = false
        pinContainer?.visibility = View.GONE
        mainContainer?.visibility = View.VISIBLE
        resetInactivityTimer()
    }

    override fun onPause() {
        super.onPause()
        lastPauseTime = System.currentTimeMillis()
        pollHandler.removeCallbacks(pollRunnable)
    }
    
    override fun onResume() {
        super.onResume()
        val timeAway = System.currentTimeMillis() - lastPauseTime
        val isActivated = getSharedPreferences("AppPrefs", Context.MODE_PRIVATE).getBoolean("IS_ACTIVATED", false)
        
        if (isActivated && lastPauseTime > 0 && timeAway > 5000 && !isPinLocked) {
            showPinLock()
        }
        
        if (isActivated && !isPinLocked) {
            checkRemoteLockStatus()
            pollHandler.postDelayed(pollRunnable, 15000L)
        }
    }
    
    private fun checkRemoteLockStatus() {
        val prefs = getSharedPreferences("AppPrefs", Context.MODE_PRIVATE)
        val user = prefs.getString("PROFILE_USER", "") ?: ""
        val pass = prefs.getString("PROFILE_PASS", "") ?: ""
        val dbUrl = prefs.getString("TURSO_URL", "") ?: ""
        val dbToken = prefs.getString("TURSO_TOKEN", "") ?: ""
        val deviceId = android.provider.Settings.Secure.getString(contentResolver, android.provider.Settings.Secure.ANDROID_ID)
        
        if (user.isEmpty() || pass.isEmpty()) return
        
        val finalUrl = "https://softlybuiltserverpos.netlify.app/.netlify/functions/verify-license"
        
        try {
            val payload = org.json.JSONObject().apply {
                put("username", user)
                put("password", pass)
                put("device_id", deviceId)
                put("db_url", dbUrl)
                put("db_token", dbToken)
            }
            val req = okhttp3.Request.Builder()
                .url(finalUrl)
                .post(payload.toString().toRequestBody("application/json".toMediaType()))
                .build()
                
            okhttp3.OkHttpClient().newCall(req).enqueue(object : okhttp3.Callback {
                override fun onFailure(call: okhttp3.Call, e: java.io.IOException) {}
                override fun onResponse(call: okhttp3.Call, response: okhttp3.Response) {
                    val respStr = response.body?.string() ?: ""
                    if (!response.isSuccessful && (respStr.contains("License is inactive") || respStr.contains("Invalid user"))) {
                        runOnUiThread {
                            prefs.edit().putBoolean("IS_ACTIVATED", false).apply()
                            lockApp("Your license has expired or is inactive. Please pay to renew and receive your activation credentials.")
                            Toast.makeText(this@MainActivity, "Admin Remotely Locked this profile.", Toast.LENGTH_LONG).show()
                        }
                    }
                }
            })
        } catch (e: Exception) {}
    }

    override fun onDestroy() {
        super.onDestroy()
        mainHandler.removeCallbacksAndMessages(null)
        inactivityHandler.removeCallbacksAndMessages(null)
        pollHandler.removeCallbacksAndMessages(null)
        etApiUrl    = null
        etStoreId   = null
        etAuthToken = null
        etDbUrl     = null
        etDbToken   = null
        try { unregisterReceiver(logReceiver) } catch (_: Exception) {}
    }
}
