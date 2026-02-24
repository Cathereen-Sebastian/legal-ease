RISK_CATEGORIES = {
    "data_sharing": {
        "weight": 5,
        "keywords": [
            "share your data", "third party", "sell your information", 
            "meta companies", "affiliated companies", "partners", 
            "transfer information", "disclose information"
        ],
        "semantic_templates": [
            "We may disclose your personal information to external partners.",
            "User data may be transferred to affiliated companies.",
            "Information is shared across corporate entities for advertising.",
            "We work with partners and service providers to share user data."
        ],
        "explanation": "This clause allows sharing of personal data with external or affiliated entities."
    },

    "arbitration": {
        "weight": 5,
        "keywords": [
            "binding arbitration", "class action waiver", "waive any right", 
            "jury trial", "dispute resolution", "individual basis"
        ],
        "semantic_templates": [
            "You agree to resolve all disputes through binding individual arbitration.",
            "You waive your right to participate in class action lawsuits.",
            "Claims must be brought only on your own behalf.",
            "You waive the right to have disputes decided by a judge or jury."
        ],
        "explanation": "This clause forces you to settle disputes outside of court and prevents group lawsuits."
    },

    "auto_renewal": {
        "weight": 4,
        "keywords": [
            "auto renew", "automatic renewal", "recurring payment", 
            "subscription continues", "cancelled"
        ],
        "semantic_templates": [
            "Your subscription continues unless cancelled.",
            "The service renews automatically after each billing cycle.",
            "Fees are automatically charged to your chosen payment method."
        ],
        "explanation": "This clause may renew services and charge fees without explicit reconfirmation."
    },

    "limited_liability": {
        "weight": 3,
        "keywords": [
            "not liable", "no responsibility", "limitation of liability", 
            "as is", "disclaimers", "maximum extent permitted"
        ],
        "semantic_templates": [
            "We are not responsible for damages arising from use.",
            "The company disclaims liability for losses.",
            "Services are provided on an as-is and as-available basis.",
            "Our total liability shall not exceed a specified amount."
        ],
        "explanation": "This clause limits the company's legal responsibility and your ability to sue for damages."
    }
}