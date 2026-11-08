from pathlib import Path
import csv

root = Path(__file__).resolve().parents[1]
rows = list(csv.DictReader((root / "references/claim-evidence.tsv").open(), delimiter="\t"))
assert len({r["key"] for r in rows}) == len(rows)
assert all(all(r.values()) for r in rows)
def escape(s):
    return s.replace("&", r"\&").replace("%", r"\%").replace("_", r"\_").replace("#", r"\#")
items = []
bib = []
for r in sorted(rows, key=lambda item: (item["author"].casefold(), item["year"])):
    key, author, year, title, url, _ = r.values()
    tex_url = url.replace("%", r"\%").replace("#", r"\#")
    items.append(r"\bibitem[" + escape(author) + "(" + year + ")]{" + key + "}\n"
                 + escape(author.rstrip(".")) + ". " + year.rstrip(".") + ". "
                 + r"\href{" + tex_url + r"}{\emph{" + escape(title) + "}}.")
    bib.append("@misc{" + key + ",\n"
               + "  author = {{" + author + "}},\n"
               + "  title = {{" + title + "}},\n"
               + ("  year = {" + year + "},\n" if year.isdecimal() else "")
               + "  url = {" + url + "}\n}\n")
(root / "references.tex").write_text("\\begin{thebibliography}{99}\n\\phantomsection\\addcontentsline{toc}{chapter}{\\bibname}\n" + "\n\n".join(items) + "\n\\end{thebibliography}\n")
(root / "references/sources.bib").write_text("\n".join(bib))
