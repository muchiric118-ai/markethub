def get_active_cert():
    with open("active_env.conf") as f:
        env = f.read().strip()
    if env == "production":
        return "cert_prod.cer"
    else:
        return "cert_sandbox.cer"

CERT_FILE = get_active_cert()
print(f"Using certificate: {CERT_FILE}")
