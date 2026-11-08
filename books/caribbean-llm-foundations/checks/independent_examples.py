#!/usr/bin/env python3
"""Verify the numerical examples in chapters 1–6 (and addendum 7–8).

Run: python3 book/checks/independent_examples.py [--book PATH] [--precision 40]
No production code or precomputed book results are imported. CSV/JSON and
transcribed problem inputs are shared with the book; displayed results are
extracted from both LaTeX variants, then compared with independently computed
values. Exercise results are printed and compared with the answer key if it
exists. Appendices beyond the solution key are outside the numerical audit.
"""
from __future__ import annotations

import argparse
import csv
import json
import math
import re
import unicodedata
from collections import Counter
from datetime import date, datetime
from decimal import Decimal, ROUND_HALF_UP, localcontext
from fractions import Fraction as F
from itertools import product
from pathlib import Path


def dec(value):
    return Decimal(value.numerator) / Decimal(value.denominator) if isinstance(value, F) else Decimal(value)


def rounded(value, places, precision):
    with localcontext() as ctx:
        ctx.prec = precision
        return dec(value).quantize(Decimal(1).scaleb(-places), rounding=ROUND_HALF_UP)


def at_precisions(fn, places, precision):
    outcomes = []
    for p in (precision, 2 * precision):
        with localcontext() as ctx:
            ctx.prec = p
            outcomes.append(rounded(fn(), places, p))
    if outcomes[0] != outcomes[1]:
        raise ArithmeticError(f"unstable at {precision} and {2 * precision} digits: {outcomes}")
    return F(outcomes[-1])


def read_csv(path):
    with path.open(encoding="utf-8", newline="") as source:
        return list(csv.DictReader(source))


def brace_arg(source, start):
    if source[start] != "{":
        raise ValueError("expected a braced TeX argument")
    level = 1
    for idx in range(start + 1, len(source)):
        char = source[idx]
        if char in "{}" and source[idx - 1] != "\\":
            level += 1 if char == "{" else -1
            if level == 0:
                return source[start + 1:idx], idx + 1
    raise ValueError("unterminated TeX argument")


def bilingual_pairs(source):
    for hit in re.finditer(r"\\B(?=\{)", source):
        first, idx = brace_arg(source, hit.end())
        idx += len(source[idx:]) - len(source[idx:].lstrip())
        second, _ = brace_arg(source, idx)
        yield first, second


def normalize_numbers(line):
    # Both draft editions use decimal points. The two source grouping styles
    # are normalized only within a number; list commas remain separators.
    line = re.sub(r"\\tfrac\s*\{?(\d)\}?\s*\{?(\d)\}?", r"\1/\2", line)
    line = re.sub(r"(?<=\d)(?:\{,\}|\\,|,)(?=\d{3}(?!\d))", "", line)
    line = re.sub(r"(?<![A-Za-z0-9.])(\d+(?:\.\d+)?)\s*\\times\s*10\^\{?(-?\d+)\}?", r"\1e\2", line)
    return re.sub(r"\\(ln|sqrt|times|approx|le|ge)(?=\d)", r"\\\1 ", line)


def read_numbers(line):
    number = r"\d+(?:\.\d+)?(?:[eE][+-]?\d+)?"
    pattern = rf"(?<![\w.])([+-]?{number})(?:/({number}))?"
    return tuple(F(num) / F(den) if den else F(num) for num, den in re.findall(pattern, normalize_numbers(line)))


def normalized_weights(weights):
    total = sum(weights)
    if total <= 0:
        raise ValueError("positive mass required")
    return tuple(F(weight) / total for weight in weights)


def site_scores(row):
    def clip(number):
        return sorted((0, F(number), 100))[1]

    rent, distance = F(row["rent_jmd_month"]), F(row["hub_distance_km"])
    return (clip(row["lunch_count"]), clip((280000 - rent) / 2000), clip(100 - 10 * distance))


def weighted_sum(values, weights):
    return sum((F(x) * F(w) for x, w in zip(values, weights, strict=True)), F(0))


def rank_sites(rows, weights):
    return {r["site_id"]: weighted_sum(site_scores(r), weights) for r in rows}


def loss_and_ppl(probabilities):
    product = dec(math.prod(probabilities))
    loss = -product.ln() / len(probabilities)
    return loss, loss.exp()


def gradient_step(w, target, rate):
    # A symmetric exact difference gives the derivative of this quadratic.
    h = F(1, 123)
    loss = lambda x: (x - target) ** 2 / 2
    slope = (loss(w + h) - loss(w - h)) / (2 * h)
    step = -rate * slope
    return slope, step, w + step


def greedy_pieces(text, vocab):
    result = []
    for word in text.split():
        while word:
            choices = [part for part in vocab if word.startswith(part)]
            if not choices:
                raise ValueError(f"uncovered text: {word!r}")
            part = max(choices, key=len)
            result.append(part)
            word = word[len(part):]
    return tuple(result)


def pair_counts(words):
    return Counter(pair for word, multiplicity in words.items()
                   for _ in range(multiplicity) for pair in zip(word, word[1:]))


def merged(words, pair):
    result = Counter()
    for word, multiplicity in words.items():
        i, output = 0, []
        while i < len(word):
            if word[i:i + 2] == pair:
                output.append("".join(pair))
                i += 2
            else:
                output.append(word[i])
                i += 1
        result[tuple(output)] += multiplicity
    return result


def attend(bases, values, last_index):
    mass = [base if i < last_index else 0 for i, base in enumerate(bases)]
    weights = normalized_weights(mass)
    return weights, weighted_sum(values, weights)


def cosine_squared(q, d):
    numerator = sum(a * b for a, b in zip(q, d, strict=True))
    square_norm = lambda x: sum(a * a for a in x)
    return F(numerator ** 2, square_norm(q) * square_norm(d)), (numerator > 0) - (numerator < 0)


def active_notices(rows, route, service_day, as_of):
    eligible = [r for r in rows
                if (r["origin"], r["destination"]) == route
                and r["service_date"] == service_day
                and r["authority"] == "dispatch"
                and datetime.fromisoformat(r["issued_local"]) <= datetime.fromisoformat(as_of)]
    superseded = {r["supersedes"] for r in eligible if r["supersedes"]}
    return tuple(sorted((r["notice_id"], r["departure_local"])
                        for r in eligible if r["notice_id"] not in superseded))


def search_scores(reference, hits):
    overlap = len(reference.intersection(hits))
    return (F(overlap, len(reference)) if reference else None, F(overlap, len(hits)) if hits else None)


def nucleus(sorted_probs, threshold):
    retained = []
    for p in sorted_probs:
        retained.append(p)
        if sum(retained) >= threshold:
            return normalized_weights(retained)
    raise ValueError("threshold exceeds supplied probability mass")


def cache_bytes(layers, positions, heads, width, bytes_per_scalar):
    # Calculate bytes for one position and independently scale by position.
    per_position = sum(width * bytes_per_scalar for _ in range(layers * heads) for _ in ("K", "V"))
    return positions * per_position


def wait_seconds(first, output_length, later_rate):
    return first + sum((F(1, later_rate) for _ in range(output_length - 1)), F(0))


class Gate:
    def __init__(self, book, precision):
        self.book, self.precision = book, precision
        self.ch = {int(p.name[:2]): p.read_text(encoding="utf-8")
                   for p in (book / "chapters").glob("[0-9][0-9]-*.tex")}
        answers = book / "appendices/solutions.tex"
        self.answers = {}
        self.has_answer_key = answers.exists()
        if self.has_answer_key:
            pieces = re.split(r"\\section\*\{\\B\{Chapter (\d+)\.", answers.read_text(encoding="utf-8"))
            for i in range(1, len(pieces), 2):
                items = [line for line in pieces[i + 1].splitlines() if line.startswith(r"\item ")]
                self.answers[int(pieces[i])] = tuple(tuple(bilingual_pairs(line))[0] for line in items)
        self.results = []
        self.answer_values = {}

    def check(self, title, observed, oracle):
        self.results.append((title, observed == oracle, observed, oracle))

    def approximate(self, fn, places):
        return at_precisions(fn, places, self.precision)

    def pair(self, chapter, en_anchor):
        matches = [(en, es) for en, es in bilingual_pairs(self.ch[chapter]) if en_anchor in en]
        if len(matches) != 1:
            raise ValueError(f"chapter {chapter}: expected one bilingual paragraph for {en_anchor!r}, found {len(matches)}")
        return matches[0]

    def prose(self, chapter, en_anchor, *values, es_values=None):
        en, es = self.pair(chapter, en_anchor)
        self.check(f"Ch {chapter} EN: {en_anchor}", read_numbers(en), tuple(map(F, values)))
        self.check(f"Ch {chapter} ES: {en_anchor}", read_numbers(es), tuple(map(F, es_values or values)))

    def exercise(self, key, *values):
        self.answer_values[key] = values

    def solution(self, chapter, item, *values):
        if chapter in self.answers:
            for language, body in zip(("EN", "ES"), self.answers[chapter][item - 1], strict=True):
                self.check(f"Solution {chapter}.{item} {language}", read_numbers(body), tuple(map(F, values)))


def controls(g):
    # Numerically known outcomes, including a reject through the same
    # comparison method used for the actual manuscripts.
    c = Gate(g.book, g.precision)
    c.check("one third plus two thirds", F(1, 3) + F(2, 3), 1)
    c.check("one-unit perturbation", F(1, 3) + F(2, 3), 2)
    c.check("last displayed digit perturbation", rounded(Decimal("0.12496"), 4, g.precision), Decimal("0.1249"))
    c.check("clean round at displayed precision", rounded(Decimal("0.12496"), 4, g.precision), Decimal("0.1250"))
    g.check("controls: positives accepted and perturbations rejected",
            tuple(ok for _, ok, _, _ in c.results), (True, False, False, True))
    print("Control: rejected the one-unit and last-displayed-digit perturbations." if
          [ok for _, ok, _, _ in c.results] == [True, False, False, True] else "Control: unexpected verdict.")


def chapter1(g):
    rows = read_csv(g.book / "data/patty-sites.csv")
    oracle_table = tuple((r["site_id"], r["area"], *map(F, (r["lunch_count"], r["rent_jmd_month"], r["hub_distance_km"]))) for r in rows)
    table = tuple((i, name, *read_numbers(f"{count} {rent} {dist}"))
                  for i, name, count, rent, dist in re.findall(r"^(K\d+) & (.*?) & (.*?) & (.*?) & (.*?)\\\\", g.ch[1], re.M))
    g.check("Ch 1 shared EN/ES site table", table, oracle_table)
    primary = tuple(map(F, (".55", ".25", ".20")))
    secondary = tuple(map(F, (".40", ".45", ".15")))
    exercise = tuple(map(F, (".80", ".10", ".10")))
    primary_scores = rank_sites(rows, primary)
    secondary_scores = rank_sites(rows, secondary)
    exercise_scores = rank_sites(rows, exercise)
    chart_lines = re.findall(r"\\addplot[^\n]+?coordinates\s*\{([^}]+)\}", g.ch[1])
    plotted = tuple(tuple((key, F(score)) for key, score in re.findall(r"\((K\d+),([\d.]+)\)", line)) for line in chart_lines)
    g.check("Ch 1 shared EN/ES plot coordinates", plotted, (tuple(primary_scores.items()), tuple(secondary_scores.items())))
    site2 = next(r for r in rows if r["site_id"] == "K2")
    ds, rs, ac = site_scores(site2)
    rent_gap = F(site2["rent_jmd_month"]) - 80000
    g.prose(1, "At Papine", 100, 80000, 2000, rent_gap, 100, rent_gap / 2000, rs,
            F(site2["hub_distance_km"]), 100, 10 * F(site2["hub_distance_km"]), ac, 100)
    g.prose(1, "Papine receives", 0, 100, *primary, ds * primary[0], rs * primary[1], ac * primary[2],
            primary_scores["K2"], primary_scores["K3"], primary_scores["K1"])
    g.prose(1, "The blue bars", *primary, *secondary)
    g.check("Ch 1 winners and third place", (max(primary_scores, key=primary_scores.get),
            min(primary_scores, key=primary_scores.get), max(secondary_scores, key=secondary_scores.get)),
            ("K2", "K1", "K3"))
    g.prose(1, "If the estimates are", 80, "0.7", 30, "0.3", "0.7", 80, "0.3", 30,
            weighted_sum((80, 30), (F(7, 10), F(3, 10))), 30, 80)
    probs = F(1, 2), F(1, 4), F(1, 8)
    nll = g.approximate(lambda: loss_and_ppl(probs)[0], 4)
    ppl = g.approximate(lambda: loss_and_ppl(probs)[1], 0)
    product = math.prod(probs)
    power_of_two = tuple(p.denominator.bit_length() - 1 for p in probs)
    average_power = sum(power_of_two) // len(power_of_two)
    g.prose(1, "their respective prefixes", *probs, *[p.denominator for p in probs], 2,
            *power_of_two, average_power, 2 ** average_power, nll, ppl, product, 1 / ppl, ppl)
    w, target, rate = F(1, 4), F(3, 4), F(1, 5)
    slope, step, next_w = gradient_step(w, target, rate)
    g.prose(1, "For a single weight", F(1, 2), target, 2, target, w, rate, slope, step, next_w, target)
    g.check("Ch 1 controls: clipping and zero-gradient fixed point",
            (site_scores(dict(lunch_count="160", rent_jmd_month="0", hub_distance_km="12")),
             gradient_step(target, target, rate)),
            ((100, 100, 0), (0, 0, target)))
    g.exercise("1.1", *exercise_scores.items(), max(exercise_scores, key=exercise_scores.get))
    all_contributions = [number for row in rows for number in (
        *(score * w for score, w in zip(site_scores(row), exercise, strict=True)),
        exercise_scores[row["site_id"]])]
    g.solution(1, 1, *all_contributions)
    if 1 in g.answers:
        for lang, body in zip(("EN", "ES"), g.answers[1][0], strict=True):
            winner = re.search(r"(K\d+)\s+(?:wins|gana)", body)
            g.check(f"Solution 1.1 {lang} winner", winner[1] if winner else None, max(exercise_scores, key=exercise_scores.get))
    ex_probs = (F(1, 8),) * 2
    ex_ppl = g.approximate(lambda: loss_and_ppl(ex_probs)[1], 0)
    g.exercise("1.3", "ln(8)", g.approximate(lambda: loss_and_ppl(ex_probs)[0], 6), ex_ppl)
    g.solution(1, 3, ex_ppl, ex_ppl, g.approximate(lambda: loss_and_ppl(ex_probs)[0], 4), ex_ppl)


def chapter2(g):
    records = json.loads((g.book / "data/language-samples.json").read_text(encoding="utf-8"))
    table = tuple((text, tuple(a.split(" | ")), tuple(b.split(" | "))) for text, a, b in
                  re.findall(r"^\\textit\{([^}]+)\} & \\texttt\{([^}]+)\} & \\texttt\{([^}]+)\}\\\\", g.ch[2], re.M))
    g.check("Ch 2 shared EN/ES token table", table, tuple((r["text"], tuple(r["a"]), tuple(r["b"])) for r in records))
    vocabs = {side: {p for r in records for p in r[side]} for side in ("a", "b")}
    words = sum(len(r["text"].split()) for r in records)
    pieces_a, pieces_b = (sum(len(greedy_pieces(r["text"], vocabs[side])) for r in records) for side in ("a", "b"))
    for row in records:
        g.check("Ch 2 longest-match trace: " + row["variety"],
                tuple(greedy_pieces(row["text"], vocabs[side]) for side in ("a", "b")),
                tuple(tuple(row[side]) for side in ("a", "b")))
    g.prose(2, "A and B produce", pieces_a, pieces_b)
    g.prose(2, "The table has", words, F(pieces_a, words), 1, F(pieces_b, words),
            g.approximate(lambda: F(pieces_b, words), 2))
    word_bag = {tuple("guagua"): 3, tuple("guante"): 1, tuple("agua"): 1}
    counts = pair_counts(word_bag)
    after_first = merged(word_bag, ("g", "u"))
    after_second = merged(after_first, ("gu", "a"))
    # Chapter spells out its pair counts; read exact words separately.
    en, es = g.pair(2, "A simplified byte-pair")
    g.check("Ch 2 EN BPE counts", (en.count("eight times"), counts[("g", "u")], counts[("u", "a")],
                                  pair_counts(after_first)[("gu", "a")], after_second[("gua", "gua")]), (2, 8, 8, 8, 3))
    g.check("Ch 2 ES BPE counts", es.count("ocho veces"), 2)
    composed, decomposed = "ó", unicodedata.normalize("NFD", "ó")
    g.check("Ch 2 Unicode sizes", (len(composed), len(composed.encode()), len(decomposed), len(decomposed.encode())), (1, 2, 2, 3))
    en, es = g.pair(2, "A code point and a byte")
    g.check("Ch 2 EN UTF-8 prose", ("one Unicode code point" in en, "two bytes" in en, "three UTF-8 bytes" in en), (True, True, True))
    g.check("Ch 2 ES UTF-8 prose", ("un punto de código Unicode" in es, "dos bytes" in es, "tres bytes UTF-8" in es), (True, True, True))
    embedding, position = tuple(map(F, ("0.2", "0.4"))), tuple(map(F, ("0.1", "0")))
    g.prose(2, "A toy row", *embedding, *position, *(a + b for a, b in zip(embedding, position, strict=True)))
    weights3, out3 = attend((1, 2, 3), (0, 3, 6), 3)
    weights2, out2 = attend((1, 2, 3), (0, 3, 6), 2)
    g.prose(2, r"Use \(d_k=1\)", 1, 1, 0, 2, 3, 0, 3, 6, 3,
            *weights3, 0, weights3[0], 3, weights3[1], 6, weights3[2], out3, 2, *weights2, out2)
    weights1, out1 = attend((1, 2, 3), (0, 3, 6), 1)
    g.check("Ch 2 controls: masked value perturbation",
            attend((1, 2, 300), (0, 3, -1234), 2), (weights2, out2))
    spanish = next(r for r in records if r["variety"] == "Caribbean Spanish")
    spans = tuple(len(greedy_pieces(spanish["text"], vocabs[side])) for side in ("a", "b"))
    denominator = len(spanish["text"].split())
    fertility = tuple(F(n, denominator) for n in spans)
    g.exercise("2.1", *fertility)
    g.solution(2, 1, spans[0], denominator, fertility[0], spans[1], denominator, fertility[1])
    g.exercise("2.2", weights1, out1)
    g.solution(2, 2, *weights1, out1)
    flat_w, flat_value = attend((1, 1, 1), (0, 3, 6), 3)
    constant_value = attend((1, 1, 1), (7, 7, 7), 3)[1]
    g.exercise("2.3", flat_value, constant_value)
    g.solution(2, 3, flat_w[0], 0, 3, 6, 3, flat_value, 7, constant_value)


def chapter3(g):
    probs = tuple(map(F, (".6", ".5", ".8")))
    g.prose(3, "The complete reply has probability", *probs, math.prod(probs), math.prod(probs[:-1]))
    # Derive the 6 multiplier from the stated forward plus backward work.
    cost = lambda n, d: (2 + 2 * 2) * n * d
    g.prose(3, "Multiply parameters by processed tokens", 10, 8, 2 * 10**9, cost(10**8, 2 * 10**9),
            2 * 10**8, 10, 9)
    g.check("Ch 3 equal-operation compute plans", cost(10**8, 2 * 10**9), cost(2 * 10**8, 10**9))
    g.prose(3, "positive fitted amplitudes", F(1, 2))
    g.check("Ch 3 scaling thought experiment", F(1, math.isqrt(4)), F(1, 2))
    seqs = len(list((i, j, k) for i in range(4) for j in range(2) for k in range(8)))
    g.prose(3, "one update covers", 4, 2, 8, seqs, 512, seqs * 512)
    n, window = 2048, 256
    bound = n * window
    exact = sum(min(row, window) for row in range(1, n + 1))
    g.prose(3, "A 256-position window", window, n, n, window, bound)
    g.check("Ch 3 causal-window boundary versus triangular correction",
            exact, bound - window * (window - 1) // 2)
    g.check("Ch 3 causal controls: 0, 1, and 3 full causal positions",
            tuple(sum(k <= q for q in range(n) for k in range(n)) for n in (0, 1, 3)), (0, 1, 6))
    exprobs = tuple(map(F, (".4", ".5", ".5")))
    full, prefix = math.prod(exprobs), math.prod(exprobs[:-1])
    g.exercise("3.1", full, prefix)
    g.solution(3, 1, *exprobs[:-1], prefix, exprobs[-1], full)
    ratio = F(cost(1, 1), cost(3, 1))
    g.exercise("3.2", ratio)
    if 3 in g.answers:
        for lang, body in zip(("EN", "ES"), g.answers[3][1], strict=True):
            matches = re.search(r"(?:by three|entre tres)\b", body)
            g.check(f"Solution 3.2 {lang} data multiplier", F(1, 3) if matches else None, ratio)
    exseqs = len(list((i, j, k) for i in range(3) for j in range(2) for k in range(4)))
    g.exercise("3.3", exseqs * 256)
    g.solution(3, 3, 3, 2, 4, exseqs, exseqs, 256, exseqs * 256)
    print(f"Ch 3 sliding window: published loose bound {bound:,}; exact included pairs {exact:,}.")


def month_day(cell, year):
    hit = re.fullmatch(r"(\d{1,2})\s+(?:de\s+)?(?:May|mayo|may\.?)(?:\s+(\d\d:\d\d))?", cell.strip(), re.I)
    if hit is None:
        raise ValueError(f"could not parse May date {cell!r}")
    return date(year, 5, int(hit[1])).isoformat() + (f"T{hit[2]}" if hit[2] else "")


def lang_cell(cell, language):
    hit = re.search(r"\\B(?=\{)", cell)
    if hit is None:
        return cell
    en, end = brace_arg(cell, hit.end())
    end += len(cell[end:]) - len(cell[end:].lstrip())
    es, end = brace_arg(cell, end)
    return cell[:hit.start()] + lang_cell((en, es)[language], language) + lang_cell(cell[end:], language)


def chapter4(g):
    rows = read_csv(g.book / "data/ferry-notices.csv")
    sq1, sign1 = cosine_squared((1, 1), (1, 2))
    sq2, sign2 = cosine_squared((1, 1), (1, 0))
    cos1 = g.approximate(lambda: sign1 * dec(sq1).sqrt(), 3)
    cos2 = g.approximate(lambda: sign2 * dec(sq2).sqrt(), 3)
    g.prose(4, "For query", -1, 1, 1, 1, 1, 2, math.isqrt(sq1.numerator), sq1.denominator, cos1,
            1, 0, math.isqrt(sq2.numerator), sq2.denominator, cos2)
    g.check("Ch 4 cosine rank; negative and orthogonal controls",
            (cos1 > cos2, cosine_squared((1, 1), (-1, -1)), cosine_squared((1, 1), (1, -1))),
            (True, (F(1), -1), (F(0), 0)))
    records = re.findall(r"^(N\d+) & (.*?) & (.*?) & (.*?) & (.*?) & (.*?)\\\\", g.ch[4], re.M)
    oracle = tuple((r["notice_id"], r["origin"], r["destination"], r["service_date"], r["issued_local"],
                    r["departure_local"], r["authority"], r["supersedes"]) for r in rows[:5])
    labels = (("Dispatch", "Unverified", "Dispatch, replaces"), ("Despacho", "Sin verificar", "Despacho, sustituye"))
    for lang, (dispatch, unverified, replaces) in enumerate(labels):
        table = []
        for ident, route, service, issued, depart, status in records:
            origin, destination = route.split(r" \(\to\) ")
            status = lang_cell(status, lang)
            replaced = status[len(replaces) + 1:] if status.startswith(replaces + " ") else ""
            issuer = "dispatch" if status == dispatch or replaced else "unverified" if status == unverified else status
            table.append((ident, origin, destination, month_day(lang_cell(service, lang), 2031),
                          month_day(lang_cell(issued, lang), 2031), depart, issuer, replaced))
        g.check(f"Ch 4 {('EN', 'ES')[lang]} ferry table and record status", tuple(table), oracle)
    g.prose(4, "Fictional May 2031", 2031)
    route = "Antigua", "Barbuda"
    lookup = lambda service, as_of: active_notices(rows, route, service, as_of)
    before = lookup("2031-05-18", "2031-05-18T06:30")
    boundary = lookup("2031-05-18", "2031-05-18T06:45")
    after = lookup("2031-05-18", "2031-05-18T07:15")
    g.check("Ch 4 dispatch result before, at, and after correction issuance", (before, boundary, after),
            ((("N02", "07:30"),), (("N03", "09:00"),), (("N03", "09:00"),)))
    for lang, body in zip(("EN", "ES"), g.pair(4, "Keep only notices for the Antigua--Barbuda route")):
        ids = tuple(re.findall(r"N\d+", body))
        g.check(f"Ch 4 {lang} applicable and excluded records in prose", ids,
                ("N01", "N04", "N05", boundary[0][0], before[0][0], after[0][0], boundary[0][0], before[0][0]))
        g.check(f"Ch 4 {lang} worked lookup times in prose", tuple(re.findall(r"\d\d:\d\d", body)),
                ("07:15", after[0][1], "06:30", before[0][1]))
    no_conflict_yet = lookup("2031-05-20", "2031-05-19T13:59")
    conflict = lookup("2031-05-20", "2031-05-19T14:00")
    jointly_issued = max(datetime.fromisoformat(r["issued_local"]) for r in rows
                         if r["notice_id"] in {record for record, _ in conflict})
    g.prose(4, "The companion CSV includes a second case", date.fromisoformat("2031-05-20").day,
            jointly_issued.hour, jointly_issued.minute, jointly_issued.day)
    g.check("Ch 4 no records before dispatch tie; conflict at issuance",
            (no_conflict_yet, conflict), ((), (("N06", "07:00"), ("N07", "08:00"))))
    g.check("Ch 4 dispatch order independence", active_notices(list(reversed(rows)), route, "2031-05-20", "2031-05-19T14:00"), conflict)
    tampered = [dict(r, authority="dispatch") if r["notice_id"] == "N05" else r for r in rows]
    g.check("Ch 4 negative control: granting N05 authority creates a conflict",
            active_notices(tampered, route, "2031-05-18", "2031-05-18T07:15"), (("N03", "09:00"), ("N05", "08:15")))
    recall, precision = search_scores({"a", "b", "c"}, ("a", "x", "b", "y"))
    g.prose(4, "For a question with at least", recall, precision)
    g.check("Ch 4 empty relevance set yields undefined recall", search_scores(set(), ("a",)), (None, F(0)))
    g.exercise("4.1", before[0], after[0], "N05 unverified; also not published at 06:30")
    ex_recall, ex_precision = search_scores({"a", "b", "c", "d", "e"}, ("c", "b", "x", "a"))
    g.exercise("4.2", ex_recall, ex_precision)
    g.solution(4, 2, ex_recall, ex_recall, ex_precision, ex_precision)
    g.exercise("4.3", after[0], "Fare absent")
    if 4 in g.answers:
        for lang, answer1, answer3 in zip(("EN", "ES"), g.answers[4][0], g.answers[4][2], strict=True):
            g.check(f"Solution 4.1 {lang} date/authority trace",
                    (tuple(re.findall(r"\d\d:\d\d", answer1)), tuple(re.findall(r"N\d+", answer1))),
                    (("06:30", "07:15"), (before[0][0], after[0][0], before[0][0], "N05")))
            g.check(f"Solution 4.3 {lang} answer notice and supported time",
                    (tuple(re.findall(r"\d\d:\d\d", answer3)), set(re.findall(r"N\d+", answer3))),
                    ((after[0][1],), {after[0][0]}))
    print("Ch 4 conflict: N06 (07:00), N07 (08:00), first jointly eligible 2031-05-19 14:00 local.")


def chapter5(g):
    probs = (F(1, 2), F(1, 2))
    mean_penalty_ln_argument = F(1, math.isqrt(math.prod(probs).denominator))
    g.prose(5, "For two target tokens", probs[0], 1 / mean_penalty_ln_argument)
    count_full = lambda width, height: len(range(width * height))
    count_factors = lambda width, height, rank: len(range(rank * width)) + len(range(height * rank))
    g.prose(5, "The thin matrix", 512, 512, 8, count_full(512, 512), 8, 512, 512, count_factors(512, 512, 8))
    prob_tie = normalized_weights((1, 1))[0]
    prob_ahead = normalized_weights((3, 1))[0]
    g.prose(5, "Equal scores give", prob_tie, 3, 1, 1, F(1, 3), prob_ahead)
    a, b, a_ref, b_ref = F(3, 5), F(3, 10), F(2, 5), F(2, 5)
    a_ratio, b_ratio = a / a_ref, b / b_ref
    odds_ratio = a_ratio / b_ratio
    a_preferred, b_preferred = normalized_weights((a_ratio, b_ratio))
    dpo_loss = g.approximate(lambda: -dec(a_preferred).ln(), 4)
    g.prose(5, "If the current policy gives", a, b, a_ref, a_ratio, b_ratio, 1, odds_ratio,
            a_preferred, 1 / a_preferred, dpo_loss)
    g.check("Ch 5 DPO controls: equal and sign-reversed log odds",
            (normalized_weights((a_ratio, a_ratio))[0], normalized_weights((b_ratio, a_ratio))[0]),
            (F(1, 2), 1 - a_preferred))
    g.prose(5, "For a fictional audit", 18, 20, 3, 5, 21, 25, 100 * F(18 + 3, 20 + 5), 100 * F(18, 20),
            100 * F(3, 5), 3 + 1, 5 + 1, g.approximate(lambda: F(4, 6) * 100, 0))
    g.exercise("5.1", prob_tie)
    g.solution(5, 1, prob_tie)
    factors, full = count_factors(256, 512, 4), count_full(256, 512)
    g.exercise("5.2", factors, full)
    g.solution(5, 2, 4, 256, 512, factors, 256, 512, full)
    swapped_loss = g.approximate(lambda: -dec(b_preferred).ln(), 4)
    g.exercise("5.3", "-ln(2)", b_preferred, "ln(3)", swapped_loss)
    g.solution(5, 3, odds_ratio, b_preferred, 1 / b_preferred, swapped_loss)
    if 5 in g.answers:
        for lang, body in zip(("EN", "ES"), g.answers[5][2], strict=True):
            g.check(f"Solution 5.3 {lang} sign of swapped logit", bool(re.search(r"\\\(-\\ln\s*2\\\)", body)), True)


def chapter6(g):
    first, length, rate = F(6, 5), 80, 20
    g.prose(6, "The first token is already included", 1, first, rate, length - 1, length,
            first, F(length - 1, rate), wait_seconds(first, length, rate))
    g.check("Ch 6 latency control: one output token", wait_seconds(first, 1, rate), first)
    branches, completions = tuple(map(F, (".60", ".40"))), tuple(map(F, (".50", ".90")))
    path = tuple(a * b for a, b in zip(branches, completions, strict=True))
    g.prose(6, "In a toy tree", *branches, *completions, *path)
    g.check("Ch 6 greedy first choice differs from best complete route", (branches[0] > branches[1], path[0] < path[1]), (True, True))
    temp1, temp_half = normalized_weights((1, 3)), normalized_weights((1, 3**2))
    g.prose(6, "With two logits", 1, 0, 3, *temp1, 1, *temp_half, F(1, 2))
    probs = tuple(map(F, (".50", ".25", ".15", ".10")))
    kept = nucleus(probs, F(7, 10))
    mass = sum(probs[:len(kept)])
    g.prose(6, "Use four sorted probabilities", *probs, F(7, 10), mass, probs[0] / mass, kept[0],
            probs[1] / mass, kept[1], F(1, 2))
    g.check("Ch 6 nucleus boundary: at threshold versus just above",
            (nucleus(probs, F(1, 2)), nucleus(probs, F(5001, 10000))), ((F(1),), kept))
    raw_weights = 7 * 10**9 * 2
    ideal_4bit = F(7 * 10**9 * 4, 8)
    g.prose(6, "14 billion bytes", F(raw_weights, 10**9), g.approximate(lambda: F(raw_weights, 1024**3), 1), F(ideal_4bit, 10**9))
    positions, layers, heads, width, scalar = 4096, 32, 8, 128, 2
    payload = lambda n: cache_bytes(layers, n, heads, width, scalar)
    g.prose(6, "The first factor of two", layers, positions, heads, width, scalar, payload(positions),
            F(payload(positions), 1024**2), 1024, F(payload(1024), 1024**2), positions)
    plot = re.search(r"\\addplot[^\n]+?coordinates\s*\{([^}]+)\}", g.ch[6])[1]
    points = tuple((int(n), int(y)) for n, y in re.findall(r"\((\d+),(\d+)\)", plot))
    g.check("Ch 6 shared EN/ES KV plot coordinates", points, tuple((n, F(payload(n), 1024**2)) for n in range(0, 4097, 1024)))
    g.prose(6, "The slope is", F(payload(1), 1024))
    ex_kept = nucleus(probs, F(4, 5))
    g.exercise("6.1", *ex_kept, F(0))
    g.solution(6, 1, sum(probs[:2]), sum(probs[:3]), *ex_kept, sum(ex_kept))
    ex_wait = wait_seconds(F(4, 5), 40, 13)
    g.exercise("6.2", ex_wait)
    g.solution(6, 2, F(4, 5), F(39, 13), ex_wait, 39)
    half_payload = cache_bytes(layers, positions, heads // 2, width, scalar)
    g.exercise("6.3", half_payload, F(half_payload, 1024**2))
    g.solution(6, 3, F(payload(positions), 1024**2), F(half_payload, 1024**2))


def allocations(rows, shipment):
    ranges = [range(int(r["minimum_crates"]), int(r["maximum_crates"]) + 1) for r in rows]
    weights = [int(r["priority_points_per_crate"]) for r in rows]
    return tuple((*allocation, sum(a * w for a, w in zip(allocation, weights, strict=True)))
                 for allocation in product(*ranges) if sum(allocation) == shipment)


def majority_three(p):
    return sum((math.prod(p if success else 1 - p for success in outcomes)
                for outcomes in product((False, True), repeat=3) if sum(outcomes) >= 2), F(0))


def coverage_error(requested, answered, errors):
    return (F(answered, requested) if requested else None,
            F(errors, answered) if answered else None)


def chapter7(g):
    rows = read_csv(g.book / "data/shipment.csv")
    table = tuple((name, *map(int, numbers)) for name, *numbers in
                  re.findall(r"^(Carriacou|Petite Martinique) & (\d+) & (\d+) & (\d+)\\\\", g.ch[7], re.M))
    oracle_table = tuple((r["island"], *map(int, (r["minimum_crates"], r["maximum_crates"],
                                                r["priority_points_per_crate"]))) for r in rows)
    g.check("Ch 7 shared EN/ES allocation table", table, oracle_table)
    shipment = 72
    feasible = allocations(rows, shipment)
    best_c, best_p, best_u = max(feasible, key=lambda allocation: allocation[-1])
    _, p_min, p_max, _ = oracle_table[1]
    g.prose(7, r"More \(c\) gives", shipment, shipment, p_max, shipment - p_max, p_min, shipment - p_min,
            feasible[0][0], feasible[-1][0], best_c, best_p, best_u)
    changed = [dict(rows[0], maximum_crates="40"), rows[1]]
    max_total = sum(int(r["maximum_crates"]) for r in changed)
    g.prose(7, "the largest total is", 40, p_max, max_total, shipment, 40, shipment - 40, shipment)
    g.check("Ch 7 reduced cap infeasible and wrong second allocation breaches cap",
            (allocations(changed, shipment), shipment - 40 > p_max), ((), True))
    plot_lines = re.findall(r"\\addplot[^\n]+?coordinates\s*\{([^}]+)\}", g.ch[7])
    points = tuple(tuple((int(x), int(y)) for x, y in re.findall(r"\((\d+),(\d+)\)", line)) for line in plot_lines)
    g.check("Ch 7 shared EN/ES crate plot coordinates", points,
            (tuple((c, u) for c, _, u in feasible), ((best_c, best_u),)))
    g.check("Ch 7 independent symbolic check over every feasible solution",
            tuple((c, u) for c, _, u in feasible), tuple((c, shipment + c) for c in range(42, 49)))
    g.prose(7, r"At \(p=0.7\)", 2, 1, 3, F(7, 10), majority_three(F(7, 10)))
    g.check("Ch 7 majority boundaries", tuple(majority_three(p) for p in (F(0), F(1, 2), F(1))), (0, F(1, 2), 1))
    loose, loose_errors = coverage_error(20, 16, 2)
    strict, strict_errors = coverage_error(20, 12, 1)
    g.prose(7, "A stricter policy", 16, 20, 100 * loose, 100 * loose_errors, 12, 100 * strict,
            g.approximate(lambda: strict_errors * 100, 1))
    g.check("Ch 7 coverage with no answers", coverage_error(20, 0, 0), (0, None))
    ex_feasible = allocations([dict(rows[0], maximum_crates="45"), rows[1]], shipment)
    ex_best = max(ex_feasible, key=lambda a: a[-1])
    g.exercise("7.1", *ex_best)
    g.solution(7, 1, ex_feasible[0][0], ex_feasible[-1][0], shipment, *ex_best)
    half, sure = F(1, 2), F(1)
    g.exercise("7.2", majority_three(half), majority_three(sure))
    g.solution(7, 2, half, 3 * half**2 * (1 - half), half**3, majority_three(half), sure, majority_three(sure))
    ex_cover, ex_error = coverage_error(30, 24, 3)
    g.exercise("7.3", ex_cover, ex_error)
    g.solution(7, 3, ex_cover, 100 * ex_cover, ex_error, 100 * ex_error)


def chapter8(g):
    rows = read_csv(g.book / "data/regional-observations.csv")
    by_id = {row["record_id"]: row for row in rows}
    num = lambda ident: F(by_id[ident]["value"])
    values = [(r["place"], F(r["value"])) for r in rows if r["record_id"] in {f"T0{i}" for i in range(1, 7)}]
    region, published = num("T07"), num("T08")
    total = sum(value for _, value in values)
    share = g.approximate(lambda: 100 * total / region, 1)
    g.prose(8, "34.2 million international overnight", region, int(by_id["T07"]["period"]), 28, 2025)
    g.prose(8, "The displayed sum is", 100, total, share, published)
    block = g.ch[8]
    plot = re.search(r"\\addplot[^\n]+?coordinates\s*\{([^}]+)\}", block)[1]
    points = tuple((F(x), int(y)) for x, y in re.findall(r"\(([\d.]+),(\d+)\)", plot))
    tick_match = re.search(r"yticklabels=(?=\{)", block)
    tick_labels, _ = brace_arg(block, tick_match.end())
    labels = tick_labels.split(",")
    expected = tuple(sorted(values, key=lambda x: x[1]))
    for language in range(2):
        es_names = {"Las Bahamas": "The Bahamas", "República Dominicana": "Dominican Republic"}
        places = [lang_cell(label.strip(), language) for label in labels]
        g.check(f"Ch 8 {('EN', 'ES')[language]} CTO destination labels and plot values",
                tuple((es_names.get(places[i], places[i]), value) for value, i in points), expected)
    growth = lambda before, after: 100 * (after / before - 1)
    all_old, all_new, food_old, food_new = map(num, ("J01", "J02", "J03", "J04"))
    all_calc = g.approximate(lambda: growth(all_old, all_new), 4)
    food_calc = g.approximate(lambda: growth(food_old, food_new), 4)
    g.prose(8, "The change from displayed values is", 2025, all_old, all_new, 100, all_new, all_old, all_old,
            all_calc, num("J05"), food_old, food_new, food_calc, num("J06"))
    g.check("Ch 8 all-items agrees at one decimal; food display does not",
            (g.approximate(lambda: growth(all_old, all_new), 1) == num("J05"),
             g.approximate(lambda: growth(food_old, food_new), 1) == num("J06")), (True, False))
    f_old, f_new = F("157.14"), F("158.56")
    g.check("Ch 8 rounding counterexample: compatible hidden food indices",
            (g.approximate(lambda: f_old, 1), g.approximate(lambda: f_new, 1),
             g.approximate(lambda: growth(f_old, f_new), 1)), (food_old, food_new, num("J06")))
    upper = 100 * (total + len(values) * F(".05")) / (region - F(".05"))
    g.check("Ch 8 CTO: 0.1m display rounding alone cannot reach reported rounded share",
            upper < published - F(".5"), True)
    ferry = read_csv(g.book / "data/ferry-notices.csv")
    for anchor, as_of in (("Query at 07:15, 18 May", "2031-05-18T07:15"), ("Query at 06:30, 18 May", "2031-05-18T06:30")):
        line, = [line for line in block.splitlines() if anchor in line]
        _, expected_states, _ = tuple(bilingual_pairs(line))
        ids = tuple(re.findall(r"N\d+", text)[0] for text in expected_states)
        current = active_notices(ferry, ("Antigua", "Barbuda"), "2031-05-18", as_of)
        actual_ids = (current[0][0],) * 2 if len(current) == 1 else tuple(record for record, _ in current)
        g.check(f"Ch 8 capstone EN/ES {anchor.strip()} unique record IDs", ids, actual_ids)
    g.exercise("8.1", total, share, published)
    g.solution(8, 1, total, region, share, published)
    g.exercise("8.2", num("J06"), food_calc)
    g.solution(8, 2, num("J06"), 100, food_new, food_old, food_old, food_calc)
    g.check("Ch 8 regional data labels STATIN division 01 without ambiguity",
            by_id["J06"]["measure"], "reported_monthly_food_and_non_alcoholic_beverages_change")
    if 8 in g.answers:
        for lang, prompt, answer, division in zip(("EN", "ES"), g.pair(8, "Write a prompt for the published STATIN"),
                                                  g.answers[8][1], ("food and non-alcoholic beverages",
                                                                  "alimentos y bebidas no alcohólicas"), strict=True):
            g.check(f"Solution 8.2 {lang} and exercise name STATIN division 01", (division in prompt, division in answer), (True, True))
        unverified = next(r for r in ferry if r["notice_id"] == "N05")
        g.check("Ch 8 solution 8.3 notice N05 is unverified", unverified["authority"], "unverified")
        for lang, body in zip(("EN", "ES"), g.answers[8][2], strict=True):
            g.check(f"Solution 8.3 {lang} catches unverified record",
                    (tuple(re.findall(r"\d\d:\d\d", body)), tuple(re.findall(r"N\d+", body))),
                    (("07:00", unverified["departure_local"]), ("N03", unverified["notice_id"], unverified["notice_id"])))


def fmt(value):
    if isinstance(value, tuple):
        return "(" + ", ".join(fmt(item) for item in value) + ")"
    if isinstance(value, dict):
        return repr(value)
    return str(value)


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--book", type=Path, default=Path(__file__).resolve().parents[1])
    parser.add_argument("--precision", type=int, default=40, help="lower Decimal precision, at least 24 digits")
    parser.add_argument("--verbose", action="store_true", help="also list each accepted comparison")
    parser.add_argument("--base-only", action="store_true", help="omit the addendum checks for chapters 7–8")
    args = parser.parse_args()
    if args.precision < 24:
        parser.error("--precision must be at least 24 digits")
    g = Gate(args.book, args.precision)
    controls(g)
    if g.has_answer_key:
        expected_chapters = tuple(range(1, 7)) + (() if args.base_only else tuple(n for n in (7, 8) if n in g.ch))
        g.check("Answer-key item inventory for checked chapters",
                tuple(len(g.answers.get(n, ())) for n in expected_chapters), (4,) * len(expected_chapters))
    for check in (chapter1, chapter2, chapter3, chapter4, chapter5, chapter6):
        check(g)
    if not args.base_only:
        for n, check in ((7, chapter7), (8, chapter8)):
            if n in g.ch:
                check(g)
    for title, ok, actual, expected in g.results:
        if not ok:
            print(f"FAIL {title}\n    found {fmt(actual)}\n    expected {fmt(expected)}")
        elif args.verbose:
            print(f"PASS {title}")
    print("Exercise oracles:")
    for key, values in g.answer_values.items():
        print(f"  {key}: {fmt(values)}")
    failed = sum(not ok for _, ok, _, _ in g.results)
    print(f"Arithmetic and data gate: {len(g.results)-failed}/{len(g.results)} comparisons passed; "
          f"Decimal precisions {args.precision} and {2 * args.precision}.")
    return int(failed > 0)


if __name__ == "__main__":
    raise SystemExit(main())
