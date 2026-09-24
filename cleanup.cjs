const fs = require('fs');

const ktPath = 'c:\\Softly built updates\\MpesaListenerApp\\app\\src\\main\\java\\com\\softbuild\\mpesalistener\\MainActivity.kt';
let ktContent = fs.readFileSync(ktPath, 'utf8');

// The file currently has duplicate methods. We can just use a regex to strip EVERYTHING after the first occurrence of `private fun showPinLock()` that shouldn't be there, 
// or simply use the fact that they are at the end of the file.

const marker = "    private fun showPinLock() {";
const firstIndex = ktContent.indexOf(marker);

if (firstIndex !== -1) {
    // We only want ONE instance of the new methods. 
    // They start at the marker. 
    ktContent = ktContent.substring(0, firstIndex);
}

// Ensure the class is closed
if (!ktContent.trim().endsWith("}")) {
    ktContent += "\n}\n";
}

// Now re-add the new methods correctly inside the class!
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

ktContent = ktContent.replace(/}\s*$/, '\n' + newMethods + '\n}\n');

fs.writeFileSync(ktPath, ktContent, 'utf8');
console.log("Cleaned up MainActivity duplicate methods!");
