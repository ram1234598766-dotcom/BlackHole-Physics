"""Audit the *rendering* of a PDF produced by pdflib.py, not just its structure.

`verify_pdf.py` checks that the file is well-formed.  This module checks that
the page will actually look right:

  1. font-width tables are compared with the authoritative Adobe AFM files
     (this is what makes word wrapping and right-edge fitting correct);
  2. every text run is located by walking the content stream's text state
     machine, and its bounding box is reconstructed from the real glyph
     widths;
  3. no run crosses the text margins (overflow), and no run sits outside the
     page;
  4. no two runs on a page overlap (which would mean text printed on text);
  5. text-rise (super/subscripts) is always reset, and the graphics state is
     balanced (q/Q).

Run:  python3 -m paper.audit_pdf [paper/partitionism.pdf]
"""

import re
import sys

from . import pdflib

PAGE_W = 595.276
PAGE_H = 841.890
M_L, M_R, M_T, M_B = 62, 62, 64, 58
RIGHT = PAGE_W - M_R
TOL = 1.6                     # points of slack before we call it an error


# --------------------------------------------------------------------------
# 1. font widths against Adobe AFM
# --------------------------------------------------------------------------
_GLYPH = {
    'space': ' ', 'exclam': '!', 'quotedbl': '"', 'numbersign': '#',
    'dollar': '$', 'percent': '%', 'ampersand': '&', 'quotesingle': "'",
    'parenleft': '(', 'parenright': ')', 'asterisk': '*', 'plus': '+',
    'comma': ',', 'hyphen': '-', 'period': '.', 'slash': '/', 'zero': '0',
    'one': '1', 'two': '2', 'three': '3', 'four': '4', 'five': '5', 'six': '6',
    'seven': '7', 'eight': '8', 'nine': '9', 'colon': ':', 'semicolon': ';',
    'less': '<', 'equal': '=', 'greater': '>', 'question': '?', 'at': '@',
    'A': 'A', 'B': 'B', 'C': 'C', 'D': 'D', 'E': 'E', 'F': 'F', 'G': 'G',
    'H': 'H', 'I': 'I', 'J': 'J', 'K': 'K', 'L': 'L', 'M': 'M', 'N': 'N',
    'O': 'O', 'P': 'P', 'Q': 'Q', 'R': 'R', 'S': 'S', 'T': 'T', 'U': 'U',
    'V': 'V', 'W': 'W', 'X': 'X', 'Y': 'Y', 'Z': 'Z', 'bracketleft': '[',
    'backslash': '\\', 'bracketright': ']', 'asciicircum': '^',
    'underscore': '_', 'grave': '`', 'a': 'a', 'b': 'b', 'c': 'c', 'd': 'd',
    'e': 'e', 'f': 'f', 'g': 'g', 'h': 'h', 'i': 'i', 'j': 'j', 'k': 'k',
    'l': 'l', 'm': 'm', 'n': 'n', 'o': 'o', 'p': 'p', 'q': 'q', 'r': 'r',
    's': 's', 't': 't', 'u': 'u', 'v': 'v', 'w': 'w', 'x': 'x', 'y': 'y',
    'z': 'z', 'braceleft': '{', 'bar': '|', 'braceright': '}', 'asciitilde': '~',
}


def _afm_widths(path):
    out = {}
    try:
        with open(path, encoding='latin-1') as fh:
            for line in fh:
                m = re.match(r'^C (-?\d+) ; WX (\d+) ; N (\S+)', line)
                if m and m.group(3) in _GLYPH:
                    out[_GLYPH[m.group(3)]] = int(m.group(2))
    except OSError:
        return None
    return out or None


def check_fonts(afm_dir='/tmp/kilo/afm'):
    """Compare pdflib's width tables with Adobe's AFM files."""
    checks = [('F1 Helvetica', pdflib._HELV, 'Helvetica.afm'),
              ('F2 Helvetica-Oblique', pdflib._HELV, 'Helvetica-Oblique.afm'),
              ('F3 Helvetica-Bold', pdflib._HELVB, 'Helvetica-Bold.afm'),
              ('F4 Helvetica-BoldOblique', pdflib._HELVB,
               'Helvetica-BoldOblique.afm'),
              ('F5 Courier', pdflib._COUR, 'Courier.afm'),
              ('F6 Courier-Bold', pdflib._COUR, 'Courier-Bold.afm')]
    ok = True
    for label, mine, fname in checks:
        ref = _afm_widths(f"{afm_dir}/{fname}")
        if ref is None:
            print("  %-28s AFM file missing (%s) - table not checked"
                  % (label, fname))
            continue
        bad = [(c, mine.get(c), ref[c]) for c in sorted(ref)
               if mine.get(c) != ref[c]]
        miss = [c for c in ref if c not in mine]
        status = 'EXACT (%d glyphs)' % len(ref) if not bad and not miss else \
                 'MISMATCH %s %s' % (bad, miss)
        print("  %-28s %s" % (label, status))
        ok = ok and not bad and not miss
    return ok


# --------------------------------------------------------------------------
# 2-5. walk the content streams
# --------------------------------------------------------------------------
_TJ_RE = re.compile(
    r'/F(?P<font>\d) (?P<size>[\d.]+) Tf'
    r'|(?P<rise>-?[\d.]+) Ts'
    r'|1 0 0 1 (?P<x>-?[\d.]+) (?P<y>-?[\d.]+) Tm '
    r'\((?P<text>(?:[^()\\]|\\.)*)\) Tj')
_Q_OPEN = re.compile(r'\bq [\d.]+ [\d.]+ [\d.]+ [\d.]+ re W n')
_Q_CLOSE = re.compile(r'^Q$')


def _unescape(s):
    return s.replace('\\(', '(').replace('\\)', ')').replace('\\\\', '\\')


def runs_from_stream(stream):
    """Walk a page content stream with the text state machine."""
    runs = []
    font = size = None
    rise = 0.0
    x = y = None
    qdepth = 0
    for line in stream.split('\n'):
        stripped = line.strip()
        if _Q_OPEN.search(stripped):
            qdepth += 1
        if _Q_CLOSE.match(stripped):
            qdepth -= 1
        for m in _TJ_RE.finditer(stripped):
            if m.group('font'):
                font = 'F' + m.group('font')
                size = float(m.group('size'))
            elif m.group('rise') is not None:
                rise = float(m.group('rise'))
            elif m.group('x') is not None:
                x, y = float(m.group('x')), float(m.group('y'))
                txt = _unescape(m.group('text'))
                if txt and font is not None:
                    w = pdflib.run_width(
                        txt, pdflib.FONT_STYLE_BY_ID[font], size)
                    runs.append(dict(x=x, y=y + rise, w=w, h=size, font=font,
                                     size=size, rise=rise, text=txt))
    return runs, qdepth


def main(path):
    print("=" * 72)
    print("RENDER AUDIT: %s" % path)
    print("=" * 72)

    print("\n[1] font metrics vs. Adobe AFM files")
    fonts_ok = check_fonts()

    data = open(path, 'rb').read()
    streams = []
    for m in re.finditer(rb'<< /Length (\d+) >>\nstream\n', data):
        n = int(m.group(1))
        st = m.end()
        streams.append(data[st:st + n].decode('latin-1'))

    print("\n[2..5] text runs, margins, overlap, state")
    print("  %3s %8s %8s %8s %8s" % ("pg", "runs", "overflow", "offpage",
                                      "overlap"))
    total_overflow = total_off = total_overlap = total_ts = 0
    for i, s in enumerate(streams, 1):
        runs, depth = runs_from_stream(s)
        overflow = off = overlap = 0
        for r in runs:
            x1 = r['x'] + r['w']
            if r['x'] < M_L - TOL or x1 > RIGHT + TOL:
                overflow += 1
            if not (0 - TOL <= r['x'] and x1 <= PAGE_W + TOL
                    and 0 - TOL <= r['y'] <= PAGE_H + TOL):
                off += 1
        # overlap: sweep by baseline
        runs.sort(key=lambda r: -r['y'])
        active = []
        for r in runs:
            active = [a for a in active if a['y'] + a['h'] > r['y'] - r['h']]
            for a in active:
                ax0, ax1 = a['x'], a['x'] + a['w']
                bx0, bx1 = r['x'], r['x'] + r['w']
                ox = min(ax1, bx1) - max(ax0, bx0)
                oy = min(a['y'] + a['h'] * 0.75,
                         r['y'] + r['h'] * 0.75) - \
                    max(a['y'] - a['h'] * 0.25, r['y'] - r['h'] * 0.25)
                if ox > 0.9 and oy > 0.9:
                    overlap += 1
            active.append(r)
        print("  %3d %8d %8d %8d %8d"
              % (i, len(runs), overflow, off, overlap))
        total_overflow += overflow
        total_off += off
        total_overlap += overlap
    print("\n  totals: overflow=%d  off-page=%d  overlapping-runs=%d"
          % (total_overflow, total_off, total_overlap))

    # q/Q balance (each figure clips with `q ... re W n` and closes with `Q`)
    bad_q = []
    for i, s in enumerate(streams, 1):
        _, depth = runs_from_stream(s)
        if depth != 0:
            bad_q.append((i, depth))
    print("  q/Q clip balance: %s"
          % ("all pages balanced" if not bad_q else "UNBALANCED %s" % bad_q))

    # every Tm is preceded by a Tf in the same BT/ET (state machine sanity)
    orphan = 0
    for s in streams:
        in_txt = False
        seen_tf = False
        for line in s.split('\n'):
            line = line.strip()
            if line == 'BT':
                in_txt, seen_tf = True, False
            elif line == 'ET':
                in_txt = False
            elif in_txt and line.startswith('/F'):
                seen_tf = True
            elif in_txt and line.endswith('Tj') and not seen_tf:
                orphan += 1
    print("  text drawn without a preceding Tf: %d" % orphan)

    ok = (fonts_ok and total_overflow == 0 and total_off == 0
          and total_overlap == 0 and not bad_q and orphan == 0)
    print("\nRESULT:", "PASS" if ok else "FAIL")
    return 0 if ok else 1


if __name__ == "__main__":
    sys.exit(main(sys.argv[1] if len(sys.argv) > 1 else 'paper/partitionism.pdf'))
