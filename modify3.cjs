const fs = require('fs');
const path = 'c:\\Softly built updates\\MpesaListenerApp\\app\\src\\main\\java\\com\\softbuild\\mpesalistener\\MainActivity.kt';
let content = fs.readFileSync(path, 'utf8');

// 1. Add etLicenseUrl variable declaration
content = content.replace('private var etUsername: EditText? = null', 'private var etLicenseUrl: EditText? = null\n    private var etUsername: EditText? = null');

// 2. Add etLicenseUrl findViewById and init from prefs
content = content.replace('etUsername    = findViewById(R.id.etUsername)', 'etLicenseUrl  = findViewById(R.id.etLicenseUrl)\n              etUsername    = findViewById(R.id.etUsername)\n\n              etLicenseUrl?.setText(getSharedPreferences("AppPrefs", Context.MODE_PRIVATE).getString("LICENSE_URL", "https://softlybuilt-license-server.netlify.app"))');

// 3. Update btnUnlock logic to read the URL, validate it, save it, and use it
const newBtnLogic = `btnUnlock?.setOnClickListener {
                val urlInput = etLicenseUrl?.text.toString().trim()
                val user = etUsername?.text.toString().trim()
                val pass = etPassword?.text.toString().trim()
                val deviceId = android.provider.Settings.Secure.getString(contentResolver, android.provider.Settings.Secure.ANDROID_ID)
                
                if (urlInput.isEmpty() || user.isEmpty() || pass.isEmpty()) {
                    Toast.makeText(this, "Enter URL, username, and password", Toast.LENGTH_SHORT).show()
                    return@setOnClickListener
                }
                
                var finalUrl = urlInput
                if (!finalUrl.endsWith("/verify-license")) {
                    if (!finalUrl.endsWith("/")) finalUrl += "/"
                    finalUrl += ".netlify/functions/verify-license"
                }
                
                getSharedPreferences("AppPrefs", Context.MODE_PRIVATE).edit().putString("LICENSE_URL", urlInput).apply()
                
                btnUnlock?.text = "Activating..."
                btnUnlock?.isEnabled = false
                
                try {
                    val payload = org.json.JSONObject().apply {
                        put("username", user)
                        put("password", pass)
                        put("device_id", deviceId)
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
                                Toast.makeText(this@MainActivity, "Network Error: \${e.message}", Toast.LENGTH_LONG).show()
                            }
                        }
                        override fun onResponse(call: okhttp3.Call, response: okhttp3.Response) {
                            val respStr = response.body?.string() ?: ""
                            runOnUiThread {
                                btnUnlock?.text = "Activate Device"
                                btnUnlock?.isEnabled = true
                                if (response.isSuccessful && respStr.contains("\\"success\\":true")) {
                                    getSharedPreferences("AppPrefs", android.content.Context.MODE_PRIVATE).edit().putBoolean("IS_ACTIVATED", true).apply()
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
                    Toast.makeText(this, "Error: \${e.message}", Toast.LENGTH_LONG).show()
                }
            }`;

// Replace everything between btnUnlock?.setOnClickListener { and the next } } } block
content = content.replace(/btnUnlock\?\.setOnClickListener \{([\s\S]*?)\}\s*catch\(e: Exception\) \{\s*btnUnlock\?\.text = "Activate Device"\s*btnUnlock\?\.isEnabled = true\s*Toast\.makeText\(this, "Error:[^"]+", Toast\.LENGTH_LONG\)\.show\(\)\s*\}\s*\}/m, newBtnLogic);

fs.writeFileSync(path, content, 'utf8');
console.log("Modifications applied");
