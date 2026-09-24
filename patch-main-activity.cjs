const fs = require('fs');
const path = 'c:\\Softly built updates\\MpesaListenerApp\\app\\src\\main\\java\\com\\softbuild\\mpesalistener\\MainActivity.kt';
let content = fs.readFileSync(path, 'utf8');

// 1. Add class variables
const varsToAdd = `
    private var pinContainer: LinearLayout? = null
    private var etUnlockPin: EditText? = null
    private var btnUnlockPin: Button? = null
    private var btnManualLock: Button? = null
    private var lastPauseTime: Long = 0
    private var isPinLocked = false
`;
content = content.replace('private var btnUnlock: Button? = null', 'private var btnUnlock: Button? = null' + varsToAdd);

// 2. Add findViewById inside onCreate
const findViewsToAdd = `
            pinContainer = findViewById(R.id.pinContainer)
            etUnlockPin = findViewById(R.id.etUnlockPin)
            btnUnlockPin = findViewById(R.id.btnUnlockPin)
            btnManualLock = findViewById(R.id.btnManualLock)
`;
content = content.replace('btnUnlock     = findViewById(R.id.btnUnlock)', 'btnUnlock     = findViewById(R.id.btnUnlock)' + findViewsToAdd);

// 3. Update btnUnlock success block to save PROFILE_USER and PROFILE_PASS
content = content.replace(
    'getSharedPreferences("AppPrefs", android.content.Context.MODE_PRIVATE).edit().putBoolean("IS_ACTIVATED", true).apply()',
    'getSharedPreferences("AppPrefs", android.content.Context.MODE_PRIVATE).edit().putBoolean("IS_ACTIVATED", true).putString("PROFILE_USER", user).putString("PROFILE_PASS", pass).apply()'
);

// 4. Add btnManualLock and btnUnlockPin listeners
const listenersToAdd = `
            btnManualLock?.setOnClickListener {
                showPinLock()
            }
            
            btnUnlockPin?.setOnClickListener {
                val pin = etUnlockPin?.text.toString().trim()
                val savedPin = getSharedPreferences("AppPrefs", Context.MODE_PRIVATE).getString("PROFILE_PASS", "") ?: ""
                if (pin == savedPin) {
                    hidePinLock()
                    Toast.makeText(this, "App Unlocked", Toast.LENGTH_SHORT).show()
                } else {
                    Toast.makeText(this, "Incorrect Password/PIN", Toast.LENGTH_SHORT).show()
                }
            }
`;
content = content.replace('btnClear.setOnClickListener {', listenersToAdd + '\n            btnClear.setOnClickListener {');

// 5. Update lockApp to hide pinContainer
content = content.replace('mainContainer?.visibility = View.GONE', 'mainContainer?.visibility = View.GONE\n        pinContainer?.visibility = View.GONE');
// 6. Update unlockApp to hide pinContainer
content = content.replace('lockContainer?.visibility = View.GONE', 'lockContainer?.visibility = View.GONE\n        pinContainer?.visibility = View.GONE\n        isPinLocked = false');

// 7. Add new methods at the end of the class
const newMethods = `
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
    }

    override fun onPause() {
        super.onPause()
        lastPauseTime = System.currentTimeMillis()
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
                            lockApp()
                            Toast.makeText(this@MainActivity, "Admin Remotely Locked this profile.", Toast.LENGTH_LONG).show()
                        }
                    }
                }
            })
        } catch (e: Exception) {}
    }
`;

// Remove the /m flag to match the absolute end of the file string instead of end of any line
content = content.replace(/}\s*$/, '\n' + newMethods + '\n}\n');

fs.writeFileSync(path, content, 'utf8');
console.log("MainActivity updated correctly");
