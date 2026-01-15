"""Schema definitions and field mappings for contract extraction."""

# Section-to-field mapping for targeted extraction
SECTION_FIELD_MAPPING = {
    # Section keywords (regex) → Fields to extract
    "preamble|recitals": [
        "form", "exhibit", "date", "buyer", "buyer_location", "seller", "seller_location",
        "issuer", "issuer_location", "agreement_type"
    ],
    "payment|fee|price|consideration|purchase|invoice|charge": [
        "fee_model", "fee_type", "fee_amount", "fee_mode", "fee_percent",
        "charged_per", "payment_freq", "tranche_trigger", "delivery_trigger",
        "payment_timing", "payment_method"
    ],
    "license|rights|intellectual|property|ip|grant": [
        "license_transferable", "sublicensing", "exclusive",
        "title_and_interest_sold", "ip_sold", "deliverables",
        "derivative_work_owned_by"
    ],
    "term|renewal|termination|scope": [
        "auto_renews", "term", "can_terminate", "termination_notice",
        "breach_terminable", "breach_notice", "breach_prorated",
        "coc_terminable", "coc_notice"
    ],
    "price|adjustment|change": [
        "prices_adjustable", "price_change_notice", "price_change_requires",
        "no_price_changes"
    ],
    "expense|tax|cost|travel": [
        "who_pays_sales_tax", "who_pays_expenses", "expenses_include"
    ],
    "warrant|representation": [
        "reps_and_warranties_mutual", "reps_and_warranties_seller",
        "reps_and_warranties_buyer", "warranty_period"
    ],
    "indemnif|liabilit|damage|limitation": [
        "indemnification", "indemnity_notify", "indemnity_discovery_trigger",
        "liable_for_indirect_damages", "max_liability", "liability_time_limit"
    ],
    "sla|service.level|support|maintenance|error|resolution|response": [
        "has_sla", "sla_tiers", "sla_has_service_credits", "sla_credit_cap_pct",
        "sla_critical_response", "sla_critical_fulltime", "sla_medium_fix",
        "sla_low_fix_required", "sla_goals_strict", "are_upgrades_provided"
    ],
    "govern|law|jurisdiction|venue|arbitration|miscellaneous": [
        "law_in_state_of", "arbitration_in_state_of"
    ],
    "exhibit": [
        "fee_amount", "fee_model", "charged_per", "payment_freq"
    ]
}

# TSV columns for 68-field extraction output
TSV_COLUMNS = [
    "idx", "form", "exhibit", "date", "buyer", "buyer_location",
    "seller", "seller_location", "issuer", "issuer_location", "url",
    "agreement_type", "license_transferable", "sublicensing", "exclusive",
    "title_and_interest_sold", "ip_sold", "deliverables", "fee_model",
    "fee_type", "fee_amount", "fee_mode", "fee_percent", "charged_per",
    "payment_freq", "tranche_trigger", "delivery_trigger", "auto_renews",
    "term", "can_terminate", "termination_notice", "breach_terminable",
    "breach_notice", "breach_prorated", "coc_terminable", "coc_notice",
    "derivative_work_owned_by", "prices_adjustable", "price_change_notice",
    "price_change_requires", "no_price_changes", "payment_timing",
    "who_pays_sales_tax", "who_pays_expenses", "expenses_include",
    "payment_method", "are_upgrades_provided", "reps_and_warranties_mutual",
    "reps_and_warranties_seller", "reps_and_warranties_buyer",
    "warranty_period", "indemnification", "indemnity_notify",
    "indemnity_discovery_trigger", "liable_for_indirect_damages",
    "max_liability", "liability_time_limit", "has_sla", "sla_tiers",
    "sla_has_service_credits", "sla_credit_cap_pct", "sla_critical_response",
    "sla_critical_fulltime", "sla_medium_fix", "sla_low_fix_required",
    "sla_goals_strict", "law_in_state_of", "arbitration_in_state_of"
]

# CUAD dataset columns (22 features)
CUAD_COLUMNS = [
    "URL",
    "Document Name",
    "Parties",
    "Agreement Date",
    "Effective Date",
    "Expiration Date",
    "Renewal Term (Days)",
    "Notice Period To Terminate Renewal",
    "Termination For Convenience",
    "Change Of Control",
    "Anti-Assignment",
    "Revenue/Profit Sharing",
    "Ip Ownership Assignment",
    "Joint Ip Ownership",
    "Non-Transferable License",
    "Source Code Escrow",
    "Post-Termination Services",
    "Audit Rights",
    "Uncapped Liability",
    "Cap On Liability",
    "Liquidated Damages",
    "Warranty Duration"
]

# Field definitions for extraction prompts
FIELD_DEFINITIONS = {
    "form": 'form: SEC form type only (e.g., "10-K", "8-K"). NOT the exhibit type. If metadata shows "EX-10.2", the form is probably "8-K".',
    "exhibit": 'exhibit: Exhibit number only (e.g., "10.6", "10.2"). Extract the number from "EX-10.2" -> "10.2"',
    "date": 'date: Contract date in M/D/YY format (e.g., "2/13/25", "5/26/25")',
    "buyer": 'buyer: Name of the purchasing party (lowercase, no legal suffixes like "corp.", "inc.", "ltd")',
    "buyer_location": 'buyer_location: Buyer\'s state/country code (e.g., "DE", "FL", "UK", "WY")',
    "seller": 'seller: Name of the selling party (lowercase, no legal suffixes like "corp.", "inc.", "ltd")',
    "seller_location": "seller_location: Seller's state/country code",
    "issuer": "issuer: If different from buyer/seller, the SEC filing company (lowercase)",
    "issuer_location": "issuer_location: Issuer's state/country code",
    "agreement_type": 'agreement_type: "support", "license", or "purchase"',
    "license_transferable": 'license_transferable: "yes" or "no" - can the license be transferred?',
    "sublicensing": 'sublicensing: "yes" or "no" - is sublicensing allowed?',
    "exclusive": 'exclusive: "yes" or "no" - is this an exclusive license?',
    "title_and_interest_sold": 'title_and_interest_sold: "yes" or "no" - is full ownership transferred?',
    "ip_sold": 'ip_sold: "yes" or "no" - is intellectual property sold?',
    "deliverables": 'deliverables: What is being delivered (e.g., "support", "license", "software, docs, trade secrets")',
    "fee_model": 'fee_model: "subscription", "usage", "flat", "tranche"',
    "fee_type": 'fee_type: "fixed" or "percentage"',
    "fee_amount": 'fee_amount: Numeric amount (e.g., "3500", "960000")',
    "fee_mode": 'fee_mode: "dollars", "stock", etc.',
    "fee_percent": 'fee_percent: If percentage-based, the decimal (e.g., "0.06")',
    "charged_per": 'charged_per: Time unit for fees (e.g., "month", "claim")',
    "payment_freq": 'payment_freq: "monthly", "quarterly", "1", "2" (number of payments)',
    "tranche_trigger": 'tranche_trigger: What triggers each payment (e.g., "software operational")',
    "delivery_trigger": 'delivery_trigger: What triggers delivery (e.g., "first payment")',
    "auto_renews": 'auto_renews: "yes" or "no"',
    "term": 'term: Contract duration (e.g., "6mo", "5y", "1y")',
    "can_terminate": 'can_terminate: "either side", "mutual agreement", etc.',
    "termination_notice": 'termination_notice: Notice period (e.g., "1mo", "6mo", "immediate")',
    "breach_terminable": 'breach_terminable: "yes" or "no" - can breach terminate the contract?',
    "breach_notice": 'breach_notice: Notice period for breach (e.g., "1mo")',
    "breach_prorated": 'breach_prorated: "yes" or "no" - is payment prorated on breach?',
    "coc_terminable": 'coc_terminable: "yes" or "no" - can change of control terminate?',
    "coc_notice": "coc_notice: Notice period for change of control",
    "derivative_work_owned_by": 'derivative_work_owned_by: Who owns derivatives ("buyer", "seller")',
    "prices_adjustable": 'prices_adjustable: "yes" or "no"',
    "price_change_notice": 'price_change_notice: Notice for price changes (e.g., "1mo")',
    "price_change_requires": 'price_change_requires: What approval needed ("consent", "negotiation")',
    "no_price_changes": 'no_price_changes: Duration of price freeze (e.g., "6mo")',
    "payment_timing": 'payment_timing: When payment is due (e.g., "start + 0d", "end + 30d")',
    "who_pays_sales_tax": 'who_pays_sales_tax: "buyer" or "seller"',
    "who_pays_expenses": 'who_pays_expenses: "buyer" or "seller"',
    "expenses_include": "expenses_include: What expenses are covered (quoted string)",
    "payment_method": 'payment_method: "wire", "check", etc.',
    "are_upgrades_provided": 'are_upgrades_provided: "yes" or "no"',
    "reps_and_warranties_mutual": "reps_and_warranties_mutual: Mutual representations (multi-line text)",
    "reps_and_warranties_seller": "reps_and_warranties_seller: Seller's representations (multi-line text)",
    "reps_and_warranties_buyer": "reps_and_warranties_buyer: Buyer's representations (multi-line text)",
    "warranty_period": 'warranty_period: Duration of warranty (e.g., "0mo", "1y")',
    "indemnification": 'indemnification: Who indemnifies whom (e.g., "seller indemnifies buyer", "mutual")',
    "indemnity_notify": 'indemnity_notify: Notice requirement for indemnification (e.g., "1y")',
    "indemnity_discovery_trigger": 'indemnity_discovery_trigger: What triggers indemnity (e.g., "constructive")',
    "liable_for_indirect_damages": 'liable_for_indirect_damages: "yes" or "no"',
    "max_liability": 'max_liability: Liability cap (e.g., "1x amount paid")',
    "liability_time_limit": 'liability_time_limit: Time limit for liability claims (e.g., "12mo")',
    "has_sla": 'has_sla: "yes" or "no" - does it have Service Level Agreement?',
    "sla_tiers": 'sla_tiers: Number of SLA tiers (e.g., "3")',
    "sla_has_service_credits": 'sla_has_service_credits: "yes" or "no"',
    "sla_credit_cap_pct": 'sla_credit_cap_pct: Service credit cap as decimal (e.g., "0")',
    "sla_critical_response": 'sla_critical_response: Critical issue response time (e.g., "30m")',
    "sla_critical_fulltime": 'sla_critical_fulltime: "yes" or "no" - 24/7 support for critical?',
    "sla_medium_fix": 'sla_medium_fix: Medium issue fix time (e.g., "5d")',
    "sla_low_fix_required": 'sla_low_fix_required: "yes" or "no" - is low priority fix required?',
    "sla_goals_strict": 'sla_goals_strict: "yes" or "no" - are SLA goals binding?',
    "law_in_state_of": 'law_in_state_of: Governing law jurisdiction (e.g., "DE", "FL", "WY")',
    "arbitration_in_state_of": 'arbitration_in_state_of: Arbitration location (e.g., "CA", "FL")',
}
