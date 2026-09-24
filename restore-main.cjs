const fs = require('fs');

const ktPath = 'c:\\Softly built updates\\MpesaListenerApp\\app\\src\\main\\java\\com\\softbuild\\mpesalistener\\MainActivity.kt';
let ktContent = fs.readFileSync(ktPath, 'utf8');

// 1. Replace validPins
ktContent = ktContent.replace(/private val validPins[\s\S]*?\)/, '');

// 2. Replace etPin with etUsername and etPassword
ktContent = ktContent.replace('private var etPin: EditText? = null', 'private var etUsername: EditText? = null\n    private var etPassword: EditText? = null');
ktContent = ktContent.replace('etPin         = findViewById(R.id.etPin)', 'etUsername = findViewById(R.id.etUsername)\n            etPassword = findViewById(R.id.etPassword)');

// 3. Replace lockApp and unlockApp etPin reset
ktContent = ktContent.replace('etPin?.setText("")', 'etUsername?.setText("")\n        etPassword?.setText("")');

// 4. Replace btnUnlock logic
const oldBtnUnlockRegex = /btnUnlock\?\.setOnClickListener \{[\s\S]*?etPin\?\.setText\(""\)\s*\}/;
const newBtnUnlockLogic = `btnUnlock?.setOnClickListener {
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
                                Toast.makeText(this@MainActivity, "Network Error: \${e.message}", Toast.LENGTH_LONG).show()
                            }
                        }
                        override fun onResponse(call: okhttp3.Call, response: okhttp3.Response) {
                            val respStr = response.body?.string() ?: ""
                            runOnUiThread {
                                btnUnlock?.text = "Activate Device"
                                btnUnlock?.isEnabled = true
                                if (response.isSuccessful && respStr.contains("\\"success\\":true")) {
                                    getSharedPreferences("AppPrefs", android.content.Context.MODE_PRIVATE).edit().putBoolean("IS_ACTIVATED", true).putString("PROFILE_USER", user).putString("PROFILE_PASS", pass).apply()
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
console.log("Restored btnUnlock logic!");
