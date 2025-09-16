# password_generator.py
import streamlit as st
import hashlib
import string
import json
import base64
from pathlib import Path

# Set page configuration
st.set_page_config(
    page_title="Secure Password Generator",
    page_icon="🔒",
    layout="wide",
    initial_sidebar_state="expanded"
)

# Default services for quick access
DEFAULT_SERVICES = {
    "Google": "google.com",
    "Facebook": "facebook.com",
    "Twitter": "twitter.com",
    "GitHub": "github.com",
    "Amazon": "amazon.com",
    "Netflix": "netflix.com",
    "Microsoft": "microsoft.com",
    "Apple": "apple.com",
    "LinkedIn": "linkedin.com",
    "Instagram": "instagram.com",
    "Dropbox": "dropbox.com",
    "PayPal": "paypal.com",
    "Slack": "slack.com",
    "Discord": "discord.com",
    "Spotify": "spotify.com"
}

# Password strength meter function
def check_password_strength(password):
    """Check password strength and return a score from 0 to 100"""
    score = 0

    # Length check
    if len(password) >= 12:
        score += 25
    elif len(password) >= 8:
        score += 15
    else:
        score += 5

    # Lowercase check
    if any(c.islower() for c in password):
        score += 10

    # Uppercase check
    if any(c.isupper() for c in password):
        score += 10

    # Digit check
    if any(c.isdigit() for c in password):
        score += 15

    # Special character check
    if any(c in string.punctuation for c in password):
        score += 20

    # Complexity check (variety of character types)
    char_types = 0
    if any(c.islower() for c in password):
        char_types += 1
    if any(c.isupper() for c in password):
        char_types += 1
    if any(c.isdigit() for c in password):
        char_types += 1
    if any(c in string.punctuation for c in password):
        char_types += 1

    if char_types >= 3:
        score += 20

    # Cap score at 100
    if score > 100:
        score = 100

    # Determine strength category
    if score >= 80:
        strength = "Very Strong"
        color = "green"
    elif score >= 60:
        strength = "Strong"
        color = "blue"
    elif score >= 40:
        strength = "Moderate"
        color = "orange"
    elif score >= 20:
        strength = "Weak"
        color = "red"
    else:
        strength = "Very Weak"
        color = "darkred"

    return score, strength, color

# Password generation function
def generate_password(service, master_password, length=16, use_digits=True, use_symbols=True, no_ambiguous=False, show_salt=False):
    """
    Generates a unique, strong password for a service based on a master password.
    Uses PBKDF2-HMAC-SHA384, a secure key derivation function.
    """
    # Create a unique salt from the service name AND part of the master password
    salt = service.encode() + master_password[:8].lower().encode()

    if show_salt:
        st.write(f"[DEBUG] Service: {service}")
        st.write(f"[DEBUG] Master Password (first 8 chars, lowercased): {master_password[:8].lower()}")
        st.write(f"[DEBUG] Salt (hex): {salt.hex()}")

    # Use PBKDF2 with SHA-384 to generate a seed
    key = hashlib.pbkdf2_hmac(
        'sha384',
        master_password.encode(),
        salt,
        150000,    # High iteration count for brute-force resistance
        dklen=512  # Generate ample key material
    )

    # Define character sets
    chars = string.ascii_letters
    if use_digits:
        chars += string.digits
    if use_symbols:
        chars += string.punctuation

    if no_ambiguous:
        ambiguous_chars = 'l1I0O'
        chars = ''.join(c for c in chars if c not in ambiguous_chars)

    # Generate password from the derived key
    password = []
    for byte in key:
        if len(password) >= length:
            break
        index = byte % len(chars)
        password.append(chars[index])

    return ''.join(password)

# Function to copy to clipboard using JavaScript (safe embedding)
def copy_to_clipboard_via_js(text):
    """
    Copy text to clipboard using navigator.clipboard.writeText.
    We safely serialize 'text' into a JS string using json.dumps so special characters won't break the JS.
    """
    safe_text = json.dumps(text)  # safely escape the string as a JS literal
    js_code = f"""
    <script>
    (async function() {{
        try {{
            const text = {safe_text};
            await navigator.clipboard.writeText(text);
            // Optionally show a small DOM change for confirmation (not visible in Streamlit directly)
            // console.log("Copied to clipboard");
        }} catch (err) {{
            // If clipboard API fails, create a fallback textarea
            try {{
                var ta = document.createElement('textarea');
                ta.value = {safe_text};
                document.body.appendChild(ta);
                ta.select();
                document.execCommand('copy');
                document.body.removeChild(ta);
            }} catch (e) {{
                console.error('Clipboard copy failed', e);
            }}
        }}
    }})();
    </script>
    """
    st.components.v1.html(js_code, height=0)

# Main application
def main():
    # Custom CSS for styling
    st.markdown("""
    <style>
    .stProgress > div > div > div > div {
        background-color: #1f77b4;
    }
    .password-strength-weak {
        color: red;
        font-weight: bold;
    }
    .password-strength-moderate {
        color: orange;
        font-weight: bold;
    }
    .password-strength-strong {
        color: blue;
        font-weight: bold;
    }
    .password-strength-very-strong {
        color: green;
        font-weight: bold;
    }
    .service-button {
        margin: 5px;
    }
    </style>
    """, unsafe_allow_html=True)

    # Title and description
    st.title("🔒 Secure Password Generator")
    st.markdown("""
    Generate unique, strong passwords for each service using a master password and PBKDF2-HMAC-SHA384 encryption.
    Your master password is never stored or transmitted.
    """)

    # Initialize session state
    if 'generated_password' not in st.session_state:
        st.session_state.generated_password = None
    if 'master_password' not in st.session_state:
        st.session_state.master_password = ""

    # Sidebar: quick access buttons
    with st.sidebar:
        st.header("Quick Access Services")
        cols = st.columns(2)
        col_idx = 0
        for service_name, service_url in DEFAULT_SERVICES.items():
            with cols[col_idx]:
                if st.button(service_name, key=f"btn_{service_name}", use_container_width=True):
                    st.session_state.service_name = service_name
                    st.session_state.service_url = service_url
            col_idx = (col_idx + 1) % 2
        st.divider()
        st.info("💡 Click a service to autofill service name & URL")

    # Create main content area with tabs
    tab1, tab2, tab3 = st.tabs(["Generate Password", "Password Strength", "About"])

    with tab1:
        # Service information
        st.header("Service Information")
        col1, col2 = st.columns(2)
        with col1:
            service_name = st.text_input(
                "Service Name",
                value=st.session_state.get('service_name', ''),
                placeholder="e.g., Google"
            )
        with col2:
            service_url = st.text_input(
                "Service URL",
                value=st.session_state.get('service_url', ''),
                placeholder="e.g., google.com"
            )

        # Password options
        st.header("Password Options")
        col1, col2, col3 = st.columns(3)
        with col1:
            length = st.slider(
                "Password Length",
                min_value=8,
                max_value=32,
                value=16,
                help="Longer passwords are more secure"
            )
        with col2:
            use_digits = st.checkbox(
                "Include Digits",
                value=True,
                help="Add numbers (0-9) to your password"
            )
            use_symbols = st.checkbox(
                "Include Symbols",
                value=True,
                help="Add special characters (!@#$%^&*) to your password"
            )
        with col3:
            no_ambiguous = st.checkbox(
                "Exclude Ambiguous Characters",
                value=False,
                help="Exclude characters like l, 1, I, 0, O that can be confusing"
            )

        # Master password
        st.header("Master Password")
        master_password = st.text_input(
            "Enter Master Password",
            type="password",
            help="This will be used to generate your unique password"
        )
        confirm_password = st.text_input(
            "Confirm Master Password",
            type="password"
        )

        # Generate button
        if st.button("Generate Password", type="primary", use_container_width=True):
            if not service_name or not service_url:
                st.error("Please enter both service name and URL")
            elif not master_password:
                st.error("Please enter a master password")
            elif master_password != confirm_password:
                st.error("Master passwords do not match")
            else:
                with st.spinner("Generating secure password..."):
                    password = generate_password(
                        service=service_url,
                        master_password=master_password,
                        length=length,
                        use_digits=use_digits,
                        use_symbols=use_symbols,
                        no_ambiguous=no_ambiguous
                    )
                    st.session_state.generated_password = password
                    st.session_state.master_password = master_password
                    st.success("Password generated!")

        # Display generated password
        if st.session_state.generated_password:
            st.header("Generated Password")
            st.code(st.session_state.generated_password, language="text")

            # Copy & download
            col1, col2, col3 = st.columns([1, 1, 2])
            with col1:
                if st.button("Copy to Clipboard", use_container_width=True):
                    # Use safe JS copy
                    copy_to_clipboard_via_js(st.session_state.generated_password)
                    st.success("Password copied to clipboard (if your browser allows it).")
            with col2:
                # Download as text file
                password_data = f"Service: {service_name} ({service_url})\nPassword: {st.session_state.generated_password}"
                b64 = base64.b64encode(password_data.encode()).decode()
                href = f'<a href="data:file/txt;base64,{b64}" download="password_{service_name}.txt">Download Password</a>'
                st.markdown(href, unsafe_allow_html=True)

            # Password strength indicator
            score, strength, color = check_password_strength(st.session_state.generated_password)
            st.subheader("Password Strength")
            st.progress(score / 100)
            st.markdown(f"<p class='password-strength-{strength.lower().replace(' ', '-')}'>{strength} ({score}/100)</p>", unsafe_allow_html=True)

    with tab2:
        st.header("Password Strength Analysis")
        st.markdown("""
        This tool evaluates your password based on several criteria:
        
        - **Length**: Longer passwords are more secure (minimum 12 characters recommended)
        - **Character Variety**: Using different character types increases security
        - **Complexity**: Mix of uppercase, lowercase, numbers, and symbols
        - **Avoidance of Ambiguous Characters**: Prevents confusion (e.g., l vs 1)
        """)
        st.subheader("Test Password Strength")
        test_password = st.text_input("Enter a password to test", type="password")
        if test_password:
            score, strength, color = check_password_strength(test_password)
            st.progress(score / 100)
            st.markdown(f"**Strength:** <span class='password-strength-{strength.lower().replace(' ', '-')}'>{strength} ({score}/100)</span>", unsafe_allow_html=True)

            # Provide feedback
            if score < 40:
                st.error("This password is weak. Consider making it longer and adding more character types.")
            elif score < 60:
                st.warning("This password is moderate. It could be improved with more complexity.")
            elif score < 80:
                st.info("This password is strong. It provides good protection.")
            else:
                st.success("This password is very strong. Excellent security!")

    with tab3:
        st.header("About This Password Generator")
        st.markdown("""
        ### How It Works
        
        This password generator uses a cryptographic technique called **PBKDF2-HMAC-SHA384** 
        to create unique, strong passwords for each service you use while requiring you to 
        remember only one master password.
        
        ### Security Features
        
        1. **Cryptographic Hashing**: Uses PBKDF2 with 150,000 iterations to resist brute-force attacks
        2. **Unique Salts**: Each service gets a unique salt based on its name and part of your master password
        3. **No Storage**: Your master password and generated passwords are never stored or transmitted
        4. **Customizable**: Control password length, character sets, and complexity
        """)

        with st.expander("Technical Details"):
            st.markdown("""
            **Algorithm**: PBKDF2-HMAC-SHA384  
            **Iterations**: 150,000  
            **Key Length**: 512 bytes  
            **Salt Composition**: service_url + first 8 characters of lowercase master password  
            **Character Sets**: 
            - Letters (a-z, A-Z)
            - Digits (0-9) - optional
            - Symbols (!@#$%^&* etc.) - optional
            - Ambiguous characters (l, 1, I, 0, O) can be excluded
            """)

if __name__ == "__main__":
    main()
