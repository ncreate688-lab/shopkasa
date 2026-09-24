package com.softbuild.mpesalistener

import android.content.BroadcastReceiver
import android.content.Context
import android.content.Intent
import android.provider.Telephony
import android.util.Log
import okhttp3.Call
import okhttp3.Callback
import okhttp3.MediaType.Companion.toMediaType
import okhttp3.OkHttpClient
import okhttp3.Request
import okhttp3.RequestBody.Companion.toRequestBody
import okhttp3.Response
import org.json.JSONObject
import java.io.IOException
import java.text.SimpleDateFormat
import java.util.Date
import java.util.Locale
import java.util.TimeZone

class SmsReceiver : BroadcastReceiver() {
    private val client = OkHttpClient()

    override fun onReceive(context: Context, intent: Intent) {
        if (intent.action == Telephony.Sms.Intents.SMS_RECEIVED_ACTION) {
            val messages = Telephony.Sms.Intents.getMessagesFromIntent(intent)
            val prefs = context.getSharedPreferences("AppPrefs", Context.MODE_PRIVATE)
            val customSender = (prefs.getString("CUSTOM_SENDER", "") ?: "").trim()
            val customTemplate = (prefs.getString("CUSTOM_TEMPLATE", "") ?: "").trim()

            for (sms in messages) {
                val sender = sms.displayOriginatingAddress
                val body = sms.displayMessageBody
                
                if (sender != null) {
                    var processed = false
                    
                    // 1. Try Custom Template First
                    if (customSender.isNotEmpty() && customTemplate.isNotEmpty() && sender.equals(customSender, ignoreCase = true)) {
                        processed = processCustomSms(context, body, customTemplate)
                    }

                    // 2. Fallback to default MPESA if not processed
                    if (!processed && sender.equals("MPESA", ignoreCase = true)) {
                        processMpesaSms(context, body)
                    }
                }
            }
        }
    }

    private fun processCustomSms(context: Context, sms: String, template: String): Boolean {
        try {
            // Find order of placeholders in the original template to know which group is which
            val placeholders = listOf("[TX]", "[AMOUNT]", "[PHONE]", "[NAME]")
            val positions = placeholders.map { it to template.indexOf(it) }
                .filter { it.second != -1 }
                .sortedBy { it.second }
                .map { it.first }

            // Escape special regex chars in template but keep our brackets intact
            var regexStr = Regex.escape(template)
            
            // Replace escaped placeholders with capture groups (unnamed for API < 26 safety)
            regexStr = regexStr.replace("\\[TX\\]", "([A-Za-z0-9]+)")
            regexStr = regexStr.replace("\\[AMOUNT\\]", "([0-9,.]+)")
            regexStr = regexStr.replace("\\[PHONE\\]", "([0-9+]+)")
            regexStr = regexStr.replace("\\[NAME\\]", "([A-Za-z \\-]+)")
            
            // Convert any literal spaces in the template to \s+ to be flexible
            regexStr = regexStr.replace("\\ ", "\\s+")
            
            val regex = Regex(regexStr, RegexOption.IGNORE_CASE)
            val match = regex.find(sms)
            
            if (match != null) {
                var txCode = ""
                var amount = 0.0
                var phone = "Unknown"
                var name = "Unknown"

                for ((index, placeholder) in positions.withIndex()) {
                    val groupValue = match.groupValues.getOrNull(index + 1) ?: continue
                    when (placeholder) {
                        "[TX]" -> txCode = groupValue
                        "[AMOUNT]" -> amount = groupValue.replace(",", "").toDoubleOrNull() ?: 0.0
                        "[PHONE]" -> phone = groupValue.trim()
                        "[NAME]" -> name = groupValue.trim()
                    }
                }
                
                if (txCode.isNotEmpty() && amount > 0) {
                    postToBackend(context, txCode, amount, name, phone)
                    return true
                }
            }
        } catch (e: Exception) {
            Log.e("SMS_PARSER", "Error parsing custom template: ${e.message}")
        }
        return false
    }

    private fun processMpesaSms(context: Context, sms: String) {
        val txCodeRegex = Regex("^[A-Z0-9]{8,15}")
        val amountRegex = Regex("(?i)Kshs?\\s*([0-9,]+\\.?[0-9]*)")
        
        // Try Phone then Name (e.g. 2547... CAROLINE)
        val fromRegex1 = Regex("(?i)(?:received from|paid to|from)\\s+([\\d+]+)\\s+([A-Za-z\\s]+)(?:\\.|New|\\d)")
        // Try Name then Phone (e.g. CAROLINE 2547...)
        val fromRegex2 = Regex("(?i)(?:received from|paid to|from)\\s+([A-Za-z\\s]+)\\s+([\\d+]+)(?:\\.|New|\\d)")

        val txMatch = txCodeRegex.find(sms)
        val amtMatch = amountRegex.find(sms)
        val fromMatch1 = fromRegex1.find(sms)
        val fromMatch2 = fromRegex2.find(sms)

        if (txMatch != null && amtMatch != null) {
            val txCode = txMatch.value
            val amountStr = amtMatch.groupValues[1].replace(",", "")
            val amount = amountStr.toDoubleOrNull() ?: 0.0
            
            var name = "Unknown"
            var phone = "Unknown"
            
            if (fromMatch1 != null) {
                phone = fromMatch1.groupValues[1].trim()
                name = fromMatch1.groupValues[2].trim()
            } else if (fromMatch2 != null) {
                name = fromMatch2.groupValues[1].trim()
                phone = fromMatch2.groupValues[2].trim()
            }

            postToBackend(context, txCode, amount, name, phone)
        }
    }

    private fun postToBackend(context: Context, txCode: String, amount: Double, name: String, phone: String) {
        val prefs = context.getSharedPreferences("AppPrefs", Context.MODE_PRIVATE)
        val apiUrl = (prefs.getString("API_URL", "") ?: "").replace("\n", "").replace("\r", "")
        val token = (prefs.getString("AUTH_TOKEN", "") ?: "").replace("\n", "").replace("\r", "")
        val storeId = (prefs.getString("STORE_ID", "") ?: "").replace("\n", "").replace("\r", "")

        // Always resolve to /api/mpesa-notify regardless of what was entered
        var endpoint = apiUrl.trim()
            .replace("/api/mpesa-notify", "")
            .replace("/api/sync-sms", "")
            .trimEnd('/')
        endpoint += "/api/mpesa-notify"
        if (endpoint.length < 10) return

        val timestamp = SimpleDateFormat("yyyy-MM-dd'T'HH:mm:ss'Z'", Locale.US).apply {
            timeZone = TimeZone.getTimeZone("UTC")
        }.format(Date())

        val jsonObj = JSONObject().apply {
            put("transaction_code", txCode)
            put("amount", amount)
            put("sender", name)
            put("phone", phone)
            put("timestamp", timestamp)
            put("store_id", storeId)
            put("token", token)
            
            // Also send db info if configured to allow backend to know where to save
            put("url", (prefs.getString("TURSO_URL", "") ?: "").replace("\n", "").replace("\r", ""))
            put("db_token", (prefs.getString("TURSO_TOKEN", "") ?: "").replace("\n", "").replace("\r", ""))
        }

        val request = Request.Builder()
            .url(endpoint)
            .addHeader("Authorization", "Bearer $token")
            .post(jsonObj.toString().toRequestBody("application/json".toMediaType()))
            .build()

        client.newCall(request).enqueue(object : Callback {
            override fun onFailure(call: Call, e: IOException) {
                Log.e("MpesaListener", "Failed to post to backend: $e")
                // Broadcast to UI
                val intent = Intent(MainActivity.LOG_ACTION)
                intent.putExtra("log", "API Error: \${e.message}")
                context.sendBroadcast(intent)
            }
            override fun onResponse(call: Call, response: Response) {
                val msg = if (response.isSuccessful) "API Success ✓ (HTTP \${response.code})" else "API Error HTTP \${response.code}"
                Log.i("MpesaListener", msg)
                // Broadcast to UI
                val intent = Intent(MainActivity.LOG_ACTION)
                intent.putExtra("log", "$msg - Tx: $txCode")
                context.sendBroadcast(intent)
                response.close()
            }
        })
    }
}
