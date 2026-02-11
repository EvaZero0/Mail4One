import mailbox
from pathlib import Path
from email.header import decode_header


def decode_email_header(header):
    """Decode email header (handles UTF-8 and other encodings)."""
    if not header:
        return ""
    
    decoded = decode_header(header)
    result = []

    for content, encoding in decoded:
        if isinstance(content, bytes):
            try:
                result.append(content.decode(encoding or 'utf-8', errors='ignore'))
            except Exception as e:
                print(f"Error decoding header: {e}")
                result.append(content.decode('utf-8', errors='ignore'))
        else:
            result.append(str(content))

    return ''.join(result)


def extract_unsubscribe_link(message):
    """Extract unsubscribe link from email message with security checks."""
    unsub_header = message.get('List-Unsubscribe', '')
    if not unsub_header:
        return None
    
    unsub_header = unsub_header.strip()
    
    # Extract link from angle brackets
    if unsub_header.startswith('<') and '>' in unsub_header:
        link = unsub_header[unsub_header.find('<')+1:unsub_header.find('>')]
        
        # Only accept HTTPS links for security
        if link.startswith('https://'):
            sender_email = message.get('From', '')
            if '@' in sender_email:
                domain = sender_email.split('@')[-1].strip('>')
                
                # Verify link domain matches sender domain (basic phishing protection)
                if domain.lower() in link.lower():
                    return link
    
    return None


def find_thunderbird_profile():
    """Find your Thunderbird profile directory."""
    import os
    
    # Get Windows AppData path
    appdata = os.getenv('APPDATA')
    if not appdata:
        print("APPDATA directory not found.")
        return None

    tb_path = Path(appdata) / 'Thunderbird' / 'Profiles'
    if not tb_path.exists():
        print("Thunderbird profile directory not found.")
        return None
    
    profiles = [p for p in tb_path.iterdir() if p.is_dir()]
                  
    if not profiles:
        print("No Thunderbird profiles found.")
        return None
    
    # Try to find default-release profile first
    your_thunderbird_profile = None
    for p in profiles:
        if p.name.endswith('.default-release'):
            your_thunderbird_profile = p
            break
    if not your_thunderbird_profile:
        your_thunderbird_profile = profiles[0]

    print(f"Found Thunderbird profile: {your_thunderbird_profile}")
    return your_thunderbird_profile


def analyze_emails(profile_path):
    """Analyze all emails, count senders and find unsubscribe links."""
    
    # Check both local and IMAP mail folders
    mail_folders = [
        profile_path / "Mail",
        profile_path / "ImapMail"
    ]
    
    sender_data = {}
    seen_message_ids = set()  # Prevent duplicate processing
    allowed_folders = ['inbox', 'newsletter', 'subscription', 'mailing list']
    
    print("Analyzing emails... Please wait.\n")
    
    for mail_folder in mail_folders:
        if not mail_folder.exists():
            print(f"Skipping {mail_folder.name} (not found)")
            continue
        
        print(f"Searching in {mail_folder.name}...")
        
        # Recursively find all mbox files
        for mbox_file in mail_folder.rglob("*"):
            # Skip index and metadata files
            if mbox_file.is_file() and mbox_file.suffix not in ['.msf', '.dat', '.json']:
                filename_lower = mbox_file.name.lower()
                
                # Only analyze relevant folders
                if not any(allowed in filename_lower for allowed in allowed_folders):
                    continue
                
                try:
                    print(f"  Reading {mbox_file.name}...")
                    mbox = mailbox.mbox(str(mbox_file))
                    
                    message_counter = 0
                    for message in mbox:
                        # Skip duplicate messages
                        message_id = message.get('Message-ID', None)
                        if message_id and message_id in seen_message_ids:
                            continue
                        if message_id:
                            seen_message_ids.add(message_id)
                        
                        message_counter += 1
                        sender = decode_email_header(message.get('From', ''))
                        if not sender:
                            continue
                        
                        recipient = message.get('Delivered-To') or message.get('To', '')
                        recipient = decode_email_header(recipient)
                        
                        # Create unique key for sender-recipient pair
                        key = f"{sender} → {recipient}"
                        
                        # Initialize sender data if not exists
                        if key not in sender_data:
                            sender_data[key] = {'count': 0, 'unsubscribe': None, 'recipient': recipient, 'sender': sender}
                        
                        sender_data[key]['count'] += 1
                        
                        # Extract unsubscribe link (only once per sender)
                        if not sender_data[key]['unsubscribe']:
                            sender_data[key]['unsubscribe'] = extract_unsubscribe_link(message)
                    
                    if message_counter > 0:
                        print(f"    -> {message_counter} messages found")
                            
                except Exception as e:
                    print(f"  Error reading {mbox_file.name}: {e}")
    
    return sender_data
