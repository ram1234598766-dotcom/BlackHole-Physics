"""A minimal, dependency-free PDF writer with a small typesetting engine.

Why this exists: the build environment has no pandoc, no LaTeX, no wkhtmltopdf,
no weasyprint, no reportlab.  Rather than give up on producing a PDF, this
module writes PDF 1.4 by hand:

  * the 14 standard Type1 fonts (Helvetica family, Courier family) with their
    real WinAnsi glyph widths, so that word wrapping and centring are correct;
  * text placement with the Tj operator and explicit Tm matrices;
  * true super/subscripts via font-size and baseline changes;
  * vector graphics (polylines, rectangles, filled paths, circles) so that
    figures can be drawn from data;
  * a flow layout: paragraphs, headings, tables, code blocks, figures, page
    breaks, footers and page numbers.

Only ASCII is emitted.  Every non-ASCII character in the source text is
transliterated by `ascii()` before it reaches the PDF (Greek -> Latin, arrows
-> "->", and so on), because WinAnsiEncoding has no glyphs for them.
"""

import math

# --------------------------------------------------------------------------
# Standard Type1 font metrics, in 1/1000 em (the standard AFM widths).
# --------------------------------------------------------------------------
_HELV = {
    ' ': 278, '!': 278, '"': 355, '#': 556, '$': 556, '%': 889, '&': 667,
    "'": 191, '(': 333, ')': 333, '*': 389, '+': 584, ',': 278, '-': 333,
    '.': 278, '/': 278, '0': 556, '1': 556, '2': 556, '3': 556, '4': 556,
    '5': 556, '6': 556, '7': 556, '8': 556, '9': 556, ':': 278, ';': 278,
    '<': 584, '=': 584, '>': 584, '?': 556, '@': 1015, 'A': 667, 'B': 667,
    'C': 722, 'D': 722, 'E': 667, 'F': 611, 'G': 778, 'H': 722, 'I': 278,
    'J': 500, 'K': 667, 'L': 556, 'M': 833, 'N': 722, 'O': 778, 'P': 667,
    'Q': 778, 'R': 722, 'S': 667, 'T': 611, 'U': 722, 'V': 667, 'W': 944,
    'X': 667, 'Y': 667, 'Z': 611, '[': 278, '\\': 278, ']': 278, '^': 469,
    '_': 556, '`': 333, 'a': 556, 'b': 556, 'c': 500, 'd': 556, 'e': 556,
    'f': 278, 'g': 556, 'h': 556, 'i': 222, 'j': 222, 'k': 500, 'l': 222,
    'm': 833, 'n': 556, 'o': 556, 'p': 556, 'q': 556, 'r': 333, 's': 500,
    't': 278, 'u': 556, 'v': 500, 'w': 722, 'x': 500, 'y': 500, 'z': 500,
    '{': 334, '|': 260, '}': 334, '~': 584,
}
_HELVB = {
    ' ': 278, '!': 333, '"': 474, '#': 556, '$': 556, '%': 889, '&': 722,
    "'": 238, '(': 333, ')': 333, '*': 389, '+': 584, ',': 278, '-': 333,
    '.': 278, '/': 278, '0': 556, '1': 556, '2': 556, '3': 556, '4': 556,
    '5': 556, '6': 556, '7': 556, '8': 556, '9': 556, ':': 333, ';': 333,
    '<': 584, '=': 584, '>': 584, '?': 611, '@': 975, 'A': 722, 'B': 722,
    'C': 722, 'D': 722, 'E': 667, 'F': 611, 'G': 778, 'H': 722, 'I': 278,
    'J': 556, 'K': 722, 'L': 611, 'M': 833, 'N': 722, 'O': 778, 'P': 667,
    'Q': 778, 'R': 722, 'S': 667, 'T': 611, 'U': 722, 'V': 667, 'W': 944,
    'X': 667, 'Y': 667, 'Z': 611, '[': 333, '\\': 278, ']': 333, '^': 584,
    '_': 556, '`': 333, 'a': 556, 'b': 611, 'c': 556, 'd': 611, 'e': 556,
    'f': 333, 'g': 611, 'h': 611, 'i': 278, 'j': 278, 'k': 556, 'l': 278,
    'm': 889, 'n': 611, 'o': 611, 'p': 611, 'q': 611, 'r': 389, 's': 556,
    't': 333, 'u': 611, 'v': 556, 'w': 778, 'x': 556, 'y': 556, 'z': 500,
    '{': 389, '|': 280, '}': 389, '~': 584,
}
_COUR = {c: 600 for c in _HELV}

FONTS = {
    'body':       ('F1', 'Helvetica'),
    'bodyi':      ('F2', 'Helvetica-Oblique'),
    'bold':       ('F3', 'Helvetica-Bold'),
    'boldi':      ('F4', 'Helvetica-BoldOblique'),
    'mono':       ('F5', 'Courier'),
    'monob':      ('F6', 'Courier-Bold'),
}
_WIDTHS = {'F1': _HELV, 'F2': _HELV, 'F3': _HELVB, 'F4': _HELVB, 'F5': _COUR,
           'F6': _COUR}

_TRANSLIT = str.maketrans({
    '—': '--', '–': '-', '→': '->', '←': '<-', '↔': '<->', '⇒': '=>',
    '≤': '<=', '≥': '>=', '≠': '!=', '≈': '~', '∝': ' prop. ', '·': '*',
    '×': 'x', '÷': '/', '±': '+/-', '−': '-', '‑': '-', '−': '-',
    '’': "'", '‘': "'", '“': '"', '”': '"', 'ℓ': 'l', 'π': 'pi',
    'γ': 'gamma', 'δ': 'delta', 'Δ': 'Delta', 'α': 'alpha', 'κ': 'kappa',
    'λ': 'lambda', 'μ': 'mu', 'ω': 'omega', 'σ': 'sigma', 'τ': 'tau',
    'ρ': 'rho', 'θ': 'theta', 'Ω': 'Omega', 'Φ': 'Phi', 'Ψ': 'Psi',
    'ξ': 'xi', 'η': 'eta', 'ζ': 'zeta', 'ε': 'eps', 'Λ': 'Lambda',
    '℃': 'C', '∞': 'infinity', '√': 'sqrt', '∑': 'sum', '∫': 'int',
    '∂': 'd', '∈': ' in ', '⊂': ' subset ', '∪': ' union ', '∩': ' inter ',
    '⁻': '-', '⁰': '0', '¹': '1', '²': '2', '³': '3', '⁴': '4', '⁵': '5',
    '⁶': '6', '⁷': '7', '⁸': '8', '⁹': '9',
    '₀': '0', '₁': '1', '₂': '2', '₃': '3',
    '✓': 'OK', '✗': 'X', '•': '*', '…': '...',
    # Latin-1 / Latin Extended letters that appear in author names
    'á': 'a', 'à': 'a', 'â': 'a', 'ä': 'ae', 'å': 'a',
    'é': 'e', 'è': 'e', 'ê': 'e', 'ë': 'e',
    'í': 'i', 'î': 'i', 'ï': 'i', 'ó': 'o', 'ô': 'o',
    'ö': 'oe', 'ú': 'u', 'ü': 'ue', 'ñ': 'n',
    'ç': 'c', 'ł': 'l', 'Ł': 'L', 'ß': 'ss',
    'ć': 'c', 'ą': 'a', 'ę': 'e', 'š': 's',
    'ž': 'z', 'Ž': 'z', 'ĥ': 'h', 'đ': 'd',
    'Á': 'A', 'É': 'E', 'Í': 'I', 'Ó': 'O', 'Ú': 'U',
    'Ñ': 'N', 'Č': 'C',
    # physics typography used in the sources
    'ħ': 'hbar', '☉': 'M_sun', '★': '*',
    '≳': '>~', '∼': '~', '§': 'Sec.', '⟩': '>',
    '∝': ' prop. ', '̄': '', ' ': ' ', ' ': ' ',
    ' ': ' ', ' ': ' ', ' ': ' ',
})


def ascii_text(s):
    """Transliterate to plain ASCII (WinAnsi-safe)."""
    out = []
    for ch in s:
        if ord(ch) < 128:
            out.append(ch)
        else:
            rep = _TRANSLIT.get(ord(ch))
            if rep is None:
                raise ValueError(
                    "character %r (U+%04X) has no ASCII rendering; add it to "
                    "_TRANSLIT before building" % (ch, ord(ch)))
            elif isinstance(rep, int):
                out.append(chr(rep))
            else:
                out.append(rep)
    return ''.join(out)


def esc(s):
    """Escape a PDF string."""
    return s.replace('\\', r'\\').replace('(', r'\(').replace(')', r'\)')


# --------------------------------------------------------------------------
# Rich-text runs: (text, style, size, script) where script in '', 'sup', 'sub'
# --------------------------------------------------------------------------
def parse_markup(s):
    """Turn a tiny markup language into a list of display runs.

    **bold**, *italic*, `mono`, ^{superscript}, _{subscript}
    """
    runs = []
    i = 0
    n = len(s)
    while i < n:
        if s.startswith('**', i):
            j = s.find('**', i + 2)
            if j < 0:
                runs.append((s[i:], 'body', 0, ''))
                break
            runs.append((s[i + 2:j], 'bold', 0, ''))
            i = j + 2
        elif s[i] == '*':
            j = s.find('*', i + 1)
            if j < 0:
                runs.append((s[i:], 'body', 0, ''))
                break
            runs.append((s[i + 1:j], 'bodyi', 0, ''))
            i = j + 1
        elif s[i] == '`':
            j = s.find('`', i + 1)
            if j < 0:
                runs.append((s[i:], 'body', 0, ''))
                break
            runs.append((s[i + 1:j], 'mono', 0, ''))
            i = j + 1
        elif s.startswith('^{', i):
            j = s.find('}', i + 2)
            if j < 0:
                runs.append((s[i:], 'body', 0, ''))
                break
            runs.append((s[i + 2:j], 'body', 0, 'sup'))
            i = j + 1
        elif s.startswith('_{', i):
            j = s.find('}', i + 2)
            if j < 0:
                runs.append((s[i:], 'body', 0, ''))
                break
            runs.append((s[i + 2:j], 'body', 0, 'sub'))
            i = j + 1
        else:
            j = i
            while j < n:
                ch = s[j]
                if ch in '*`':
                    break
                if ch == '^' and j + 1 < n and s[j + 1] == '{':
                    break
                if ch == '_' and j + 1 < n and s[j + 1] == '{':
                    break
                j += 1
            if j == i:
                j = i + 1
            runs.append((s[i:j], 'body', 0, ''))
            i = j
    return runs


class Run:
    __slots__ = ('text', 'style', 'size', 'script', 'width')

    def __init__(self, text, style, size, script):
        self.text = text
        self.style = style
        self.size = size
        self.script = script
        self.width = run_width(text, style, size)


def run_width(text, style, size):
    fid = FONTS[style][0]
    tab = _WIDTHS[fid]
    w = 0.0
    for ch in ascii_text(text):
        w += tab.get(ch, _HELV['?'] if '_' in fid else 556)
    return w * size / 1000.0


class Doc:
    """Accumulates pages and writes a PDF file."""

    PAGE_W = 595.276            # A4 in points
    PAGE_H = 841.890
    MARGIN_L = 62
    MARGIN_R = 62
    MARGIN_T = 64
    MARGIN_B = 58

    def __init__(self, title='', author='', subject=''):
        self.title = title
        self.author = author
        self.subject = subject
        self.pages = []            # list of list of ops
        self.buf = []
        self._new_page()
        self.y = self.PAGE_H - self.MARGIN_T
        self.page_number = 1
        self.buf = []              # current content stream

    # -- low level --------------------------------------------------------
    def _new_page(self):
        if self.buf:
            self.pages.append(self.buf)
        self.buf = []
        self.ops = self.buf
        self.y = self.PAGE_H - self.MARGIN_T
        self.page_number = len(self.pages) + 1

    def _op(self, s):
        self.buf.append(s)

    def _emit_text(self, x, y, runs, size, color=None, align='left'):
        """Emit one line of runs at (x, y) with baseline y."""
        # measure
        total = sum(r.width for r in runs)
        if align == 'center':
            x = x - total / 2.0
        elif align == 'right':
            x = x - total
        if color:
            self._op(f"{color[0]} {color[1]} {color[2]} rg")
        self._op("BT")
        cx = x
        for r in runs:
            if not r.text:
                continue
            fid = FONTS[r.style][0]
            sz = r.size
            rise = 0.0
            if r.script == 'sup':
                sz = round(size * 0.66, 2)
                rise = round(size * 0.34, 2)
            elif r.script == 'sub':
                sz = round(size * 0.66, 2)
                rise = round(-size * 0.18, 2)
            self._op(f"/{fid} {sz:.2f} Tf")
            if rise:
                self._op(f"{rise:.2f} Ts")
            self._op(f"1 0 0 1 {cx:.2f} {y:.2f} Tm ({esc(ascii_text(r.text))}) Tj")
            if rise:
                self._op("0 Ts")
            cx += r.width
        self._op("ET")
        if color:
            self._op("0 0 0 rg")
        return total

    # -- layout primitives -------------------------------------------------
    def _space_left(self):
        return self.y - self.MARGIN_B

    def _ensure(self, h):
        if self._space_left() < h:
            self.page_break()

    def page_break(self):
        self._emit_footer()
        self._new_page()

    def _emit_footer(self):
        self._op("0 0 0 rg")
        self._op(f"{self.MARGIN_L} {self.MARGIN_B - 16} m "
                 f"{self.PAGE_W - self.MARGIN_R} {self.MARGIN_B - 16} l "
                 f"0.6 w S")
        self._emit_text(self.PAGE_W / 2.0, self.MARGIN_B - 28,
                        [Run("", 'body', 0, '')] , 8, align='center')
        txt = f"{self._footer_left}    |    page {self.page_number}"
        runs = [Run(t, 'body', 8, '') for t in (txt,)]
        self._emit_text(self.PAGE_W - self.MARGIN_R, self.MARGIN_B - 28,
                        runs, 8, align='right', color=(0.35, 0.35, 0.35))

    _footer_left = 'Partitionism'

    # -- text blocks -------------------------------------------------------
    def spacer(self, pts=6):
        self.y -= pts

    def para(self, text, size=9.5, style='body', indent=0, leading=13.2,
             space_after=6.0, color=None, align='left', width_frac=1.0):
        """Flow a paragraph, wrapping on the available width."""
        avail = (self.PAGE_W - self.MARGIN_L - self.MARGIN_R - indent) * width_frac
        runs = [Run(t, st, size, sc) for (t, st, sz, sc) in parse_markup(text)]
        if style != 'body':
            runs = [Run(r.text, style, size, r.script) if r.style == 'body'
                    else r for r in runs]
        line = []
        line_w = 0.0
        lines = []
        for r in runs:
            # split on spaces so that wrapping can happen
            words = r.text.split(' ')
            for k, word in enumerate(words):
                piece = word + (' ' if k < len(words) - 1 else '')
                if not piece:
                    continue
                pw = run_width(piece, r.style, r.size)
                if line_w + pw > avail and line:
                    lines.append((line, line_w))
                    line, line_w = [], 0.0
                sub = Run(piece, r.style, r.size, r.script)
                # measure without the trailing space for the fit test
                if piece.endswith(' '):
                    sub.width = run_width(piece, sub.style, sub.size)
                line.append(sub)
                line_w += sub.width
        if line:
            lines.append((line, line_w))
        first = True
        for ln, lw in lines:
            need = leading
            if self._space_left() < need:
                self.page_break()
            if first:
                first = False
            x = self.MARGIN_L + indent
            self._emit_text(x, self.y - size, ln, size, color=color,
                            align=align if len(lines) == 1 else 'left')
            self.y -= leading
        self.y -= space_after

    def heading(self, text, level=1, number=None):
        size = {0: 19, 1: 13.5, 2: 11.5, 3: 10.2}[level]
        style = 'bold'
        before = {0: 10, 1: 16, 2: 12, 3: 9}[level]
        after = {0: 8, 1: 5, 2: 4, 3: 3}[level]
        label = f"{number}   {text}" if number else text
        need = before + size + after
        if self._space_left() < need + 24:
            self.page_break()
        self.y -= before
        if level <= 1:
            self._op(f"{self.MARGIN_L} {self.y - size + 2:.2f} m "
                     f"{self.PAGE_W - self.MARGIN_R} {self.y - size + 2:.2f} l "
                     f"0.9 w S")
        self._emit_text(self.MARGIN_L, self.y - size,
                        [Run(label, style, size, '')], size)
        self.y -= size + after

    def rule(self, weight=0.6, space=6):
        if self._space_left() < space * 2:
            self.page_break()
        self.y -= space
        self._op(f"{self.MARGIN_L} {self.y:.2f} m "
                 f"{self.PAGE_W - self.MARGIN_R} {self.y:.2f} l "
                 f"{weight} w 0.75 0.75 0.75 RG S")
        self.y -= space

    def code(self, text, size=7.8, leading=10.4):
        """A monospace block, no wrapping (source must be pre-broken)."""
        for raw in text.split('\n'):
            if self._space_left() < leading:
                self.page_break()
            self._op(f"0.96 0.96 0.97 rg "
                     f"{self.MARGIN_L} {self.y - leading + 2:.2f} "
                     f"{self.PAGE_W - self.MARGIN_L - self.MARGIN_R} "
                     f"{leading:.2f} re f")
            self._emit_text(self.MARGIN_L + 4, self.y - size + 1.2,
                            [Run(raw, 'mono', size, '')], size)
            self.y -= leading
        self.y -= 6

    def table(self, rows, widths=None, size=8.2, header=True, leading=10.6,
              align=None, title=None):
        """A bordered table.  `rows` is a list of lists of marked-up strings."""
        if title:
            if self._space_left() < 28:
                self.page_break()
            self._emit_text(self.MARGIN_L, self.y - 9,
                            [Run(title, 'bold', 9, '')], 9)
            self.y -= 14
        total = self.PAGE_W - self.MARGIN_L - self.MARGIN_R
        if widths is None:
            widths = [1.0 / len(rows[0])] * len(rows[0])
        widths = [w / sum(widths) * total for w in widths]
        if align is None:
            align = ['left'] * len(widths)
        rendered = []
        for r_i, row in enumerate(rows):
            style = 'bold' if (header and r_i == 0) else 'body'
            cells = []
            for c_i, cell in enumerate(row):
                runs = [Run(t, style if st == 'body' else st, size, sc)
                        for (t, st, sz, sc) in parse_markup(cell)]
                cells.append(runs)
            rendered.append(cells)
        # row heights: allow wrapping inside a cell
        for cells in rendered:
            rh = 0.0
            for c_i, runs in enumerate(cells):
                avail = widths[c_i] - 8
                lines = self._wrap_runs(runs, avail)
                rh = max(rh, len(lines) * leading + 6)
            self._need(rh)
            y0 = self.y - rh
            for c_i, runs in enumerate(cells):
                lines = self._wrap_runs(runs, widths[c_i] - 8)
                x = self.MARGIN_L + sum(widths[:c_i]) + 4
                for li, ln in enumerate(lines):
                    a = (align[c_i] if c_i < len(align) else 'left')
                    w = sum(r.width for r in ln)
                    xx = x if a == 'left' else (x + (widths[c_i] - 8 - w) / 2
                                                if a == 'center' else
                                                x + widths[c_i] - 8 - w)
                    self._emit_text(xx, y0 + 4 + (len(lines) - 1 - li) * leading,
                                    ln, size)
                self._op(f"{self.MARGIN_L + sum(widths[:c_i]):.2f} {y0:.2f} "
                         f"{widths[c_i]:.2f} {rh:.2f} re 0.4 w S")
            self._op(f"{self.MARGIN_L} {y0:.2f} "
                     f"{total:.2f} {rh:.2f} re 0.8 w S")
            self.y = y0
        self.y -= 8

    def _wrap_runs(self, runs, avail):
        line, line_w, lines = [], 0.0, []
        for r in runs:
            words = r.text.split(' ')
            for k, word in enumerate(words):
                piece = word + (' ' if k < len(words) - 1 else '')
                if not piece:
                    continue
                sub = Run(piece, r.style, r.size, r.script)
                if line_w + sub.width > avail and line:
                    lines.append(line)
                    line, line_w = [], 0.0
                line.append(sub)
                line_w += sub.width
        if line:
            lines.append(line)
        return lines

    def _need(self, h):
        if self._space_left() < h:
            self.page_break()

    # -- vector graphics ---------------------------------------------------
    def figure(self, draw_fn, height, title=None, caption=None):
        """draw_fn(d) issues drawing commands; (0,0) is bottom-left of figure."""
        cap_h = (len(caption) // 90 + 1) * 11.0 if caption else 0.0
        need = height + (18 if title else 0) + cap_h + 24
        if self._space_left() < need + 10:
            self.page_break()
        if title:
            self._emit_text(self.MARGIN_L, self.y - 9, [Run(title, 'bold', 9, '')], 9)
            self.y -= 14
        x0 = self.MARGIN_L
        y0 = self.y - height
        w = self.PAGE_W - self.MARGIN_L - self.MARGIN_R
        self._op(f"q {x0:.2f} {y0:.2f} {w:.2f} {height:.2f} re W n")
        draw_fn(_Surface(self, x0, y0, w, height))
        self._op("Q")
        self.y = y0 - 6
        if caption:
            self.para(caption, size=8, style='bodyi', leading=10.5,
                      space_after=8, color=(0.3, 0.3, 0.3))
        else:
            self.y -= 8

    # -- finish ------------------------------------------------------------
    def save(self, path):
        self._emit_footer()
        self.pages.append(self.buf)
        n_obj = 3 + 6 + 2 * len(self.pages) + 1
        objs = {}
        # 1 catalog, 2 pages, 3..8 fonts
        font_objs = {}
        for i, (name, (fid, base)) in enumerate(FONTS.items()):
            obj_num = 3 + i
            font_objs[fid] = f"{obj_num} 0 R"
        kids = []
        first_page_obj = 9
        for p in range(len(self.pages)):
            kids.append(f"{first_page_obj + 2 * p} 0 R")
        objs[1] = ("<< /Type /Catalog /Pages 2 0 R >>")
        objs[2] = ("<< /Type /Pages /Count %d /Kids [%s] >>"
                   % (len(self.pages), ' '.join(kids)))
        for i, (name, (fid, base)) in enumerate(FONTS.items()):
            objs[3 + i] = ("<< /Type /Font /Subtype /Type1 /BaseFont /%s "
                           "/Encoding /WinAnsiEncoding >>" % base)
        for p in range(len(self.pages)):
            stream = self._stream(self.pages[p])
            objs[first_page_obj + 2 * p] = (
                "<< /Type /Page /Parent 2 0 R /MediaBox [0 0 %.4f %.4f] "
                "/Resources << /Font << %s >> /ProcSet [/PDF /Text] >> "
                "/Contents %d 0 R >>"
                % (self.PAGE_W, self.PAGE_H,
                   ' '.join(f"/{fid} {font_objs[fid]}" for fid in
                            ['F1', 'F2', 'F3', 'F4', 'F5', 'F6']),
                   first_page_obj + 2 * p + 1))
            objs[first_page_obj + 2 * p + 1] = stream
        info_num = first_page_obj + 2 * len(self.pages)
        objs[info_num] = ("<< /Title (%s) /Author (%s) /Subject (%s) "
                          "/Creator (pdflib.py) /Producer (pdflib.py) >>"
                          % (esc(ascii_text(self.title)),
                             esc(ascii_text(self.author)),
                             esc(ascii_text(self.subject))))
        out = bytearray()
        out += b"%PDF-1.4\n%\xe2\xe3\xcf\xd3\n"
        offsets = {}
        for num in sorted(objs):
            offsets[num] = len(out)
            body = objs[num]
            if isinstance(body, tuple):        # stream
                head, data = body
                out += ("%d 0 obj\n%s\nstream\n" % (num, head)).encode('latin-1')
                out += data
                out += b"\nendstream\nendobj\n"
            else:
                out += ("%d 0 obj\n%s\nendobj\n" % (num, body)).encode('latin-1')
        xref_at = len(out)
        n = max(objs) + 1
        out += ("xref\n0 %d\n" % n).encode('latin-1')
        out += b"0000000000 65535 f \n"
        for num in range(1, n):
            out += ("%010d 00000 n \n" % offsets[num]).encode('latin-1')
        out += ("trailer\n<< /Size %d /Root 1 0 R /Info %d 0 R >>\n"
                % (n, info_num)).encode('latin-1')
        out += ("startxref\n%d\n%%%%EOF\n" % xref_at).encode('latin-1')
        with open(path, 'wb') as fh:
            fh.write(bytes(out))
        return len(self.pages)

    @staticmethod
    def _stream(ops):
        data = ('\n'.join(ops) + '\n').encode('latin-1')
        return ("<< /Length %d >>" % len(data), data)


class _Surface:
    """A drawing canvas mapped onto the current PDF page."""

    def __init__(self, doc, x0, y0, w, h):
        self.d = doc
        self.x0, self.y0, self.w, self.h = x0, y0, w, h

    def _t(self, x, y):
        return self.x0 + x * self.w, self.y0 + y * self.h

    def text(self, x, y, s, size=7, style='body', align='left', color=None,
             raw=False):
        """x, y in figure coordinates (0..1).  `raw=True` means points."""
        if raw:
            px, py = x, y
        else:
            px, py = self._t(x, y)
        s = ascii_text(s)
        runs = [Run(s, style, size, '')]
        total = sum(r.width for r in runs)
        if align == 'center':
            px -= total / 2.0
        elif align == 'right':
            px -= total
        if color:
            self.d._op(f"{color[0]} {color[1]} {color[2]} rg")
        self.d._op("BT")
        fid = FONTS[style][0]
        self.d._op(f"/{fid} {size:.2f} Tf 1 0 0 1 {px:.2f} {py:.2f} Tm "
                   f"({esc(s)}) Tj")
        self.d._op("ET")
        if color:
            self.d._op("0 0 0 rg")

    def text_width(self, s, size, style='body'):
        return run_width(ascii_text(s), style, size)

    def line(self, x1, y1, x2, y2, weight=0.7, color=(0, 0, 0), dash=None,
             raw=False):
        if raw:
            p1, p2 = (x1, y1), (x2, y2)
        else:
            p1, p2 = self._t(x1, y1), self._t(x2, y2)
        self.d._op(f"{color[0]} {color[1]} {color[2]} RG {weight} w")
        if dash:
            self.d._op(f"[{dash}] 0 d")
        self.d._op(f"{p1[0]:.2f} {p1[1]:.2f} m {p2[0]:.2f} {p2[1]:.2f} l S")
        if dash:
            self.d._op("[] 0 d")

    def polyline(self, pts, weight=1.1, color=(0.1, 0.2, 0.6), dash=None):
        if not pts:
            return
        self.d._op(f"{color[0]} {color[1]} {color[2]} RG {weight} w")
        if dash:
            self.d._op(f"[{dash}] 0 d")
        first = pts[0]
        if isinstance(first, tuple):
            pp = pts
        else:
            pp = [self._t(p[0], p[1]) for p in pts]
        self.d._op(" ".join(f"{p[0]:.2f} {p[1]:.2f} m" for p in pp[:1]))
        self.d._op(" ".join(f"{p[0]:.2f} {p[1]:.2f} l" for p in pp[1:]) + " S")
        if dash:
            self.d._op("[] 0 d")

    def rect(self, x, y, w, h, fill=None, stroke=(0, 0, 0), weight=0.5,
             raw=False):
        if raw:
            px, py = x, y
        else:
            px, py = self._t(x, y)
        pw = w * self.w if not raw else w
        ph = h * self.h if not raw else h
        if fill:
            self.d._op(f"{fill[0]} {fill[1]} {fill[2]} rg "
                       f"{px:.2f} {py:.2f} {pw:.2f} {ph:.2f} re f")
        self.d._op(f"{stroke[0]} {stroke[1]} {stroke[2]} RG {weight} w "
                   f"{px:.2f} {py:.2f} {pw:.2f} {ph:.2f} re S")

    def circle(self, x, y, r, fill=None, stroke=(0, 0, 0), weight=0.6):
        px, py = self._t(x, y)
        k = r * self.w
        if fill:
            self.d._op(f"{fill[0]} {fill[1]} {fill[2]} rg")
        self.d._op(f"{stroke[0]} {stroke[1]} {stroke[2]} RG {weight} w")
        c = 0.5523
        self.d._op(
            f"{px + k:.2f} {py:.2f} m "
            f"{px + k:.2f} {py + k * c:.2f} {px + k * c:.2f} {py + k:.2f} "
            f"{px:.2f} {py + k:.2f} c "
            f"{px - k * c:.2f} {py + k:.2f} {px - k:.2f} {py + k * c:.2f} "
            f"{px - k:.2f} {py:.2f} c "
            f"{px - k:.2f} {py - k * c:.2f} {px - k * c:.2f} {py - k:.2f} "
            f"{px:.2f} {py - k:.2f} c "
            f"{px + k * c:.2f} {py - k:.2f} {px + k:.2f} {py - k * c:.2f} "
            f"{px + k:.2f} {py:.2f} c")
        self.d._op('S' if not fill else 'b')

    def dot(self, x, y, r=0.006, color=(0.1, 0.2, 0.6)):
        self.circle(x, y, r, fill=color, stroke=color, weight=0.3)
