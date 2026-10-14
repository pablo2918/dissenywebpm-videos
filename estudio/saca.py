import email, sys, pathlib
from email import policy
src, out = sys.argv[1], pathlib.Path(sys.argv[2]); out.mkdir(exist_ok=True)
m = email.message_from_bytes(open(src,'rb').read(), policy=policy.default)
n=0
for part in m.walk():
    if part.get_content_type().startswith('image/'):
        (out/f"sb_{n:02d}.jpg").write_bytes(part.get_payload(decode=True)); n+=1
print(n)
