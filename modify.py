import re

path = r'c:\Softly built updates\MpesaListenerApp\app\src\main\java\com\softbuild\mpesalistener\MainActivity.kt'
with open(path, 'r', encoding='utf-8') as f:
    content = f.read()

# 1. Replace validPins
content = re.sub(r'private val validPins = listOf\("[^"]+", "[^"]+"\)', 'private val LICENSE_API_URL = "https://YOUR-SITE-NAME.netlify.app/.netlify/functions/verify-license"', content)

# 2. Replace etPin with Username/Password
content = content.replace('private var etPin: EditText? = null', 'private var etUsername: EditText? = null\n    private var etPassword: EditText? = null')

# 3. Remove inactivity variables
content = re.sub(r'private val inactivityHandler = Handler\(Looper\.getMainLooper\(\)\)\s*private val lockRunnable = Runnable \{ lockApp\(\) \}', '', content)

# 4. Remove isLocked
content = content.replace('private var isLocked = false', '')

# 5. In onCreate, find etPin and btnUnlock bindings
content = content.replace('etPin         = findViewById(R.id.etPin)', 'etUsername    = findViewById(R.id.etUsername)\n            etPassword    = findViewById(R.id.etPassword)')

# 6. Replace btnUnlock logic
btn_logic = '''btnUnlock?.setOnClickListener {
                val user = etUsername?.text.toString().trim()
                val pass = etPassword?.text.toString().trim()
                val deviceId = android.provider.Settings.Secure.getString(contentResolver, android.provider.Settings.Secure.ANDROID_ID)
                
                if (user.isEmpty() || pass.isEmpty()) {
                    Toast.makeText(this, "Enter username and password", Toast.LENGTH_SHORT).show()
                    return@setOnClickListener
                }
                
                btnUnlock?.text = "Activating..."
                btnUnlock?.isEnabled = false
                
                try {
                    val payload = org.json.JSONObject().apply {
                        put("username", user)
                        put("password", pass)
                        put("device_id", deviceId)
                    }
                    val req = okhttp3.Request.Builder()
                        .url(LICENSE_API_URL)
                        .post(okhttp3.RequestBody.create(okhttp3.MediaType.parse("application/json"), payload.toString()))
                        .build()
                        
                    okhttp3.OkHttpClient().newCall(req).enqueue(object : okhttp3.Callback {
                        override fun onFailure(call: okhttp3.Call, e: java.io.IOException) {
                            runOnUiThread {
                                btnUnlock?.text = "Activate Device"
                                btnUnlock?.isEnabled = true
                                Toast.makeText(this@MainActivity, "Network Error", Toast.LENGTH_LONG).show()
                            }
                        }
                        override fun onResponse(call: okhttp3.Call, response: okhttp3.Response) {
                            val respStr = response.body()?.string()
                            runOnUiThread {
                                btnUnlock?.text = "Activate Device"
                                btnUnlock?.isEnabled = true
                                if (response.isSuccessful && respStr?.contains("\"success\":true") == true) {
                                    getSharedPreferences("AppPrefs", android.content.Context.MODE_PRIVATE).edit().putBoolean("IS_ACTIVATED", true).apply()
                                    unlockApp()
                                    Toast.makeText(this@MainActivity, "Activated Successfully!", Toast.LENGTH_LONG).show()
                                } else {
                                    Toast.makeText(this@MainActivity, "Activation Failed. Invalid credentials or device limit reached.", Toast.LENGTH_LONG).show()
                                }
                            }
                        }
                    })
                } catch(e: Exception) {
                    btnUnlock?.text = "Activate Device"
                    btnUnlock?.isEnabled = true
                    Toast.makeText(this, "Error: ${e.message}", Toast.LENGTH_LONG).show()
                }
            }'''

# Replace old btnUnlock?.setOnClickListener block
content = re.sub(r'btnUnlock\?\.setOnClickListener \{[^\}]+\}[^\}]+\}', btn_logic, content, count=1, flags=re.MULTILINE|re.DOTALL)

# 7. Check if activated on startup
content = content.replace('resetInactivityTimer()', 'if (!getSharedPreferences("AppPrefs", android.content.Context.MODE_PRIVATE).getBoolean("IS_ACTIVATED", false)) { lockApp() } else { unlockApp() }')

# 8. onUserInteraction - remove resetInactivityTimer
content = re.sub(r'override fun onUserInteraction\(\) \{[\s\S]+?\}\s*private fun resetInactivityTimer\(\) \{[\s\S]+?\}', '', content)

# 9. lockApp update
content = content.replace('etPin?.setText("")', 'etPassword?.setText("")')
content = content.replace('isLocked = true', '')
content = content.replace('isLocked = false', '')

# 11. Remove inactivity handler from onDestroy
content = content.replace('inactivityHandler.removeCallbacksAndMessages(null)', '')

with open(path, 'w', encoding='utf-8') as f:
    f.write(content)
print("Done")
