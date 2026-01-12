from scripts.log_2fa_cron import generate_totp

def test_totp_format():
    seed = "a" * 64
    code = generate_totp(seed)
    assert len(code) == 6
    assert code.isdigit()
