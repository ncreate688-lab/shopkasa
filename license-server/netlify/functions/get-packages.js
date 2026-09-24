exports.handler = async function (event, context) {
    // Handle CORS preflight requests
    if (event.httpMethod === 'OPTIONS') {
        return {
            statusCode: 200,
            headers: {
                'Access-Control-Allow-Origin': '*',
                'Access-Control-Allow-Headers': 'Content-Type',
                'Access-Control-Allow-Methods': 'GET, OPTIONS'
            },
            body: ''
        };
    }

    const packages = [
        { name: "1 Device", price: "Ksh 300/mo", description: "Perfect for single shops" },
        { name: "5 Devices", price: "Ksh 500/mo", description: "Best for multiple branches" },
        { name: "3 Devices Lifetime", price: "Contact for pricing", description: "Pay once, use forever" },
        { name: "5 Devices Lifetime", price: "Contact for pricing", description: "Pay once, use forever" },
        { name: "Up to 10 Devices Lifetime", price: "Contact for pricing", description: "For medium enterprises" },
        { name: "Up to 20 Devices Lifetime", price: "Contact for pricing", description: "For large enterprises" }
    ];

    return {
        statusCode: 200,
        headers: { 
            'Access-Control-Allow-Origin': '*',
            'Content-Type': 'application/json'
        },
        body: JSON.stringify({ success: true, packages })
    };
};
