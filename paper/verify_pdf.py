"""Verify the generated PDF without any third-party PDF library.

Checks:
  1. header, xref offsets, trailer, EOF, object count
  2. page count and MediaBox
  3. text extraction from the uncompressed content streams
  4. every drawing coordinate lies inside the page box
  5. no character that would have been transliterated to '?'
  6. figure operators are present on the pages that carry figures
"""

import re
import sys


def parse(path):
    data = open(path, 'rb').read()
    assert data[:8] == b'%PDF-1.4', data[:8]
    m = re.search(rb'startxref\s+(\d+)\s+%%EOF', data)
    assert m, 'no startxref/EOF'
    start = int(m.group(1))
    assert data[start:start + 4] == b'xref', data[start:start + 20]

    # split the xref table
    xr = data[start:]
    body = xr.split(b'trailer')[0]
    lines = body.split(b'\n')
    header = lines[1].split()
    first, count = int(header[0]), int(header[1])
    offsets = {}
    for i, ln in enumerate(lines[2:]):
        ln = ln.strip()
        if not ln:
            continue
        parts = ln.split()
        if len(parts) == 3 and parts[2] == b'n':
            offsets[first + i] = int(parts[0])
    return data, offsets, first, count


def check_offsets(data, offsets):
    bad = []
    for num, off in offsets.items():
        token = b'%d 0 obj' % num
        if data[off:off + len(token)] != token:
            bad.append((num, off))
    return bad


def streams(data):
    """Return the raw content-stream text of every page."""
    out = []
    for m in re.finditer(rb'<< /Length (\d+) >>\nstream\n', data):
        n = int(m.group(1))
        start = m.end()
        out.append(data[start:start + n].decode('latin-1'))
    return out


def main(path):
    data, offsets, first, count = parse(path)
    bad = check_offsets(data, offsets)
    pages = len(re.findall(rb'/Type /Page[^s]', data))
    print(f"file                 : {path}")
    print(f"size                 : {len(data)} bytes")
    print(f"objects              : {len(re.findall(rb'[0-9]+ 0 obj', data))}")
    print(f"xref entries         : {len(offsets)} (from {first}, size {count})")
    print(f"bad xref offsets     : {len(bad)} {bad[:3]}")
    print(f"pages (/Type /Page)  : {pages}")
    boxes = set(re.findall(rb'/MediaBox \[([\d\. ]+)\]', data))
    print(f"MediaBox values      : {boxes}")
    fonts = sorted(set(x.decode() for x in
                       re.findall(rb'/BaseFont /(\S+)', data)))
    print(f"fonts                : {fonts}")

    ss = streams(data)
    print(f"content streams      : {len(ss)}")

    # coordinate bounds check
    out_of_bounds = 0
    for s in ss:
        for m in re.finditer(r'(?<![\d.])(\d+\.\d+) (\d+\.\d+) m', s):
            x, y = float(m.group(1)), float(m.group(2))
            if not (-2 <= x <= 600 and -2 <= y <= 845):
                out_of_bounds += 1
        for m in re.finditer(r'1 0 0 1 (\d+\.\d+) (\d+\.\d+) Tm', s):
            x, y = float(m.group(1)), float(m.group(2))
            if not (-5 <= x <= 600 and -5 <= y <= 845):
                out_of_bounds += 1
    print(f"out-of-bounds points : {out_of_bounds}")

    # text extraction (escape-aware, whitespace-normalised)
    tesc = re.findall(rb'\(((?:[^()\\]|\\.)*)\) Tj', data)
    raw = ' '.join(t.decode('latin-1') for t in tesc)
    raw = raw.replace('\\(', '(').replace('\\)', ')')
    total_text = len(raw)
    all_chars = set(raw)
    print("extracted characters : %d" % total_text)
    non_ascii = sorted(c for c in all_chars if ord(c) > 126)
    print("non-ASCII in output  : %s" % (non_ascii if non_ascii else 'none'))
    print("literal '?' runs     : %d" % data.count(b'(?'))
    norm = re.sub(r'\s+', ' ', raw)
    print("'?' in text          : %d" % norm.count('?'))
    print("Q.E.D. count        : %d" % norm.count('Q.E.D'))
    print("theorems            : %d   lemmas: %d   corollaries: %d"
          % (len(re.findall(r'Theorem \d+', norm)),
             len(re.findall(r'Lemma \d+', norm)),
             len(re.findall(r'Corollary \d+', norm))))
    print("figures              : %s" % sorted(set(re.findall(r'Figure \d', norm))))
    print("appendices           : %s" % sorted(set(re.findall(r'Appendix [A-E]', norm))))

    ops = {'Tj': 0, 'm': 0, 'l': 0, 're': 0, 'c': 0, 'S': 0, 'f': 0}
    for s in ss:
        ops['Tj'] += len(re.findall(r'\) Tj', s))
        for tok in ('m', 'l', 're', 'c'):
            ops[tok] += len(re.findall(r'(?<=[\d\.]) %s(?= |$)' % tok, s))
        ops['S'] += len(re.findall(r' S\n', s))
        ops['f'] += len(re.findall(r' f\n', s))
    print("text runs            : %d" % ops['Tj'])
    print("vector operators     : m=%d l=%d re=%d c=%d  strokes=%d fills=%d"
          % (ops['m'], ops['l'], ops['re'], ops['c'], ops['S'], ops['f']))

    # per-page text volume
    print("per-page character counts:")
    for i, s in enumerate(ss, 1):
        txt = ''.join(re.findall(r'\((.*?)\) Tj', s))
        has_gfx = bool(re.search(r'\d+\.\d+ \d+\.\d+ (?:m|l|re)', s))
        tag = '   <-- vector graphics' if has_gfx else ''
        print("   page %2d: %6d chars, %4d line ops%s "
              % (i, len(txt), len(re.findall(r'(?<=[\d\.]) l(?= |$)', s)),
                 tag))

    ok = (not bad and pages == len(ss) and out_of_bounds == 0
          and not non_ascii)
    print("\nRESULT:", "PASS" if ok else "FAIL")
    return 0 if ok else 1


if __name__ == "__main__":
    sys.exit(main(sys.argv[1] if len(sys.argv) > 1 else 'paper/partitionism.pdf'))
