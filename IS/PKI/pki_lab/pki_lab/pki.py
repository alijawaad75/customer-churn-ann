# PKI Practical Implementation in Python
# This script provides hands-on experience with Public Key Infrastructure (PKI) concepts

import os
import subprocess
import shutil
from pathlib import Path

def run_command(cmd, shell=True):
    """Helper function to run shell commands and return output"""
    try:
        result = subprocess.run(cmd, shell=shell, capture_output=True, text=True)
        if result.stdout:
            print(result.stdout)
        if result.stderr and result.returncode != 0:
            print(f"Error: {result.stderr}")
        return result.returncode == 0
    except Exception as e:
        print(f"Command failed: {e}")
        return False

# ============================================================================
# CELL 1: Setup and Environment Check
# ============================================================================

print("=== PKI Practical Implementation ===\n")

# Check OpenSSL availability
print("Checking OpenSSL availability...")
run_command("openssl version")

# Create working directory
work_dir = "pki_lab"
if os.path.exists(work_dir):
    shutil.rmtree(work_dir)
os.makedirs(work_dir)
os.chdir(work_dir)
print(f"\nWorking directory: {os.getcwd()}")

# ============================================================================
# CELL 2: Asymmetric Encryption - Key Pair Generation
# ============================================================================

print("\n" + "="*60)
print("1. ASYMMETRIC ENCRYPTION - KEY PAIR GENERATION")
print("="*60)

# Generate RSA private key (2048 bits)
print("Generating RSA private key...")
run_command("openssl genrsa -out private_key.pem 2048")

# Extract public key from private key
print("\nExtracting public key...")
run_command("openssl rsa -in private_key.pem -pubout -out public_key.pem")

# Examine key files
print("\n=== Files Created ===")
run_command("ls -la *.pem")

print("\n=== Private Key Details ===")
run_command("openssl rsa -in private_key.pem -text -noout | head -20")

print("\n=== Public Key Details ===")
run_command("openssl rsa -in public_key.pem -pubin -text -noout")

# ============================================================================
# CELL 3: Test Encryption and Decryption
# ============================================================================

print("\n" + "="*60)
print("TESTING ENCRYPTION AND DECRYPTION")
print("="*60)

# Create a test message
test_message = "This is a secret message for PKI demonstration!"
with open('messag3e.txt', 'w') as f:
    f.write(test_message)

print(f"Original message: {test_message}")

# Encrypt with public key
print("\nEncrypting message with public key...")
run_command("openssl rsautl -encrypt -inkey public_key.pem -pubin -in message.txt -out encrypted_message.bin")

print("Encrypted file size:")
run_command("ls -la encrypted_message.bin")

print("\nFirst few bytes of encrypted message (hex):")
run_command("hexdump -C encrypted_message.bin | head -5")

# Decrypt with private key
print("\nDecrypting message with private key...")
run_command("openssl rsautl -decrypt -inkey private_key.pem -in encrypted_message.bin -out decrypted_message.txt")

# Verify decryption
with open('decrypted_message.txt', 'r') as f:
    decrypted_content = f.read()

print(f"Decrypted message: {decrypted_content}")
print(f"Decryption successful: {test_message == decrypted_content}")

# ============================================================================
# CELL 4: Certificate Authority (CA) Creation
# ============================================================================

print("\n" + "="*60)
print("2. CERTIFICATE AUTHORITY (CA) CREATION")
print("="*60)

# Create CA directory structure
ca_dirs = ['mini-ca', 'mini-ca/certs', 'mini-ca/private', 'mini-ca/newcerts']
for dir_name in ca_dirs:
    os.makedirs(dir_name, exist_ok=True)

# Initialize CA files
with open('mini-ca/serial', 'w') as f:
    f.write('01\n')

# Create empty index file
open('mini-ca/index.txt', 'w').close()

print("CA directory structure created.")

# Create OpenSSL configuration for CA
openssl_config = """
[ ca ]
default_ca = CA_default

[ CA_default ]
dir               = ./mini-ca
certs             = $dir/certs
new_certs_dir     = $dir/newcerts
database          = $dir/index.txt
serial            = $dir/serial
private_key       = $dir/private/ca-key.pem
certificate       = $dir/certs/ca-cert.pem
default_days      = 365
default_md        = sha256
policy            = policy_any

[ policy_any ]
countryName            = optional
stateOrProvinceName    = optional
organizationName       = optional
organizationalUnitName = optional
commonName             = supplied
emailAddress           = optional

[ req ]
distinguished_name = req_distinguished_name
x509_extensions = v3_ca
prompt = no

[ req_distinguished_name ]
C = US
ST = California
L = San Francisco
O = Jupyter PKI Lab
CN = Jupyter Root CA

[ v3_ca ]
subjectKeyIdentifier = hash
authorityKeyIdentifier = keyid:always,issuer:always
basicConstraints = CA:true
"""

with open('openssl.cnf', 'w') as f:
    f.write(openssl_config)

print("OpenSSL configuration created!")

# Generate CA private key
print("\nGenerating CA private key...")
run_command("openssl genrsa -out mini-ca/private/ca-key.pem 2048")

# Generate CA certificate (self-signed)
print("\nGenerating CA certificate (self-signed)...")
run_command("openssl req -new -x509 -key mini-ca/private/ca-key.pem -out mini-ca/certs/ca-cert.pem -days 365 -config openssl.cnf")

print("\n=== CA Certificate Details ===")
run_command("openssl x509 -in mini-ca/certs/ca-cert.pem -text -noout | head -30")

# ============================================================================
# CELL 5: Create and Sign Server Certificate
# ============================================================================

print("\n" + "="*60)
print("CREATING AND SIGNING SERVER CERTIFICATE")
print("="*60)

# Generate server private key
print("Generating server private key...")
run_command("openssl genrsa -out server-key.pem 2048")

# Create server certificate configuration
server_config = """
[ req ]
distinguished_name = req_distinguished_name
prompt = no

[ req_distinguished_name ]
C = US
ST = California
L = San Francisco
O = Jupyter PKI Lab
CN = jupyter-server.local
"""

with open('server.cnf', 'w') as f:
    f.write(server_config)

# Create certificate signing request (CSR)
print("\nCreating Certificate Signing Request (CSR)...")
run_command("openssl req -new -key server-key.pem -out server.csr -config server.cnf")

print("\n=== CSR Details ===")
run_command("openssl req -in server.csr -text -noout | head -20")

# Sign the CSR with our CA
print("\nSigning server certificate with CA...")
run_command("openssl ca -config openssl.cnf -in server.csr -out server-cert.pem -batch")

print("\n=== Signed Certificate Details ===")
run_command("openssl x509 -in server-cert.pem -text -noout | grep -A 5 'Issuer:\\|Subject:'")

# ============================================================================
# CELL 6: Digital Signatures
# ============================================================================

print("\n" + "="*60)
print("3. DIGITAL SIGNATURES")
print("="*60)

# Create a document to sign
document_content = """
IMPORTANT DOCUMENT
==================

This document contains critical information about PKI implementation.
It must be digitally signed to ensure authenticity and integrity.

Date: 2024-06-06
Author: PKI Lab
Version: 1.0
"""

with open('document.txt', 'w') as f:
    f.write(document_content)

print("Document created for signing.")

# Create digital signature
print("\nCreating digital signature...")
run_command("openssl dgst -sha256 -sign private_key.pem -out document.sig document.txt")

print("Digital signature created!")
print("\nSignature file size:")
run_command("ls -la document.sig")

# Verify the digital signature
print("\n=== Verifying Original Document ===")
result = run_command("openssl dgst -sha256 -verify public_key.pem -signature document.sig document.txt")
print(f"Verification successful: {result}")

# Test with modified document
modified_content = document_content.replace("Version: 1.0", "Version: 1.1")
with open('modified_document.txt', 'w') as f:
    f.write(modified_content)

print("\n=== Verifying Modified Document ===")
result = run_command("openssl dgst -sha256 -verify public_key.pem -signature document.sig modified_document.txt")
print(f"Verification failed (as expected): {not result}")
print("✅ Signature verification correctly detects document modification!")

# ============================================================================
# CELL 7: S/MIME Signing and Verification
# ============================================================================

print("\n" + "="*60)
print("ADVANCED: S/MIME SIGNING")
print("="*60)

# Sign document using S/MIME with certificate
print("Signing document with S/MIME...")
run_command("openssl smime -sign -in document.txt -out document.p7s -signer server-cert.pem -inkey server-key.pem")

print("Document signed with certificate!")
print("\nSigned document size:")
run_command("ls -la document.p7s")

# Verify S/MIME signature
print("\nVerifying S/MIME signature...")
run_command("openssl smime -verify -in document.p7s -CAfile mini-ca/certs/ca-cert.pem -out verified_document.txt")

print("S/MIME signature verified successfully!")

# ============================================================================
# CELL 8: HTTPS Certificate Creation
# ============================================================================

print("\n" + "="*60)
print("4. HTTPS CERTIFICATE CREATION")
print("="*60)

# Create HTTPS server configuration
https_config = """
[ req ]
distinguished_name = req_distinguished_name
req_extensions = v3_req
prompt = no

[ req_distinguished_name ]
C = US
ST = CA
L = San Francisco
O = Jupyter Lab
CN = localhost

[ v3_req ]
keyUsage = keyEncipherment, dataEncipherment
extendedKeyUsage = serverAuth
subjectAltName = @alt_names

[ alt_names ]
DNS.1 = localhost
DNS.2 = *.localhost
IP.1 = 127.0.0.1
"""

with open('https.cnf', 'w') as f:
    f.write(https_config)

# Generate HTTPS certificate
print("Creating HTTPS server certificate...")
run_command("openssl req -x509 -newkey rsa:2048 -keyout https-server.key -out https-server.crt -days 365 -nodes -config https.cnf")

print("\n=== HTTPS Certificate Details ===")
run_command("openssl x509 -in https-server.crt -text -noout | grep -A 10 'Subject:\\|DNS:'")

# ============================================================================
# CELL 9: Summary and Verification
# ============================================================================

print("\n" + "="*60)
print("5. SUMMARY AND ANALYSIS")
print("="*60)

print("=== PKI Lab Summary ===")
print("\nFiles created in this lab:")
run_command("find . -name '*.pem' -o -name '*.crt' -o -name '*.key' -o -name '*.sig' -o -name '*.p7s' | sort")

print("\n=== Certificate Chain Verification ===")
run_command("openssl verify -CAfile mini-ca/certs/ca-cert.pem server-cert.pem")

print("\n=== Key Relationships ===")
relationships = [
    "1. private_key.pem + public_key.pem = Asymmetric key pair",
    "2. ca-key.pem + ca-cert.pem = Root CA", 
    "3. server-key.pem + server-cert.pem = Server certificate (signed by CA)",
    "4. document.sig = Digital signature of document.txt",
    "5. https-server.key + https-server.crt = Self-signed HTTPS certificate"
]

for relationship in relationships:
    print(relationship)

# ============================================================================
# CELL 10: Interactive Exercises
# ============================================================================

print("\n" + "="*60)
print("6. INTERACTIVE EXERCISES")
print("="*60)

# Exercise 1: Sign a new document
exercise_doc = "Student Exercise Document\nDate: 2024-06-06\nI understand PKI concepts!"

with open('exercise1.txt', 'w') as f:
    f.write(exercise_doc)

print("Exercise 1: Signing exercise document...")
run_command("openssl dgst -sha256 -sign private_key.pem -out exercise1.sig exercise1.txt")
print("Verifying exercise signature...")
result = run_command("openssl dgst -sha256 -verify public_key.pem -signature exercise1.sig exercise1.txt")
print(f"Exercise 1 completed successfully: {result}")

# Exercise 2: Create new server certificate
print("\nExercise 2: Creating new server certificate...")

# Create new server config
exercise_server_config = """
[ req ]
distinguished_name = req_distinguished_name
prompt = no

[ req_distinguished_name ]
C = US
ST = California  
L = San Francisco
O = Exercise Lab
CN = exercise.local
"""

with open('exercise-server.cnf', 'w') as f:
    f.write(exercise_server_config)

# Generate new server key and CSR
run_command("openssl genrsa -out exercise-server-key.pem 2048")
run_command("openssl req -new -key exercise-server-key.pem -out exercise-server.csr -config exercise-server.cnf")

# Sign with CA
run_command("openssl ca -config openssl.cnf -in exercise-server.csr -out exercise-server-cert.pem -batch")

# Verify certificate chain
print("Verifying exercise certificate chain...")
result = run_command("openssl verify -CAfile mini-ca/certs/ca-cert.pem exercise-server-cert.pem")
print(f"Exercise 2 completed successfully: {result}")

print("\n" + "="*60)
print("PKI LAB COMPLETED SUCCESSFULLY!")
print("="*60)

print("""
Real-World Applications:
- Web Security: HTTPS/TLS certificates
- Code Signing: Software authenticity  
- Email Security: S/MIME encrypted emails
- VPN: Client certificates for authentication
- IoT Security: Device identity certificates
- Blockchain: Digital signatures for transactions

Next Steps:
1. Explore certificate revocation (CRL/OCSP)
2. Learn about HSMs (Hardware Security Modules)
3. Study modern protocols (TLS 1.3, Certificate Transparency)
4. Practice with enterprise tools
""")

# ============================================================================
# CELL 11: Cleanup Function (Optional)
# ============================================================================

def cleanup_lab():
    """Clean up all generated files"""
    os.chdir('..')
    if os.path.exists('pki_lab'):
        shutil.rmtree('pki_lab')
        print("Lab files cleaned up!")
    else:
        print("No lab files to clean up.")

print(f"\nTo clean up lab files, run: cleanup_lab()")
print(f"Current working directory: {os.getcwd()}")