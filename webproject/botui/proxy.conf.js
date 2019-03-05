const PROXY_CONFIG = [
    {
        context: [
            "/webhooks",
        ],
        target: "http://localhost:5002",
        secure: false
    }
]

module.exports = PROXY_CONFIG;