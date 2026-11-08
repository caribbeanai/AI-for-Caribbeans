from pathlib import Path
from place_cases import indexed_places

root = Path(__file__).resolve().parents[1]
rows = list(indexed_places())
codes = {
    "660", "028", "533", "044", "052", "535", "092", "136", "192", "531",
    "212", "214", "308", "312", "332", "388", "474", "500", "630", "652",
    "659", "662", "663", "670", "534", "780", "796", "850",
}
core = [r["code"] for r in rows if r["group"] == "core"]
assert len(core) == len(codes) and set(core) == codes
assert all(all(r.values()) for r in rows)

def pair(en, es):
    def escape(s):
        return s.replace("&", r"\&").replace("%", r"\%")
    return r"\B{" + escape(en) + "}{" + escape(es) + "}"

for group in ("core", "islands", "wider"):
    items = [r for r in rows if r["group"] == group]
    content = [
        pair(r["place_en"], r["place_es"]) + r"\newline\texttt{" + r["case_id"] + "} & " +
        pair(r["task_en"], r["task_es"]) + r"\\[3pt]"
        for r in items
    ]
    (root / f"appendices/places-{group}.tex").write_text("\n".join(content) + "\n")
    print(f"{group}: {len(items)}")
