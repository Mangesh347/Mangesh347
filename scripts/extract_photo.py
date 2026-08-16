import re
import base64
from pathlib import Path

src = Path(r"C:\Resume\portfolio\mangesh_portfolio_updated.html")
html = src.read_text(encoding="utf-8", errors="ignore")
m = re.search(r'src="data:image/(jpeg|jpg|png);base64,([^"]+)"', html)
if not m:
    raise SystemExit("no embedded photo found")
data = base64.b64decode(m.group(2))
out = Path(__file__).resolve().parents[1] / "source-photo.jpg"
out.write_bytes(data)
print("wrote", out, "bytes", len(data), "kind", m.group(1))
