RISK_CATEGORIES = {

    "data_sharing": {
        "weight": 5,
        "keywords": [
            "share your data",
            "third party",
            "sell your information",
            "affiliated companies",
            "partners",
            "transfer information",
            "disclose information",
            "monetize your data"
        ],
        "semantic_templates": [
            "We may disclose your personal information to external partners.",
            "User data may be transferred to affiliated companies.",
            "Information may be shared with third party partners.",
            "We may share your data with advertising partners."
        ],
        "explanation": "This clause allows sharing of personal data with external or affiliated entities."
    },

    "arbitration": {
        "weight": 5,
        "keywords": [
            "binding arbitration",
            "class action waiver",
            "waive any right",
            "jury trial",
            "dispute resolution",
            "individual basis"
        ],
        "semantic_templates": [
            "You agree to resolve disputes through binding arbitration.",
            "You waive the right to participate in class action lawsuits.",
            "Claims must be brought individually.",
            "Disputes will be resolved outside court."
        ],
        "explanation": "This clause forces disputes to be resolved outside court and limits legal rights."
    },

    "governing_law": {
        "weight": 3,
        "keywords": [
            "exclusive jurisdiction",
            "submit to jurisdiction",
            "courts located in",
            "governed by the laws of",
            "legal proceedings shall be conducted"
        ],
        "semantic_templates": [
            "This agreement is governed by the laws of a specific jurisdiction.",
            "Legal actions must be filed in specific courts.",
            "The parties submit to the jurisdiction of certain courts."
        ],
        "explanation": "This clause determines which jurisdiction's laws apply to disputes."
    },

    "content_ownership": {
        "weight": 4,
        "keywords": [
            "royalty free",
            "perpetual license",
            "irrevocable license",
            "transferable license",
            "sublicensable",
            "worldwide license",
            "use your content"
        ],
        "semantic_templates": [
            "You grant us a perpetual license to use your content.",
            "The company may host, use, and distribute your uploaded content.",
            "Uploaded content may be reproduced or modified by the company."
        ],
        "explanation": "This clause gives the company rights to use or distribute content uploaded by users."
    },

    "unilateral_changes": {
        "weight": 4,
        "keywords": [
            "modify these terms",
            "change at any time",
            "sole discretion",
            "without prior notice",
            "updated terms"
        ],
        "semantic_templates": [
            "We reserve the right to modify this agreement at any time.",
            "Terms may be updated without prior notice.",
            "Continued use means acceptance of modified policies."
        ],
        "explanation": "The company may change the agreement without user approval."
    },

    "auto_renewal": {
        "weight": 4,
        "keywords": [
            "auto renew",
            "automatic renewal",
            "recurring payment",
            "subscription continues",
            "renew automatically"
        ],
        "semantic_templates": [
            "Subscriptions automatically renew unless cancelled.",
            "Recurring payments will be charged periodically.",
            "Fees will be automatically charged after each billing cycle."
        ],
        "explanation": "This clause may automatically renew subscriptions and charge users."
    },

    "limited_liability": {
        "weight": 3,
        "keywords": [
            "not liable",
            "limitation of liability",
            "no responsibility",
            "as is",
            "disclaim all warranties"
        ],
        "semantic_templates": [
            "Services are provided on an as-is basis.",
            "The company is not liable for damages.",
            "Liability for losses is limited."
        ],
        "explanation": "This clause limits the company’s legal responsibility for damages."
    },

    "cookies_tracking": {
        "weight": 3,
        "keywords": [
            "cookies",
            "tracking technologies",
            "analytics",
            "usage statistics",
            "log files"
        ],
        "semantic_templates": [
            "Cookies may be used to track user activity.",
            "Analytics tools collect usage data.",
            "Tracking technologies monitor how users interact with the service."
        ],
        "explanation": "This clause allows tracking of user activity through cookies or analytics."
    },

    "monitoring_notifications": {
        "weight": 2,
        "keywords": [
            "push notifications",
            "send notifications",
            "alerts",
            "monitor activity"
        ],
        "semantic_templates": [
            "The app may send push notifications.",
            "Users may receive alerts regarding account activity.",
            "The platform may monitor usage activity."
        ],
        "explanation": "This clause allows monitoring of user activity or sending system notifications."
    },

    "account_control": {
        "weight": 3,
        "keywords": [
            "terminate your account",
            "suspend your account",
            "remove your content",
            "account suspension",
            "account termination"
        ],
        "semantic_templates": [
            "We may suspend or terminate your account.",
            "Content may be removed if it violates guidelines.",
            "Accounts may be restricted by the platform."
        ],
        "explanation": "The platform can suspend accounts or remove user content."
    },

    "payment_access": {
        "weight": 4,
        "keywords": [
            "payment information",
            "credit card",
            "billing details",
            "financial information"
        ],
        "semantic_templates": [
            "Your payment details may be stored.",
            "Credit card information may be processed.",
            "Billing information may be collected."
        ],
        "explanation": "The service may access or process financial information."
    },

    "device_permissions": {
        "weight": 4,
        "keywords": [
            "camera access",
            "microphone access",
            "location data",
            "gps location",
            "access your contacts",
            "read your contacts",
            "device storage",
            "access photos",
            "access media files"
        ],
        "semantic_templates": [
            "The application may access your device camera.",
            "Location information may be collected from your device.",
            "The app may access contacts or address book.",
            "The service may access photos or files stored on your device."
        ],
        "explanation": "This clause allows access to device hardware or personal data such as camera, contacts, or location."
    }

}