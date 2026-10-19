#!/usr/bin/env python3
"""Refresh the live-stats section of the profile README from my study-progress API.

Reads competitive-programming, CSES and vocabulary data from the API, renders the charts
to assets/stats/*.png and rewrites the block between the STATS markers in README.md.
Nothing is written unless the required API calls succeed, so a failed run leaves the
README as it was.

Environment:
    STUDY_API_URL    base URL of the API, e.g. https://study-progress.isym.uk
    STUDY_API_TOKEN  bearer token (the API's static API_TOKEN)
"""
import hashlib
import json
import os
import sys
import time
from collections import defaultdict
from datetime import date, datetime, timezone
from pathlib import Path

import matplotlib

matplotlib.use("Agg")
import matplotlib.dates as mdates  # noqa: E402
import matplotlib.pyplot as plt  # noqa: E402
import requests  # noqa: E402
from matplotlib.ticker import FuncFormatter, MaxNLocator  # noqa: E402

ROOT = Path(__file__).resolve().parent.parent
README = ROOT / "README.md"
OUT = ROOT / "assets" / "stats"
HASHES = OUT / ".hashes.json"
START, END = "<!-- STATS:START -->", "<!-- STATS:END -->"

# Facts that no API tracks.
STATIC_FACTS = {"usaco": "Silver", "jlpt": "N1"}

LANGUAGE_NAMES = {"nihongo": "Japanese", "pt": "Portuguese", "zhongwen": "Chinese"}

# Problem-rating bands. Lower bounds match the API's BAND_BOUNDS; -1 is "unrated".
BANDS = {
    "atcoder": {
        -1: ("Unrated", "#6e7781"), 0: ("0-399", "#9a9a9a"), 400: ("400-799", "#a0522d"),
        800: ("800-1199", "#2e9e44"), 1200: ("1200-1599", "#18b8b8"), 1600: ("1600-1999", "#3b82f6"),
        2000: ("2000-2399", "#d4c020"), 2400: ("2400-2799", "#f08a24"), 2800: ("2800+", "#e5484d"),
    },
    "codeforces": {
        -1: ("Unrated", "#6e7781"), 0: ("0-1199", "#9a9a9a"), 1200: ("1200-1399", "#2e9e44"),
        1400: ("1400-1599", "#18b8b8"), 1600: ("1600-1899", "#3b82f6"), 1900: ("1900-2099", "#b455d6"),
        2100: ("2100-2299", "#f0a024"), 2300: ("2300-2399", "#f08a24"), 2400: ("2400-2599", "#e5484d"),
        2600: ("2600-2999", "#d23c41"), 3000: ("3000+", "#9b1c20"),
    },
}
PLATFORM_COLOURS = {"atcoder": "#4c9aff", "codeforces": "#f5a524", "themecp": "#b455d6", "cses": "#2eb872"}
PLATFORM_LABELS = {"atcoder": "AtCoder", "codeforces": "Codeforces", "themecp": "ThemeCP (virtual)", "cses": "CSES"}

INK = "#7d8590"  # readable on both GitHub's light and dark backgrounds


# --------------------------------------------------------------------------- API

class Api:
    def __init__(self, base: str, token: str):
        self.base = base.rstrip("/")
        self.session = requests.Session()
        self.session.headers["Authorization"] = f"Bearer {token}"

    def get(self, path: str, **params):
        last = None
        for attempt in range(3):
            try:
                resp = self.session.get(f"{self.base}{path}", params=params, timeout=30)
                if resp.status_code >= 500:
                    raise requests.HTTPError(f"{resp.status_code} from {path}")
                resp.raise_for_status()
                return resp.json()
            except requests.RequestException as err:
                last = err
                if isinstance(err, requests.HTTPError) and err.response is not None and err.response.status_code < 500:
                    break
                time.sleep(2 * (attempt + 1))
        raise RuntimeError(f"GET {path} failed: {last}")

    def maybe(self, path: str, **params):
        try:
            return self.get(path, **params)
        except RuntimeError as err:
            print(f"warning: {err}", file=sys.stderr)
            return None


# ------------------------------------------------------------------------ charts

def style():
    plt.rcParams.update({
        "figure.facecolor": "none", "axes.facecolor": "none", "savefig.facecolor": "none",
        "text.color": INK, "axes.labelcolor": INK, "axes.edgecolor": INK, "xtick.color": INK, "ytick.color": INK,
        "axes.spines.top": False, "axes.spines.right": False, "axes.grid": True, "grid.color": INK,
        "grid.alpha": 0.2, "grid.linewidth": 0.6, "font.size": 10, "axes.titlesize": 11, "axes.titleweight": "bold",
        "axes.titlelocation": "left", "legend.frameon": False, "legend.labelcolor": INK,
    })


def parse_dates(rows, key="date"):
    return [date.fromisoformat(str(r[key])[:10]) for r in rows]


def date_axis(ax):
    ax.xaxis.set_major_locator(mdates.AutoDateLocator(minticks=3, maxticks=6))
    ax.xaxis.set_major_formatter(mdates.ConciseDateFormatter(ax.xaxis.get_major_locator()))


def thousands(ax, axis="y"):
    fmt = FuncFormatter(lambda v, _: f"{int(v):,}")
    (ax.yaxis if axis == "y" else ax.xaxis).set_major_formatter(fmt)


def band_of(rating: int, platform: str) -> int:
    bounds = sorted(b for b in BANDS[platform] if b >= 0)
    return max((b for b in bounds if b <= rating), default=0)


def chart_solved_over_time(data):
    fig, ax = plt.subplots(figsize=(7.2, 3.6))
    for platform, rows in data.items():
        if len(rows) < 2:
            continue
        xs, ys = parse_dates(rows), [r["solved"] for r in rows]
        ax.plot(xs, ys, color=PLATFORM_COLOURS[platform], lw=2, label=f"{PLATFORM_LABELS[platform]}  {ys[-1]:,}")
        ax.fill_between(xs, ys, color=PLATFORM_COLOURS[platform], alpha=0.12)
    ax.set_title("Problems solved over time")
    ax.legend(loc="upper left")
    ax.set_ylim(bottom=0)
    date_axis(ax)
    return fig


def chart_ratings(data):
    fig, ax = plt.subplots(figsize=(7.2, 3.6))
    for platform, rows in data.items():
        rows = [r for r in rows if r["rating"] is not None]
        if len(rows) < 2:
            continue
        xs, ys = parse_dates(rows), [r["rating"] for r in rows]
        ax.plot(xs, ys, color=PLATFORM_COLOURS[platform], lw=1.8, marker="o", ms=2.5,
                ls="--" if platform == "themecp" else "-", label=f"{PLATFORM_LABELS[platform]}  {ys[-1]:,}")
    ax.set_title("Contest rating")
    ax.legend(loc="upper left")
    date_axis(ax)
    return fig


def chart_difficulty(platform, by_rating, by_band):
    fig, (left, right) = plt.subplots(1, 2, figsize=(10, 3.8), gridspec_kw={"width_ratios": [1, 1.15]})
    label = PLATFORM_LABELS[platform]
    if by_rating:
        xs = [r["rating"] for r in by_rating]
        left.bar(xs, [r["solved"] for r in by_rating], width=90,
                 color=[BANDS[platform][band_of(r["rating"], platform)][1] for r in by_rating])
        left.set_xlim(min(xs) - 100, max(xs) + 150)
        left.set_xlabel("Problem rating")
        left.set_ylabel("Solved")
    left.set_title(f"{label}: difficulty of problems solved")
    if by_band:
        dates = sorted({r["date"] for r in by_band})
        bands = sorted({r["band"] for r in by_band})
        lookup = {(r["date"], r["band"]): r["cumulative"] for r in by_band}
        series = [[lookup.get((d, b), 0) for d in dates] for b in bands]
        right.stackplot([date.fromisoformat(d[:10]) for d in dates], *series,
                        colors=[BANDS[platform].get(b, ("", INK))[1] for b in bands],
                        labels=[BANDS[platform].get(b, (str(b), INK))[0] for b in bands], alpha=0.95)
        right.legend(loc="upper left", fontsize=7, ncol=2, title="Problem rating", title_fontsize=8)
        date_axis(right)
    right.set_title(f"{label}: solved by difficulty over time")
    right.set_ylim(bottom=0)
    fig.tight_layout()
    return fig


def chart_cses(summary, history):
    fig, (left, right) = plt.subplots(1, 2, figsize=(10, 3.8), gridspec_kw={"width_ratios": [1.2, 1]})
    sections = summary["sections"][::-1]
    names = [s["section"] for s in sections]
    left.barh(names, [s["total"] for s in sections], color=INK, alpha=0.22)
    left.barh(names, [s["solved"] for s in sections], color=PLATFORM_COLOURS["cses"])
    for i, s in enumerate(sections):
        left.text(s["total"] + 1, i, f'{s["solved"]}/{s["total"]}', va="center", fontsize=8)
    left.set_title(f'CSES Problem Set: {summary["solved"]}/{summary["total"]} solved')
    left.grid(axis="y", visible=False)
    left.tick_params(axis="y", labelsize=8)
    if history and len(history) >= 2:
        xs, ys = parse_dates(history), [r["solved"] for r in history]
        right.plot(xs, ys, color=PLATFORM_COLOURS["cses"], lw=2)
        right.fill_between(xs, ys, color=PLATFORM_COLOURS["cses"], alpha=0.15)
        right.set_ylim(bottom=0)
        date_axis(right)
    right.set_title("CSES solved over time")
    fig.tight_layout()
    return fig


def chart_languages(series):
    fig, axes = plt.subplots(1, len(series), figsize=(5 * len(series), 3.4), squeeze=False)
    colours = ["#e5484d", "#2eb872", "#f5a524", "#4c9aff"]
    for ax, (name, rows), colour in zip(axes[0], series.items(), colours):
        xs, ys = parse_dates(rows), [r["total_incl_pre_anki"] for r in rows]
        ax.plot(xs, ys, color=colour, lw=2)
        ax.fill_between(xs, ys, color=colour, alpha=0.15)
        ax.set_title(f"{name}: {ys[-1]:,} words")
        ax.set_ylim(bottom=0)
        ax.yaxis.set_major_locator(MaxNLocator(5))
        thousands(ax)
        date_axis(ax)
    fig.tight_layout()
    return fig


def save(name, payload, build):
    """Render and save a chart unless its input data is unchanged since the last run."""
    digest = hashlib.sha256(json.dumps(payload, sort_keys=True, default=str).encode()).hexdigest()
    hashes = json.loads(HASHES.read_text()) if HASHES.exists() else {}
    path = OUT / f"{name}.png"
    if path.exists() and hashes.get(name) == digest:
        return True
    try:
        fig = build()
        fig.savefig(path, dpi=150, bbox_inches="tight", transparent=True)
        plt.close(fig)
    except Exception as err:  # one broken chart should not block the others
        print(f"warning: chart {name} failed: {err}", file=sys.stderr)
        plt.close("all")
        return path.exists()
    hashes[name] = digest
    HASHES.write_text(json.dumps(hashes, indent=1, sort_keys=True) + "\n")
    return True


# ------------------------------------------------------------------------- block

def fmt_platform(s):
    if not s or s.get("solved") is None:
        return "n/a"
    parts = [f"**{s['solved']:,}** solved"]
    if s.get("current_rating"):
        peak = f" (peak {s['max_rating']:,})" if s.get("max_rating") and s["max_rating"] != s["current_rating"] else ""
        parts.append(f"rating **{s['current_rating']:,}**{peak}")
    return "<br>".join(parts)


def build_block(summary, cses, vocab, charts):
    by_platform = {s["platform"]: s for s in summary}
    cells = {"AtCoder": fmt_platform(by_platform.get("atcoder")),
             "Codeforces": fmt_platform(by_platform.get("codeforces"))}
    if cses and cses["total"]:
        cells["CSES"] = f"**{cses['solved']}** / {cses['total']}<br>{cses['solved'] * 100 // cses['total']}% of the set"
    for lang, label in (("nihongo", "日本語"), ("pt", "Português")):
        if vocab.get(lang, {}).get("total_incl_pre_anki", 0) > 0:  # 0 means the deck wasn't found, not "no words"
            extra = f"<br>JLPT {STATIC_FACTS['jlpt']}" if lang == "nihongo" else ""
            cells[label] = f"**{vocab[lang]['total_incl_pre_anki']:,}** words{extra}"
    lines = [
        "## 📈 Live stats", "",
        f"<sub>Pulled daily from my self-hosted study-progress API. Last updated {datetime.now(timezone.utc):%Y-%m-%d}.</sub>", "",
        "| " + " | ".join(cells) + " |", "|" + ":---:|" * len(cells), "| " + " | ".join(cells.values()) + " |", "",
    ]
    extras = [f"**USACO:** {STATIC_FACTS['usaco']}"]
    themecp = by_platform.get("themecp")
    if themecp and themecp.get("current_rating"):
        extras.append(f"**ThemeCP virtual rating:** {themecp['current_rating']:,} over {themecp.get('contests', 0)} contests")
    lines += [" · ".join(extras), ""]

    def img(name, alt, width="100%"):
        return f'<img src="assets/stats/{name}.png" alt="{alt}" width="{width}" />' if name in charts else ""

    row = [img("solved-over-time", "Problems solved over time", "49%"), img("ratings", "Contest rating over time", "49%")]
    lines += ['<p align="center">', *[r for r in row if r], "</p>", ""]
    for platform in ("atcoder", "codeforces"):
        tag = img(f"difficulty-{platform}", f"{PLATFORM_LABELS[platform]} problem difficulty")
        if tag:
            lines += ['<p align="center">', tag, "</p>", ""]
    for name, alt in (("cses", "CSES problem set progress"), ("languages", "Vocabulary growth")):
        tag = img(name, alt)
        if tag:
            lines += ['<p align="center">', tag, "</p>", ""]
    return "\n".join(lines).rstrip() + "\n"


def build_json(summary, cses, vocab, charts):
    """Machine-readable copy of the numbers in the README block, for other sites (e.g. isym.uk)."""
    by_platform = {s["platform"]: s for s in summary}

    def platform(name):
        s = by_platform.get(name) or {}
        return {"solved": s.get("solved"), "rating": s.get("current_rating"), "peak": s.get("max_rating"),
                "contests": s.get("contests")}

    return {
        "updated": datetime.now(timezone.utc).strftime("%Y-%m-%d"),
        "atcoder": platform("atcoder"), "codeforces": platform("codeforces"), "themecp": platform("themecp"),
        "cses": {"solved": cses["solved"], "total": cses["total"]} if cses and cses["total"] else None,
        "words": {LANGUAGE_NAMES.get(k, k.title()): v["total_incl_pre_anki"]
                  for k, v in vocab.items() if v["total_incl_pre_anki"] > 0},
        "usaco": STATIC_FACTS["usaco"], "jlpt": STATIC_FACTS["jlpt"],
        "charts": sorted(charts),
    }


def splice(text, block):
    head, sep, rest = text.partition(START)
    _, sep2, tail = rest.partition(END)
    if not sep or not sep2:
        raise RuntimeError(f"README is missing the {START} / {END} markers")
    return f"{head}{START}\n{block}{END}{tail}"


# -------------------------------------------------------------------------- main

def main() -> int:
    url, token = os.environ.get("STUDY_API_URL"), os.environ.get("STUDY_API_TOKEN")
    if not url or not token:
        print("STUDY_API_URL and STUDY_API_TOKEN must be set", file=sys.stderr)
        return 2
    api = Api(url, token)

    # Required: if any of these fail, leave everything untouched.
    try:
        summary = api.get("/cp/summary")
        vocab = {v["language"]: v for v in api.get("/vocab/totals")}
    except RuntimeError as err:
        print(f"error: {err}", file=sys.stderr)
        return 1

    cses = api.maybe("/cp/cses")
    cumulative = api.maybe("/cp/history/cumulative-solved", group_by="week") or []
    ratings = api.maybe("/cp/history/ratings") or []
    series = {p: [{"date": r["date"], "solved": r["cumulative_solved"]} for r in cumulative if r["platform"] == p]
              for p in ("atcoder", "codeforces")}
    cses_history = (api.maybe("/cp/cses/history", group_by="day") or []) if cses else []
    by_platform_ratings = defaultdict(list)
    for r in ratings:
        by_platform_ratings[r["platform"]].append(r)

    OUT.mkdir(parents=True, exist_ok=True)
    style()
    charts = set()

    def add(name, payload, build):
        if payload and save(name, payload, build):
            charts.add(name)

    add("solved-over-time", series, lambda: chart_solved_over_time(series))
    add("ratings", dict(by_platform_ratings), lambda: chart_ratings(by_platform_ratings))
    for platform in ("atcoder", "codeforces"):
        by_rating = api.maybe("/cp/history/by-rating", platform=platform, bucket_size=100) or []
        by_band = api.maybe("/cp/history/cumulative-solved-by-band", platform=platform, group_by="week") or []
        add(f"difficulty-{platform}", [by_rating, by_band],
            lambda p=platform, a=by_rating, b=by_band: chart_difficulty(p, a, b))
    if cses and cses["total"]:
        add("cses", [cses, cses_history], lambda: chart_cses(cses, cses_history))
    languages = {}
    for lang in vocab:
        rows = api.maybe("/history/vocab", language=lang, group_by="week") or []
        if len(rows) >= 2 and rows[-1]["total_incl_pre_anki"] > 0:
            languages[LANGUAGE_NAMES.get(lang, lang.title())] = rows
    add("languages", languages, lambda: chart_languages(languages))

    block = build_block(summary, cses, vocab, charts)
    README.write_text(splice(README.read_text(encoding="utf-8"), block), encoding="utf-8")
    (OUT / "stats.json").write_text(json.dumps(build_json(summary, cses, vocab, charts), indent=1) + "\n")
    print(f"README stats block updated with {len(charts)} charts")
    return 0


if __name__ == "__main__":
    sys.exit(main())
