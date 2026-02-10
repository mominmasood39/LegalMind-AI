import re

class PracticalGuidance:
    """Provides practical, actionable guidance for legal situations"""
    
    def __init__(self):
        # Guidance templates for different legal situations
        self.guidance_templates = {
            'rape_victim': {
                'keywords': ['rape', 'sexual assault', 'molestation', 'sexual violence', 'forced'],
                'immediate_steps': """

IMMEDIATE STEPS FOR THE VICTIM:

1. ENSURE SAFETY FIRST:
   - Go to a safe location immediately
   - Contact a trusted family member or friend
   - If in immediate danger, call 15 (police helpline)

2. PRESERVE EVIDENCE (CRITICAL):
   - DO NOT wash, bathe, or shower
   - DO NOT change or wash the clothes you were wearing
   - DO NOT clean or disturb the crime scene
   - Keep all clothing in a paper bag (not plastic)
   - Do not brush teeth, rinse mouth, or use the restroom if possible

3. SEEK MEDICAL ATTENTION IMMEDIATELY:
   - Go to nearest government hospital within 72 hours (preferably within 24 hours)
   - Request a Medico-Legal Certificate (MLC)
   - Medical examination will document injuries and collect forensic evidence
   - Treatment is FREE at government hospitals for sexual assault victims

4. FILE AN FIR:
   - Go to the nearest police station or women's police station
   - You have the RIGHT to file an FIR - police CANNOT refuse
   - If police refuse, contact DSP/SP or use citizen portal
   - You can bring a trusted person with you
   - Request a copy of the FIR

5. LEGAL AID:
   - Contact District Legal Aid Authority for free legal representation
   - Women's crisis centers can provide support and guidance
   - You can contact Madadgaar 1099 or Punjab Women Helpline 1043

IMPORTANT RIGHTS:
- Your identity will be kept confidential
- Statement can be recorded at home if you cannot go to police station
- You have right to female police officer for statement
- Medical examination must be done by female doctor (if you request)"""
            },
            
            'harassment_victim': {
                'keywords': ['harassment', 'stalking', 'threatening', 'blackmail', 'cyberstalking'],
                'immediate_steps': """

IMMEDIATE STEPS FOR HARASSMENT VICTIM:

1. ENSURE YOUR SAFETY:
   - Assess if you are in immediate physical danger
   - If yes, go to a safe location and contact police (15)
   - Inform trusted family members or friends

2. PRESERVE ALL EVIDENCE:
   - DO NOT delete messages, emails, or call logs
   - Take screenshots of ALL threatening messages (include date/time)
   - Save voice messages and recordings
   - Keep a detailed log: dates, times, what happened, witnesses
   - If physical threats, keep threatening letters/notes in original form

3. BLOCK AND REPORT:
   - Block the harasser on all platforms
   - Report to platform (Facebook, Instagram, WhatsApp, etc.)
   - For cyberstalking: Report to FIA Cyber Crime Wing (complaint.fia.gov.pk)

4. FILE A COMPLAINT:
   - Police Station: File FIR under PPC Section 509 (harassment)
   - Cyber Harassment: File complaint with FIA Cyber Crime
   - Workplace: File complaint with ombudsman
   - Get a stamped copy of your complaint

5. LEGAL PROTECTION:
   - You can request police protection if threats are serious
   - Apply for protective bail if you fear false counter-complaint
   - Women can contact Punjab Women Protection Authority

WHAT TO INCLUDE IN COMPLAINT:
- Complete timeline of harassment
- All evidence (screenshots, messages, recordings)
- Names and details of witnesses
- Details of harasser (name, phone, address if known)
- Your contact information and location"""
            },
            
            'theft_victim': {
                'keywords': ['theft', 'stolen', 'robbery', 'burglary', 'snatching'],
                'immediate_steps': """

IMMEDIATE STEPS FOR THEFT VICTIM:

1. ENSURE SAFETY:
   - If robbery just occurred, do not chase the thief (safety first)
   - If you witnessed the theft, note descriptions of suspects
   - Check if anyone is injured and call ambulance if needed

2. PRESERVE EVIDENCE:
   - DO NOT touch or disturb the crime scene
   - Take photos/videos of the scene before anything is moved
   - Note exact time and location
   - Collect contact info of any witnesses

3. LIST STOLEN ITEMS:
   - Make detailed list of ALL stolen items
   - Include: brand, model, serial numbers, value, purchase receipts
   - For mobile phones: note IMEI number
   - For vehicles: note registration number, chassis number, engine number

4. FILE FIR IMMEDIATELY:
   - Go to nearest police station within 24 hours
   - Provide complete description of stolen items
   - Provide witness details if any
   - Request copy of FIR

5. FOLLOW-UP ACTIONS:
   - Mobile phone: Contact PTA to block IMEI
   - Bank cards: Immediately block all stolen cards
   - Documents: File complaint for lost documents (CNIC, license, etc.)
   - Insurance: Inform insurance company if items were insured

DOCUMENTS TO BRING:
- Purchase receipts of stolen items
- Photos of stolen items (if available)
- CNIC copy
- Witness statements (written)"""
            },
            
            'domestic_violence': {
                'keywords': ['domestic violence', 'domestic abuse', 'wife beating', 'husband violence', 'family violence'],
                'immediate_steps': """

IMMEDIATE STEPS FOR DOMESTIC VIOLENCE VICTIM:

1. ENSURE IMMEDIATE SAFETY:
   - If in immediate danger, leave the house and go to a safe place
   - Call 15 (police) or 1099 (Madadgaar helpline)
   - Go to nearest police station or women's shelter

2. SEEK MEDICAL ATTENTION:
   - Go to hospital IMMEDIATELY for injuries
   - Get Medico-Legal Certificate (MLC) - this is legal evidence
   - Take photos of all visible injuries
   - Keep medical reports and prescriptions safe

3. PRESERVE EVIDENCE:
   - DO NOT wash clothes with blood stains
   - Keep torn or damaged clothes as evidence
   - Take photos of injuries and damaged property
   - Note dates, times, and details of each incident
   - Keep threatening messages, voice recordings

4. FILE COMPLAINT:
   - File FIR at police station under PPC 337/336 (hurt) or 506 (threat)
   - OR file application under Domestic Violence Act at Magistrate court
   - Request police protection order
   - Women's police stations are available in major cities

5. SEEK PROTECTION ORDER:
   - Apply to court for protection order against abuser
   - Court can order abuser to stay away from you
   - Can include residence order (exclusive use of home)
   - Free legal aid available through District Legal Aid

6. GET SUPPORT:
   - Contact: Punjab Women Protection Authority (1043)
   - Shelter homes available (Dar-ul-Aman)
   - Legal aid: District Legal Aid Committee
   - Counseling and support services available

IMPORTANT DOCUMENTS:
- Medical reports and MLC
- Photos of injuries
- Witness statements
- Evidence of threats (messages, recordings)
- Marriage certificate
- CNIC copies"""
            },
            
            'fir_filing': {
                'keywords': ['file fir', 'lodge fir', 'report to police', 'police complaint', 'how to report crime'],
                'immediate_steps': """

HOW TO FILE AN FIR (First Information Report):

1. WHERE TO FILE:
   - Police station in whose jurisdiction (area) the crime occurred
   - Any police station if it's a cognizable offense (serious crime)
   - Women's police station (for crimes against women)
   - Online: Through citizen portal in some provinces

2. WHAT TO BRING:
   - Your original CNIC
   - Any evidence you have (documents, photos, objects)
   - Witness contact details
   - Medical reports (if injured)
   - Written complaint (optional but helpful)

3. INFORMATION TO PROVIDE:
   - Your name, father's name, CNIC, address, contact number
   - Date, time, and exact location of incident
   - Detailed description of what happened
   - Description of accused (if known): name, address, physical features
   - Names and contact of witnesses
   - List of stolen/damaged items (if applicable)

4. YOUR RIGHTS DURING FIR:
   - Police CANNOT refuse to register FIR for cognizable offense
   - FIR must be written in your presence
   - FIR must be read back to you before you sign
   - You must get a FREE copy of the FIR
   - FIR should be in language you understand

5. IF POLICE REFUSE TO FILE FIR:
   - Request written reason for refusal
   - Contact SHO (Station House Officer)
   - Complaint to DSP/SP of the area
   - Use online complaint portal
   - File private complaint directly to Magistrate

6. AFTER FILING FIR:
   - Keep FIR copy safe - you'll need it for court
   - Note down the FIR number
   - Police will investigate and may call you for statement
   - You can follow up on investigation progress
   - Inform police if you receive threats

IMPORTANT NOTES:
- FIR is completely FREE
- You don't need a lawyer to file FIR
- Statement to police is NOT under oath (that comes later in court)
- If you remember more details later, you can provide supplementary statement"""
            },
            
            'bail_procedure': {
                'keywords': ['bail', 'get bail', 'bail application', 'interim bail', 'anticipatory bail'],
                'immediate_steps': """

BAIL PROCEDURE IN PAKISTAN:

1. TYPES OF BAIL:
   - Before Arrest Bail (Anticipatory Bail): Apply before arrest
   - Post-Arrest Bail: Apply after arrest
   - Interim Bail: Temporary bail while main application pending

2. WHERE TO APPLY:
   - Sessions Court: For cases in Magistrate or Sessions Court
   - High Court: For serious cases or if Sessions Court rejects
   - Supreme Court: If High Court rejects (rare)

3. DOCUMENTS REQUIRED:
   - Bail application (typed on stamp paper)
   - FIR copy (if available)
   - CNIC copy of accused
   - Surety bonds (as per court order)
   - Character certificates
   - Medical reports (if applicable)
   - Employment proof (job letter, business registration)
   - Property documents (for surety)

4. BAIL PROCEDURE:
   - Hire a lawyer (mandatory for bail applications)
   - Lawyer will draft bail application
   - Application filed in court with required documents
   - Court may call for comments from police/prosecution
   - Hearing date will be fixed (usually 2-7 days)
   - You or surety must appear in court on hearing date

5. SURETY REQUIREMENTS:
   - 1 or 2 sureties required (as per court order)
   - Surety must be reliable person
   - Surety provides property documents or cash security
   - Surety guarantees accused will appear in court

6. BAIL CONDITIONS:
   - Regular appearance in court on all dates
   - Do not leave country (passport may be submitted)
   - Do not contact witnesses or victims
   - Do not commit any offense while on bail
   - Violation can lead to bail cancellation

7. WHEN BAIL IS DIFFICULT:
   - Murder cases
   - Terrorism cases
   - Cases under certain sections of Narcotics Act
   - If accused is flight risk
   - If accused may tamper with evidence

IMMEDIATE STEPS IF ARRESTED:
   - Inform family immediately
   - Contact a lawyer as soon as possible
   - Do not sign any confession
   - Request police to inform family
   - Request medical examination if tortured

COST ESTIMATE:
- Lawyer fee: PKR 20,000 - 100,000+ (varies)
- Stamp paper: PKR 300-500
- Court fee: Minimal (few hundred rupees)
- Surety bonds: As per court order"""
            },
        }
    
    def detect_situation_type(self, query):
        """Detect what type of legal situation this is"""
        query_lower = query.lower()
        
        # Check each situation type
        for situation, data in self.guidance_templates.items():
            for keyword in data['keywords']:
                if keyword in query_lower:
                    return situation
        
        return None
    
    def get_guidance(self, query):
        """Get practical guidance for the query"""
        situation = self.detect_situation_type(query)
        
        if situation and situation in self.guidance_templates:
            return self.guidance_templates[situation]['immediate_steps']
        
        # Default guidance for general queries
        return """

GENERAL LEGAL GUIDANCE:

To help you better, please provide:
1. Your province/city
2. Brief description of what happened
3. When it happened
4. Whether you have filed any complaint/FIR
5. What outcome you are seeking

This will help me provide specific guidance on:
- What immediate steps to take
- What evidence to preserve
- How to file complaint/FIR
- What documents you'll need
- Your legal rights and options"""
    
    def should_add_guidance(self, query):
        """Check if query needs practical guidance"""
        # Keywords that indicate someone needs help/guidance
        help_indicators = [
            'what should', 'what to do', 'what can i do', 'how to',
            'help me', 'guide me', 'what are my options', 'what steps',
            'victim', 'happened to me', 'i was', 'someone did'
        ]
        
        query_lower = query.lower()
        for indicator in help_indicators:
            if indicator in query_lower:
                return True
        
        return False