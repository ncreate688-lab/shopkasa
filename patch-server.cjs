const fs = require('fs');

const path = 'c:\\Softly built updates\\license-server\\netlify\\functions\\verify-license.js';
let content = fs.readFileSync(path, 'utf8');

const newVerifyLogic = `exports.handler = async function (event, context) {
    if (event.httpMethod === 'OPTIONS') {
        return {
            statusCode: 200,
            headers: {
                'Access-Control-Allow-Origin': '*',
                'Access-Control-Allow-Headers': 'Content-Type',
                'Access-Control-Allow-Methods': 'POST, OPTIONS'
            },
            body: ''
        };
    }

    if (event.httpMethod !== 'POST') {
        return { statusCode: 405, body: 'Method Not Allowed' };
    }

    try {
        const { username, password, device_id, db_url, db_token } = JSON.parse(event.body);

        if (!username || !password || !device_id) {
            return {
                statusCode: 400,
                headers: { 'Access-Control-Allow-Origin': '*' },
                body: JSON.stringify({ success: false, message: 'Missing username, password, or device_id' })
            };
        }

        const TURSO_URL = db_url || process.env.TURSO_LICENSE_URL || 'libsql://sms-forwarder-pos-success.aws-ap-northeast-1.turso.io';
        const TURSO_TOKEN = db_token || process.env.TURSO_LICENSE_TOKEN || '';
        
        if (!TURSO_TOKEN) {
            return {
                statusCode: 500,
                headers: { 'Access-Control-Allow-Origin': '*' },
                body: JSON.stringify({ success: false, message: 'Server database configuration missing.' })
            };
        }

        const dbUrl = \`https://\${TURSO_URL.replace('libsql://', '')}/v2/pipeline\`;

        // 1. Fetch license
        const fetchReq = {
            requests: [
                {
                    type: "execute",
                    stmt: {
                        sql: "SELECT * FROM licenses WHERE username = ? AND password = ?",
                        args: [{ type: "text", value: username }, { type: "text", value: password }]
                    }
                }
            ]
        };

        const fetchRes = await fetch(dbUrl, {
            method: 'POST',
            headers: {
                'Authorization': \`Bearer \${TURSO_TOKEN}\`,
                'Content-Type': 'application/json'
            },
            body: JSON.stringify(fetchReq)
        });

        const fetchData = await fetchRes.json();
        
        // If Turso returns a direct error message
        if (fetchData.message) {
            return {
                statusCode: 500,
                headers: { 'Access-Control-Allow-Origin': '*' },
                body: JSON.stringify({ success: false, message: \`Database Error: \${fetchData.message}\` })
            };
        }
        
        if (fetchData.error) {
            return {
                statusCode: 500,
                headers: { 'Access-Control-Allow-Origin': '*' },
                body: JSON.stringify({ success: false, message: \`Database Error: \${fetchData.error.message || fetchData.error}\` })
            };
        }

        if (!fetchData.results || !fetchData.results[0] || !fetchData.results[0].response || !fetchData.results[0].response.result.rows || fetchData.results[0].response.result.rows.length === 0) {
            return {
                statusCode: 401,
                headers: { 'Access-Control-Allow-Origin': '*' },
                body: JSON.stringify({ success: false, message: 'Invalid user or password' })
            };
        }

        const cols = fetchData.results[0].response.result.cols.map(c => c.name);
        const row = fetchData.results[0].response.result.rows[0];
        const license = {};
        cols.forEach((c, i) => license[c] = row[i].value);

        if (license.status !== 'active') {
            return {
                statusCode: 403,
                headers: { 'Access-Control-Allow-Origin': '*' },
                body: JSON.stringify({ success: false, message: 'License is inactive' })
            };
        }

        let deviceIds = [];
        try {
            deviceIds = license.device_ids ? JSON.parse(license.device_ids) : [];
        } catch (e) {
            deviceIds = [];
        }

        // If this device is already activated on this license, allow it immediately
        if (deviceIds.includes(device_id)) {
            return {
                statusCode: 200,
                headers: { 'Access-Control-Allow-Origin': '*' },
                body: JSON.stringify({ success: true, message: 'Device already activated', plan: license.plan_name })
            };
        }

        // Check if there are slots available
        if (deviceIds.length >= parseInt(license.total_devices, 10)) {
            return {
                statusCode: 403,
                headers: { 'Access-Control-Allow-Origin': '*' },
                body: JSON.stringify({ success: false, message: 'Maximum devices reached for this license' })
            };
        }

        // Add device and update
        deviceIds.push(device_id);

        const updateReq = {
            requests: [
                {
                    type: "execute",
                    stmt: {
                        sql: "UPDATE licenses SET device_ids = ? WHERE username = ?",
                        args: [{ type: "text", value: JSON.stringify(deviceIds) }, { type: "text", value: username }]
                    }
                }
            ]
        };

        const updateRes = await fetch(dbUrl, {
            method: 'POST',
            headers: {
                'Authorization': \`Bearer \${TURSO_TOKEN}\`,
                'Content-Type': 'application/json'
            },
            body: JSON.stringify(updateReq)
        });

        return {
            statusCode: 200,
            headers: { 'Access-Control-Allow-Origin': '*' },
            body: JSON.stringify({ 
                success: true, 
                message: 'Device activated successfully',
                plan: license.plan_name,
                devices_used: deviceIds.length,
                devices_total: parseInt(license.total_devices, 10)
            })
        };

    } catch (err) {
        console.error(err);
        return {
            statusCode: 500,
            headers: { 'Access-Control-Allow-Origin': '*' },
            body: JSON.stringify({ success: false, message: 'Internal server error: ' + err.message })
        };
    }
};`;

fs.writeFileSync(path, newVerifyLogic, 'utf8');
console.log("verify-license.js updated");
