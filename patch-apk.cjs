const fs = require('fs');

// --- Fix activity_main.xml ---
const xmlPath = 'c:\\Softly built updates\\MpesaListenerApp\\app\\src\\main\\res\\layout\\activity_main.xml';
let xmlContent = fs.readFileSync(xmlPath, 'utf8');

// Remove etLicenseUrl
xmlContent = xmlContent.replace(/<EditText\s+android:id="\@\+id\/etLicenseUrl"[\s\S]*?\/>\s*/, '');
// Change text to Verification Required
xmlContent = xmlContent.replace('Enter your Username and Password to activate this device.', 'Verification Required');

fs.writeFileSync(xmlPath, xmlContent, 'utf8');

// --- Fix MainActivity.kt ---
const ktPath = 'c:\\Softly built updates\\MpesaListenerApp\\app\\src\\main\\java\\com\\softbuild\\mpesalistener\\MainActivity.kt';
let ktContent = fs.readFileSync(ktPath, 'utf8');

// Remove etLicenseUrl var
ktContent = ktContent.replace('private var etLicenseUrl: EditText? = null\n', '');
// Remove findViewById
ktContent = ktContent.replace(/etLicenseUrl\s*=\s*findViewById\(R\.id\.etLicenseUrl\)\n/, '');
// Remove etLicenseUrl?.setText
ktContent = ktContent.replace(/etLicenseUrl\?\.setText\([\s\S]*?\)\n/, '');

// Fix btnUnlock logic
const oldBtnUnlockRegex = /btnUnlock\?\.setOnClickListener \{([\s\S]*?)\}\s*catch\(e: Exception\) \{\s*btnUnlock\?\.text = "Activate Device"[\s\S]*?\}\s*\}/;

const newBtnUnlockLogic = `btnUnlock?.setOnClickListener {
                val user = etUsername?.text.toString().trim()
                val pass = etPassword?.text.toString().trim()
                val deviceId = android.provider.Settings.Secure.getString(contentResolver, android.provider.Settings.Secure.ANDROID_ID)
                
                if (user.isEmpty() || pass.isEmpty()) {
                    Toast.makeText(this, "Enter username and password", Toast.LENGTH_SHORT).show()
                    return@setOnClickListener
                }
                
                val dbUrl = getSharedPreferences("AppPrefs", Context.MODE_PRIVATE).getString("TURSO_URL", "") ?: ""
                val dbToken = getSharedPreferences("AppPrefs", Context.MODE_PRIVATE).getString("TURSO_TOKEN", "") ?: ""
                
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

ktContent = ktContent.replace(oldBtnUnlockRegex, newBtnUnlockLogic);

fs.writeFileSync(ktPath, ktContent, 'utf8');
console.log("Android App patched");
