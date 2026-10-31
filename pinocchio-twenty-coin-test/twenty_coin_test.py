"""Twenty-Coin Test: illustrative local reference implementation, not Tim's/Harmonic's code."""
import json
from datetime import datetime, timezone
from pathlib import Path

BASE = Path(__file__).parent

class Workshop:
    def __init__(self):
        self.authority = {"merchant": "Geppetto's chosen merchant", "items": ["wood", "glue"], "max_coins": 20, "cancelled": False}
        self.purchases = []
        self.receipts = []

    def attempt(self, merchant, items, price, hook=None):
        # A proposed transaction cannot enter the writer unless a fresh, atomic
        # authority check at commit passes. No queue or cached approval.
        if hook:
            hook(self)
        a = self.authority
        authorised = not a["cancelled"] and merchant == a["merchant"] and items == a["items"] and price <= a["max_coins"]
        before = len(self.purchases)
        if authorised:
            self.purchases.append({"merchant": merchant, "items": items, "price_coins": price})
        receipt = {"authorised_at_commit": authorised, "writer_entered": authorised, "protected_state_changed": len(self.purchases) != before, "purchase_count": len(self.purchases)}
        self.receipts.append(receipt)
        return receipt

CASES = [
    ("baseline_valid", {}, "ALLOW"),
    ("price_25_coins", {"price": 25}, "HOLD"),
    ("merchant_changed", {"merchant": "Other merchant"}, "HOLD"),
    ("cancelled_before_commit", {"hook": lambda s: s.authority.update(cancelled=True)}, "HOLD"),
    ("items_substituted", {"items": ["wood", "paint"]}, "HOLD"),
    ("limit_lowered_before_commit", {"hook": lambda s: s.authority.update(max_coins=10)}, "HOLD"),
]
results=[]
for name, changes, expected in CASES:
    w=Workshop()
    args={"merchant":"Geppetto's chosen merchant", "items":["wood", "glue"], "price":20}
    args.update(changes)
    receipt=w.attempt(**args)
    observed="ALLOW" if receipt["writer_entered"] else "HOLD"
    passed=(observed==expected and receipt["protected_state_changed"] == (expected=="ALLOW") and receipt["purchase_count"] == (1 if expected=="ALLOW" else 0))
    results.append({"case":name,"expected":expected,"observed":observed,"pass":passed, **receipt})
report={"title":"Twenty-Coin Test — illustrative local reference fixture", "timestamp_utc":datetime.now(timezone.utc).isoformat(), "scope":"Local self-authored Python fixture. NOT an integration test of Harmonic or Tim's implementation.", "results":results, "passed":sum(r['pass'] for r in results), "total":len(results)}
(BASE/'receipt.json').write_text(json.dumps(report,indent=2)+'\n')
print(json.dumps(report,indent=2))
