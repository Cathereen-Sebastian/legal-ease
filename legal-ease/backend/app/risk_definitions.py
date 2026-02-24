RISK_CATEGORIES = {
    "data_sharing": {
        "weight": 5,
        "keywords": [
            "share your data", "third party", "sell your information", 
            "meta companies", "affiliated companies", "partners", 
            "transfer information", "disclose information", "monetize"
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

    "governing_law": {
        "weight": 4,
        "keywords": [
            "governing law", "jurisdiction", "exclusive venue", 
            "laws of", "state of", "country of", "courts of"
        ],
        "semantic_templates": [
            "This agreement is governed by the laws of a specific jurisdiction.",
            "Any legal action must be brought in a court located far from the user.",
            "The parties submit to the exclusive jurisdiction of the courts of Delaware.",
            "Legal proceedings shall be conducted under the laws of Singapore."
        ],
        "explanation": "This clause determines which country or state's laws apply, making it difficult to seek justice locally."
    },

    "content_ownership": {
        "weight": 4,
        "keywords": [
            "royalty-free", "sublicensable", "transferable license", 
            "host, use, and distribute", "perpetual", "irrevocable", "worldwide license"
        ],
        "semantic_templates": [
            "You grant us a perpetual license to use and distribute your content.",
            "The company retains rights to modify and display your uploaded media.",
            "By uploading content, you provide us with a worldwide right to reproduce it."
        ],
        "explanation": "This clause gives the company broad rights to use, sell, or modify the content you upload."
    },

    "unilateral_changes": {
        "weight": 4,
        "keywords": [
            "modify these terms", "change at any time", "sole discretion", 
            "without prior notice", "updated version"
        ],
        "semantic_templates": [
            "We reserve the right to alter this agreement at our sole discretion.",
            "Your continued use of the service constitutes acceptance of new terms.",
            "We may change our policies without specifically notifying you."
        ],
        "explanation": "The company can change the rules of the agreement at any time without your consent."
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