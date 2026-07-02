"""Reusable SVG builders for curriculum unit hero and diagram visuals."""

from __future__ import annotations


def esc(text: str) -> str:
    return (
        text.replace("&", "&amp;")
        .replace("<", "&lt;")
        .replace(">", "&gt;")
        .replace('"', "&quot;")
    )


def _t(x, y, text, size=14, color="#334155", anchor="start", weight="400", family="DejaVu Sans, sans-serif"):
    w = f' font-weight="{weight}"' if weight != "400" else ""
    return (
        f'<text x="{x}" y="{y}" text-anchor="{anchor}" '
        f'font-family="{family}" font-size="{size}" fill="{color}"{w}>{esc(text)}</text>'
    )


def _title_size(text: str, max_size: int = 20) -> int:
    n = len(text)
    if n <= 32:
        return max_size
    if n <= 48:
        return max(max_size - 2, 16)
    return max(max_size - 5, 14)


def _label_size(text: str, base: int = 11) -> int:
    n = len(text)
    if n <= 10:
        return base
    if n <= 16:
        return max(base - 1, 9)
    return max(base - 2, 8)


def _box_w_for_label(text: str, min_w: int = 72, max_w: int = 140) -> int:
    return int(max(min_w, min(max_w, len(text) * 6.8 + 24)))


def _label_box(x, y, w, h, text, fill="#dbeafe", stroke="#3b82f6", text_color="#1d4ed8", sw=2, rx=6):
    size = _label_size(text)
    return "\n".join([
        _rect(x, y, w, h, fill, stroke, sw, rx),
        _t(x + w / 2, y + h / 2 + size * 0.35, text, size, text_color, "middle", "600"),
    ])


def _rect(x, y, w, h, fill="#fff", stroke="#e2e8f0", sw=1.5, rx=8):
    return f'<rect x="{x}" y="{y}" width="{w}" height="{h}" rx="{rx}" fill="{fill}" stroke="{stroke}" stroke-width="{sw}"/>'


def _circle(cx, cy, r, fill="#3b82f6", stroke=None, sw=2):
    s = f' stroke="{stroke}" stroke-width="{sw}"' if stroke else ""
    return f'<circle cx="{cx}" cy="{cy}" r="{r}" fill="{fill}"{s}/>'


def _line(x1, y1, x2, y2, color="#64748b", sw=2, dash=None):
    d = f' stroke-dasharray="{dash}"' if dash else ""
    return f'<line x1="{x1}" y1="{y1}" x2="{x2}" y2="{y2}" stroke="{color}" stroke-width="{sw}"{d}/>'


def _arrow(x1, y1, x2, y2, color="#64748b", sw=2):
    return (
        f'{_line(x1, y1, x2, y2, color, sw)}'
        f'<polygon points="{x2},{y2} {x2 - 6},{y2 - 3} {x2 - 6},{y2 + 3}" fill="{color}"/>'
    )


def svg_doc(view_w, view_h, body: str, aria: str = "") -> str:
    aria_attr = f' aria-label="{esc(aria)}"' if aria else ""
    return (
        f'<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 {view_w} {view_h}" role="img"{aria_attr}>\n'
        f'{body}\n</svg>'
    )


def hero_two_panel(
    title: str,
    left_title: str,
    left_caption: str,
    left_body: str,
    right_title: str,
    right_caption: str,
    right_body: str,
    left_color: str = "#3b82f6",
    right_color: str = "#7c3aed",
) -> str:
    body = f"""  <rect width="1200" height="320" rx="16" fill="#f8fafc"/>
  {_t(600, 42, title, 28, "#1e293b", "middle", "800")}
  {_rect(40, 58, 540, 200, "#fff", left_color, 3, 14)}
  {_t(310, 88, left_title, 22, left_color, "middle", "700")}
  <g transform="translate(50, 96)">{left_body}</g>
  {_t(310, 248, left_caption, 14, "#475569", "middle", "600")}
  {_t(600, 168, "→", 36, "#94a3b8", "middle")}
  {_rect(620, 58, 540, 200, "#fff", right_color, 3, 14)}
  {_t(890, 88, right_title, 22, right_color, "middle", "700")}
  <g transform="translate(630, 96)">{right_body}</g>
  {_t(890, 248, right_caption, 14, "#475569", "middle", "600")}"""
    return svg_doc(1200, 320, body, title)


def diagram_card(title: str, body: str, subtitle: str = "", accent: str = "#3b82f6", h: int = 380) -> str:
    title_sz = _title_size(title)
    sub = f'\n  {_t(350, h - 28, subtitle, 12, "#64748b", "middle")}' if subtitle else ""
    body_h = h - 128
    inner = f"""  <rect width="700" height="{h}" rx="12" fill="#f8fafc"/>
  {_rect(24, 20, 652, 56, "#fff", accent, 2, 8)}
  {_t(350, 54, title, title_sz, accent, "middle", "700")}
  {_rect(24, 88, 652, body_h, "#fff", "#e2e8f0", 1.5, 8)}
  <g transform="translate(90, 108)">{body}</g>{sub}"""
    return svg_doc(700, h, inner, title)


def diagram_compare(title_l: str, body_l: str, title_r: str, body_r: str, caption: str = "") -> str:
    w, h = 720, 320 if not caption else 348
    pw, ph = 332, 248
    lx, rx = 20, 368
    title_bar = 44
    body_y = 20 + title_bar + 12
    sub = f'\n  {_t(w / 2, h - 18, caption, 11, "#64748b", "middle")}' if caption else ""
    inner = f"""  <rect width="{w}" height="{h}" rx="12" fill="#f8fafc"/>
  {_rect(lx, 20, pw, ph, "#fff", "#e2e8f0", 1.5, 10)}
  {_rect(lx, 20, pw, title_bar, "#fff7ed", "#f97316", 1.5, 10)}
  {_t(lx + pw / 2, 48, title_l, _title_size(title_l, 15), "#c2410c", "middle", "700")}
  <g transform="translate({lx + 24}, {body_y})">{body_l}</g>
  {_rect(rx, 20, pw, ph, "#fff", "#e2e8f0", 1.5, 10)}
  {_rect(rx, 20, pw, title_bar, "#f0fdf4", "#22c55e", 1.5, 10)}
  {_t(rx + pw / 2, 48, title_r, _title_size(title_r, 15), "#15803d", "middle", "700")}
  <g transform="translate({rx + 24}, {body_y})">{body_r}</g>{sub}"""
    return svg_doc(w, h, inner, f"{title_l} vs {title_r}")


def flow_horizontal(steps: list[tuple[str, str]], y: int = 50, max_width: int = 560) -> str:
    """steps: [(label, color), ...]"""
    if not steps:
        return ""
    gap = 28
    box_ws = [_box_w_for_label(label) for label, _ in steps]
    total = sum(box_ws) + gap * (len(steps) - 1)
    if total > max_width:
        scale = max_width / total
        box_ws = [max(64, int(w * scale)) for w in box_ws]
        gap = max(18, int(gap * scale))
    parts: list[str] = []
    x = 0
    box_h = 48
    for i, (label, color) in enumerate(steps):
        bw = box_ws[i]
        parts.append(_rect(x, y, bw, box_h, color + "22", color, 2, 8))
        parts.append(_t(x + bw / 2, y + box_h / 2 + _label_size(label) * 0.35, label, _label_size(label), color, "middle", "600"))
        if i < len(steps) - 1:
            parts.append(_arrow(x + bw, y + box_h / 2, x + bw + gap - 8, y + box_h / 2, "#64748b", 1.5))
        x += bw + gap
    return "\n".join(parts)


def mini_tree(root: str, left: str, right: str, ll: str = "", lr: str = "") -> str:
    bw = 108
    bh = 32
    cx = 250
    parts = [
        *_label_box(cx - bw / 2, 0, bw, bh, root, "#dbeafe", "#3b82f6", "#1d4ed8").split("\n"),
        _line(cx, bh, 110, bh + 34, "#94a3b8", 1.5),
        _line(cx, bh, 390, bh + 34, "#94a3b8", 1.5),
        *_label_box(56, bh + 34, bw, bh, left, "#dcfce7", "#22c55e", "#15803d").split("\n"),
        *_label_box(334, bh + 34, bw, bh, right, "#fef3c7", "#f59e0b", "#b45309").split("\n"),
    ]
    if ll:
        parts += [
            _line(390, bh + 34 + bh, 330, bh + 34 + bh + 34, "#94a3b8", 1.5),
            _line(390, bh + 34 + bh, 450, bh + 34 + bh + 34, "#94a3b8", 1.5),
            *_label_box(276, bh + 68 + bh, bw, bh, ll, "#ede9fe", "#8b5cf6", "#6d28d9").split("\n"),
            *_label_box(396, bh + 68 + bh, bw, bh, lr, "#fce7f3", "#ec4899", "#be185d").split("\n"),
        ]
    return "\n".join(parts)


def mini_animal_tree() -> str:
    """Feathers? → Yes: Bird | No: Walks? → Yes: Dog / No: Cat"""
    return mini_tree("Feathers?", "Bird", "Walks?", "Dog", "Cat")


def mini_rf_vote() -> str:
    trees = [(60, 8), (230, 8), (400, 8)]
    parts = []
    votes = ["A", "A", "B"]
    for i, (tx, ty) in enumerate(trees):
        parts += [
            _line(tx + 30, ty + 44, tx + 15, ty + 62, "#22c55e", 1.5),
            _line(tx + 30, ty + 44, tx + 45, ty + 62, "#22c55e", 1.5),
            _circle(tx + 30, ty + 26, 18, "#dcfce7", "#22c55e", 2),
            _t(tx + 30, ty + 31, "T" + str(i + 1), 10, "#15803d", "middle", "700"),
            _t(tx + 30, ty + 78, f"vote {votes[i]}", 10, "#475569", "middle", "600"),
        ]
    parts += [
        _rect(150, 98, 220, 36, "#ede9fe", "#7c3aed", 2, 8),
        _t(260, 122, "Majority vote → A", 12, "#6d28d9", "middle", "700"),
    ]
    return "\n".join(parts)


def mini_parallel_trees(compact: bool = False) -> str:
    if compact:
        xs = [40, 100, 160, 220]
        bar, vote = (70, 100, 180, 28), (160, 120)
        fs = 9
    else:
        xs = [60, 180, 300, 420]
        bar, vote = (120, 110, 280, 32), (260, 132)
        fs = 10
    parts = []
    for i, x in enumerate(xs):
        parts += [
            _circle(x, 40, 14 if compact else 16, "#dbeafe", "#3b82f6", 2),
            _line(x, 54, x - 10, 76, "#3b82f6", 1.5),
            _line(x, 54, x + 10, 76, "#3b82f6", 1.5),
            _t(x, 90, f"T{i+1}", fs, "#64748b", "middle"),
        ]
    parts += [
        _rect(bar[0], bar[1], bar[2], bar[3], "#dbeafe", "#3b82f6", 2, 8),
        _t(vote[0], vote[1], "Parallel vote", 11 if compact else 13, "#1d4ed8", "middle", "700"),
    ]
    return "\n".join(parts)


def mini_sequential_boost(compact: bool = False) -> str:
    if compact:
        parts = [
            _rect(8, 28, 64, 30, "#fee2e2", "#ef4444", 2, 6),
            _t(40, 48, "err +5m", 9, "#b91c1c", "middle", "600"),
            _arrow(72, 43, 98, 43),
            _rect(98, 28, 64, 30, "#fef3c7", "#f59e0b", 2, 6),
            _t(130, 48, "fix -4m", 9, "#b45309", "middle", "600"),
            _arrow(162, 43, 188, 43),
            _rect(188, 28, 64, 30, "#dcfce7", "#22c55e", 2, 6),
            _t(220, 48, "fix -1m", 9, "#15803d", "middle", "600"),
            _rect(70, 88, 160, 26, "#ede9fe", "#7c3aed", 2, 8),
            _t(150, 106, "Sequential fix", 10, "#6d28d9", "middle", "700"),
        ]
    else:
        parts = [
            _rect(20, 30, 80, 36, "#fee2e2", "#ef4444", 2, 6),
            _t(60, 54, "err +5m", 10, "#b91c1c", "middle", "600"),
            _arrow(100, 48, 140, 48),
            _rect(140, 30, 80, 36, "#fef3c7", "#f59e0b", 2, 6),
            _t(180, 54, "fix -4m", 10, "#b45309", "middle", "600"),
            _arrow(220, 48, 260, 48),
            _rect(260, 30, 80, 36, "#dcfce7", "#22c55e", 2, 6),
            _t(300, 54, "fix -1m", 10, "#15803d", "middle", "600"),
            _rect(100, 100, 220, 32, "#ede9fe", "#7c3aed", 2, 8),
            _t(210, 122, "Sequential correction", 12, "#6d28d9", "middle", "700"),
        ]
    return "\n".join(parts)


def mini_kmeans(compact: bool = False) -> str:
    if compact:
        pts = [(52, 78), (68, 68), (84, 86), (188, 62), (204, 74), (196, 52)]
        ca, cb = (68, 78), (200, 66)
        label_y = 108
    else:
        pts = [(60, 100), (80, 90), (100, 110), (220, 70), (240, 82), (230, 58)]
        ca, cb = (80, 100), (230, 75)
        label_y = 130
    parts = []
    for i, (x, y) in enumerate(pts):
        c = "#f97316" if i < 3 else "#8b5cf6"
        parts.append(_circle(x, y, 10, c))
    parts += [
        _circle(ca[0], ca[1], 14, "none", "#f97316", 2),
        _circle(cb[0], cb[1], 14, "none", "#8b5cf6", 2),
        _t(ca[0], label_y, "Centroid A", 10, "#c2410c", "middle"),
        _t(cb[0], label_y - 8, "Centroid B", 10, "#6d28d9", "middle"),
    ]
    return "\n".join(parts)


def mini_dbscan(compact: bool = False) -> str:
    if compact:
        parts = [
            _circle(52, 72, 8, "#3b82f6"), _circle(66, 82, 8, "#3b82f6"), _circle(58, 90, 8, "#3b82f6"),
            _circle(198, 68, 8, "#8b5cf6"), _circle(214, 80, 8, "#8b5cf6"), _circle(206, 90, 8, "#8b5cf6"),
            _circle(128, 118, 6, "#94a3b8"), _circle(142, 124, 6, "#94a3b8"),
            _rect(38, 54, 52, 48, "none", "#3b82f6", 1.5, 16),
            _rect(182, 52, 52, 52, "none", "#8b5cf6", 1.5, 16),
            _t(135, 142, "noise", 10, "#64748b", "middle"),
        ]
    else:
        parts = [
            _circle(80, 70, 8, "#3b82f6"), _circle(95, 80, 8, "#3b82f6"), _circle(70, 85, 8, "#3b82f6"),
            _circle(220, 60, 8, "#8b5cf6"), _circle(240, 75, 8, "#8b5cf6"), _circle(230, 90, 8, "#8b5cf6"),
            _circle(155, 115, 6, "#94a3b8"), _circle(172, 120, 6, "#94a3b8"),
            _rect(50, 40, 80, 60, "none", "#3b82f6", 1.5, 20),
            _rect(200, 40, 70, 65, "none", "#8b5cf6", 1.5, 20),
            _t(164, 138, "noise", 10, "#64748b", "middle"),
        ]
    return "\n".join(parts)


def mini_pca() -> str:
    parts = [
        _circle(80, 60, 6, "#3b82f6", None, 0), _circle(100, 80, 6, "#3b82f6", None, 0),
        _circle(90, 100, 6, "#3b82f6", None, 0), _circle(120, 70, 6, "#3b82f6", None, 0),
        _circle(110, 90, 6, "#3b82f6", None, 0), _circle(70, 90, 6, "#3b82f6", None, 0),
        _line(60, 110, 140, 50, "#f97316", 2.5),
        _arrow(160, 80, 220, 80),
        _rect(230, 50, 200, 80, "#fff", "#e2e8f0", 1.5, 6),
        _circle(260, 90, 5, "#3b82f6", None, 0), _circle(290, 75, 5, "#3b82f6", None, 0),
        _circle(320, 85, 5, "#3b82f6", None, 0), _circle(350, 70, 5, "#3b82f6", None, 0),
        _line(250, 100, 400, 100, "#94a3b8", 1.5),
        _t(325, 115, "2D projection", 10, "#64748b", "middle"),
    ]
    return "\n".join(parts)


def mini_crossval() -> str:
    colors = ["#ef4444", "#f59e0b", "#22c55e", "#3b82f6", "#8b5cf6"]
    parts = []
    for fold in range(5):
        y = fold * 22
        for i in range(5):
            c = colors[i] if i == fold else "#e2e8f0"
            parts.append(_rect(40 + i * 52, y, 48, 18, c, "#cbd5e1", 1, 4))
        parts.append(_t(310, y + 14, f"Fold {fold+1} test", 10, "#475569", "start"))
    return "\n".join(parts)


def mini_grid_search() -> str:
    vals = [0.6, 0.72, 0.81, 0.65, 0.88, 0.79, 0.70, 0.83, 0.91]
    parts = [_t(0, 12, "max_depth × lr", 11, "#64748b", "start", "600")]
    for i, v in enumerate(vals):
        row, col = divmod(i, 3)
        intensity = int(200 - v * 120)
        fill = f"rgb({intensity},{intensity + 30},255)"
        parts.append(_rect(10 + col * 70, 24 + row * 36, 64, 30, fill, "#cbd5e1", 1, 4))
        parts.append(_t(42 + col * 70, 44 + row * 36, f"{v:.2f}", 10, "#1e293b", "middle", "600"))
    parts.append(_rect(80, 140, 120, 28, "#dcfce7", "#22c55e", 2, 6))
    parts.append(_t(140, 158, "Best: 0.91", 11, "#15803d", "middle", "700"))
    return "\n".join(parts)


def mini_pipeline() -> str:
    return flow_horizontal([
        ("Load", "#3b82f6"), ("Clean", "#8b5cf6"), ("Split", "#f59e0b"),
        ("Train", "#22c55e"), ("Eval", "#ec4899"),
    ], y=50)


def mini_nn_layers() -> str:
    """3-input, 2-hidden, 1-output MLP; output node vertically centered with hidden layer."""
    lx_in, lx_hid, lx_out = 60, 230, 400
    input_ys = [55, 100, 145]
    hidden_ys = [75, 125]
    output_y = 100
    r, sw = 18, 1.25
    parts: list[str] = []

    for i, y in enumerate(input_ys):
        parts += [_circle(lx_in, y, r, "#dbeafe", "#3b82f6", 2), _t(lx_in, y + 5, f"x{i + 1}", 11, "#1d4ed8", "middle", "600")]
    for i, y in enumerate(hidden_ys):
        parts += [_circle(lx_hid, y, r, "#dbeafe", "#3b82f6", 2), _t(lx_hid, y + 5, f"h{i + 1}", 11, "#1d4ed8", "middle", "600")]
    parts += [_circle(lx_out, output_y, r, "#dbeafe", "#3b82f6", 2), _t(lx_out, output_y + 5, "y", 11, "#1d4ed8", "middle", "600")]

    for iy in input_ys:
        for hy in hidden_ys:
            parts.append(_line(lx_in + r, iy, lx_hid - r, hy, "#94a3b8", sw))
    for hy in hidden_ys:
        parts.append(_line(lx_hid + r, hy, lx_out - r, output_y, "#94a3b8", sw))

  # Layer labels with subtle column guides
    parts += [
        _line(lx_in, 168, lx_in, 12, "#e2e8f0", 1, "4 4"),
        _line(lx_hid, 168, lx_hid, 12, "#e2e8f0", 1, "4 4"),
        _line(lx_out, 168, lx_out, 12, "#e2e8f0", 1, "4 4"),
        _t(lx_in, 182, "Input", 11, "#64748b", "middle", "600"),
        _t(lx_hid, 182, "Hidden", 11, "#64748b", "middle", "600"),
        _t(lx_out, 182, "Output", 11, "#64748b", "middle", "600"),
    ]
    return "\n".join(parts)


def mini_training_loop() -> str:
    steps = [("Forward", "#3b82f6"), ("Loss", "#ef4444"), ("Backward", "#f59e0b"), ("Update", "#22c55e")]
    x, y, bw, bh, gap = 16, 32, 96, 46, 24
    parts: list[str] = []
    tops: list[tuple[float, float]] = []

    for i, (label, color) in enumerate(steps):
        cx = x + bw / 2
        parts += [
            _rect(x, y, bw, bh, color + "22", color, 2, 8),
            _t(cx, y + bh / 2 + 4, label, _label_size(label), color, "middle", "600"),
        ]
        tops.append((cx, y))
        if i < len(steps) - 1:
            parts.append(_arrow(x + bw, y + bh / 2, x + bw + gap - 8, y + bh / 2, "#64748b", 1.5))
        x += bw + gap

    first_cx, last_cx = tops[0][0], tops[-1][0]
    bottom = y + bh
    loop_y = bottom + 42
    parts += [
        f'<path d="M {last_cx} {bottom} L {last_cx} {loop_y} L {first_cx} {loop_y} L {first_cx} {bottom}" '
        f'fill="none" stroke="#64748b" stroke-width="1.5"/>',
        f'<polygon points="{first_cx},{bottom} {first_cx - 5},{bottom + 8} {first_cx + 5},{bottom + 8}" fill="#64748b"/>',
        _t((first_cx + last_cx) / 2, loop_y + 18, "repeat", 11, "#64748b", "middle", "600"),
    ]
    return "\n".join(parts)


def mini_tensor() -> str:
    parts = [
        _rect(20, 20, 120, 80, "#dbeafe", "#3b82f6", 2, 6),
        _t(80, 50, "Tensor", 14, "#1d4ed8", "middle", "700"),
        _t(80, 72, "(batch, feat)", 11, "#475569", "middle"),
        _arrow(150, 60, 210, 60),
        _rect(210, 20, 120, 80, "#ede9fe", "#7c3aed", 2, 6),
        _t(270, 50, "matmul", 14, "#6d28d9", "middle", "700"),
        _t(270, 72, "→ logits", 11, "#475569", "middle"),
    ]
    return "\n".join(parts)


def mini_autograd() -> str:
    parts = [
        _rect(30, 40, 90, 40, "#dcfce7", "#22c55e", 2, 6),
        _t(75, 66, "loss", 12, "#15803d", "middle", "700"),
        _t(75, 30, ".backward()", 10, "#64748b", "middle"),
        _arrow(120, 60, 180, 60),
        _rect(180, 40, 110, 40, "#fef3c7", "#f59e0b", 2, 6),
        _t(235, 66, "gradients", 12, "#b45309", "middle", "700"),
        _arrow(290, 60, 350, 60),
        _rect(350, 40, 110, 40, "#dbeafe", "#3b82f6", 2, 6),
        _t(405, 66, "optimizer", 12, "#1d4ed8", "middle", "700"),
    ]
    return "\n".join(parts)


def mini_loss_curves(compact: bool = False) -> str:
    w = 260 if compact else 380
    parts = [
        _line(20, 110, 20, 20, "#94a3b8", 1.5),
        _line(20, 110, w, 110, "#94a3b8", 1.5),
        _t(12, 18, "loss", 9, "#64748b", "middle"),
        '  <path d="M30,100 C60,92 90,65 130,50 S200,35 240,30" fill="none" stroke="#ef4444" stroke-width="2.5"/>',
        '  <path d="M30,105 C70,98 110,88 150,82 S210,76 240,74" fill="none" stroke="#3b82f6" stroke-width="2.5"/>',
        _t(170, 42, "MSE", 9, "#ef4444", "start", "600"),
        _t(170, 56, "CE", 9, "#3b82f6", "start", "600"),
    ]
    return "\n".join(parts)


def mini_optimizers(compact: bool = False) -> str:
    w = 260 if compact else 360
    parts = [
        _line(20, 90, 20, 20, "#94a3b8", 1.5),
        _line(20, 90, w, 90, "#94a3b8", 1.5),
        '  <path d="M35,82 L65,68 L95,72 L125,48 L155,52 L185,38 L215,42 L240,28" fill="none" stroke="#3b82f6" stroke-width="2" stroke-dasharray="6 3"/>',
        '  <path d="M35,82 C80,70 125,52 170,38 S220,28 240,26" fill="none" stroke="#22c55e" stroke-width="2.5"/>',
        _t(150, 16, "Adam", 9, "#22c55e", "start", "600"),
        _t(150, 78, "SGD", 9, "#3b82f6", "start", "600"),
    ]
    return "\n".join(parts)


def mini_overfit(compact: bool = False) -> str:
    w = 220 if compact else 280
    parts = [
        _line(12, 100, 12, 16, "#94a3b8", 1.5),
        _line(12, 100, w, 100, "#94a3b8", 1.5),
        '  <path d="M22,92 C45,88 68,38 88,52 S130,78 165,42 S195,26 205,30" fill="none" stroke="#ef4444" stroke-width="2.5"/>',
        _circle(45, 72, 3, "#3b82f6", None, 0),
        _circle(88, 58, 3, "#3b82f6", None, 0),
        _circle(130, 68, 3, "#3b82f6", None, 0),
        _circle(175, 46, 3, "#3b82f6", None, 0),
        _t(24, 112, "Memorizes noise", 9, "#b91c1c", "start"),
    ]
    return "\n".join(parts)


def mini_dropout(compact: bool = False) -> str:
    if compact:
        nodes = [(36, 32), (36, 64), (36, 96), (120, 48), (120, 80), (200, 64)]
    else:
        nodes = [(60, 40), (60, 80), (60, 120), (180, 60), (180, 100), (300, 80)]
    active = [True, False, True, True, False, True]
    r = 11 if compact else 14
    parts = []
    for (x, y), on in zip(nodes, active):
        if on:
            parts.append(_circle(x, y, r, "#dbeafe", "#3b82f6", 2))
        else:
            parts.append(_circle(x, y, r, "#f1f5f9", "#94a3b8", 2))
            parts.append(_line(x - 8, y - 8, x + 8, y + 8, "#94a3b8", 2))
    cx = 120 if compact else 180
    parts.append(_t(cx, 118 if compact else 140, "Zero neurons", 9 if compact else 11, "#64748b", "middle"))
    return "\n".join(parts)


def mini_cnn() -> str:
    parts = [
        _rect(20, 40, 60, 60, "#e2e8f0", "#64748b", 1.5, 4),
        _t(50, 75, "Image", 10, "#475569", "middle"),
        _arrow(85, 70, 120, 70),
        _rect(120, 35, 70, 70, "#dbeafe", "#3b82f6", 2, 4),
        _t(155, 75, "Conv", 11, "#1d4ed8", "middle", "700"),
        _arrow(195, 70, 230, 70),
        _rect(230, 45, 60, 50, "#ede9fe", "#7c3aed", 2, 4),
        _t(260, 75, "Pool", 11, "#6d28d9", "middle", "700"),
        _arrow(295, 70, 330, 70),
        _rect(330, 50, 70, 40, "#dcfce7", "#22c55e", 2, 4),
        _t(365, 75, "Linear", 11, "#15803d", "middle", "700"),
    ]
    return "\n".join(parts)


def mini_transfer() -> str:
    parts = [
        _rect(20, 30, 160, 90, "#f1f5f9", "#64748b", 2, 8),
        _t(100, 55, "Backbone", 12, "#475569", "middle", "700"),
        _t(100, 78, "(frozen)", 10, "#94a3b8", "middle"),
        _t(100, 98, "ImageNet", 10, "#64748b", "middle"),
        _arrow(185, 75, 230, 75),
        _rect(230, 40, 140, 70, "#dcfce7", "#22c55e", 2, 8),
        _t(300, 68, "New head", 12, "#15803d", "middle", "700"),
        _t(300, 90, "2 classes", 10, "#64748b", "middle"),
    ]
    return "\n".join(parts)


def mini_train_val() -> str:
    parts = [
        _line(30, 110, 30, 20, "#94a3b8", 1.5),
        _line(30, 110, 380, 110, "#94a3b8", 1.5),
        '  <path d="M40,100 C100,85 160,50 220,35 S320,25 360,20" fill="none" stroke="#3b82f6" stroke-width="2.5"/>',
        '  <path d="M40,105 C100,95 160,75 220,65 S300,58 360,55" fill="none" stroke="#f59e0b" stroke-width="2.5"/>',
        _t(300, 30, "train acc", 10, "#3b82f6", "start", "600"),
        _t(300, 48, "val acc", 10, "#f59e0b", "start", "600"),
    ]
    return "\n".join(parts)


def mini_tfidf(compact: bool = False) -> str:
    if compact:
        parts = [
            _t(4, 16, "the cat sat", 9, "#64748b", "start"),
            _arrow(72, 28, 100, 28),
            _rect(100, 8, 150, 42, "#fff", "#e2e8f0", 1.5, 4),
        ]
        words = ["cat", "sat", "mat"]
        for i, w in enumerate(words):
            parts.append(_t(110, 20 + i * 12, w, 8, "#475569", "start"))
            parts.append(_rect(145 + i * 32, 14 + i * 12, 26, 8, "#dbeafe", "#3b82f6", 1, 2))
        parts.append(_t(110, 58, "Sparse TF-IDF", 8, "#1d4ed8", "start", "600"))
    else:
        parts = [
            _t(10, 20, "the cat sat", 11, "#64748b", "start"),
            _arrow(100, 40, 150, 40),
            _rect(150, 15, 200, 50, "#fff", "#e2e8f0", 1.5, 4),
        ]
        words = ["cat", "sat", "mat"]
        for i, w in enumerate(words):
            parts.append(_t(170, 30 + i * 14, w, 9, "#475569", "start"))
            parts.append(_rect(220 + i * 40, 22 + i * 14, 30, 10, "#dbeafe", "#3b82f6", 1, 2))
        parts.append(_t(170, 75, "Sparse TF-IDF vector", 10, "#1d4ed8", "start", "600"))
    return "\n".join(parts)


def mini_embedding(compact: bool = False) -> str:
    if compact:
        parts = [
            _rect(8, 22, 56, 56, "#fee2e2", "#ef4444", 2, 6),
            _t(36, 58, "one-hot", 8, "#b91c1c", "middle", "600"),
            _arrow(68, 50, 88, 50),
            _rect(88, 22, 160, 56, "#ede9fe", "#7c3aed", 2, 6),
            _circle(110, 42, 5, "#3b82f6", None, 0),
            _circle(140, 36, 5, "#8b5cf6", None, 0),
            _circle(170, 48, 5, "#ec4899", None, 0),
            _circle(200, 38, 5, "#f59e0b", None, 0),
            _circle(230, 44, 5, "#22c55e", None, 0),
            _t(168, 88, "Dense embedding", 8, "#6d28d9", "middle", "600"),
        ]
    else:
        parts = [
            _rect(20, 30, 80, 80, "#fee2e2", "#ef4444", 2, 6),
            _t(60, 75, "one-hot", 10, "#b91c1c", "middle", "600"),
            _t(60, 55, "sparse", 10, "#64748b", "middle"),
            _arrow(105, 70, 155, 70),
            _rect(155, 30, 220, 80, "#ede9fe", "#7c3aed", 2, 6),
            _circle(190, 60, 6, "#3b82f6", None, 0),
            _circle(230, 50, 6, "#8b5cf6", None, 0),
            _circle(270, 70, 6, "#ec4899", None, 0),
            _circle(310, 55, 6, "#f59e0b", None, 0),
            _circle(350, 65, 6, "#22c55e", None, 0),
            _t(265, 100, "Dense embedding space", 10, "#6d28d9", "middle", "600"),
        ]
    return "\n".join(parts)


def mini_rnn() -> str:
    parts = []
    xs = [40, 130, 220, 310]
    for i, x in enumerate(xs):
        parts += [
            _rect(x, 50, 60, 40, "#dbeafe", "#3b82f6", 2, 6),
            _t(x + 30, 76, f"h_{i}", 11, "#1d4ed8", "middle", "700"),
        ]
        if i < len(xs) - 1:
            parts.append(_arrow(x + 60, 70, x + 70, 70))
    parts.append(_t(175, 110, "h_t depends on h_{t-1}", 11, "#64748b", "middle"))
    return "\n".join(parts)


def mini_lstm() -> str:
    parts = [
        _rect(40, 30, 420, 90, "#ede9fe", "#7c3aed", 2, 8),
        _t(250, 58, "LSTM Cell", 14, "#6d28d9", "middle", "700"),
        *_label_box(70, 72, 72, 28, "Forget", "#fee2e2", "#ef4444", "#b91c1c", 1.5).split("\n"),
        *_label_box(174, 72, 72, 28, "Input", "#dcfce7", "#22c55e", "#15803d", 1.5).split("\n"),
        *_label_box(278, 72, 72, 28, "Output", "#dbeafe", "#3b82f6", "#1d4ed8", 1.5).split("\n"),
        *_label_box(382, 72, 58, 28, "State", "#fef3c7", "#f59e0b", "#b45309", 1.5).split("\n"),
        _t(250, 140, "Gates control what to forget, add, and pass on", 10, "#64748b", "middle"),
    ]
    return "\n".join(parts)


def mini_attention() -> str:
    parts = [
        _rect(20, 20, 360, 100, "#fff", "#e2e8f0", 1.5, 6),
    ]
    for i in range(4):
        for j in range(4):
            op = 0.2 + (0.8 if i == j else 0.15 + abs(i - j) * 0.05)
            fill = f"rgba(59,130,246,{op:.2f})"
            parts.append(_rect(30 + j * 85, 30 + i * 22, 75, 18, fill, "#cbd5e1", 0.5, 2))
    parts += [
        _t(200, 135, "Query × Key → attention weights", 11, "#1d4ed8", "middle", "600"),
    ]
    return "\n".join(parts)


def mini_transformer() -> str:
    return flow_horizontal([
        ("Multi-head", "#3b82f6"), ("Attention", "#8b5cf6"), ("FFN", "#22c55e"), ("Add+Norm", "#f59e0b"),
    ], y=55)


def mini_rag(compact: bool = False) -> str:
    steps = [
        ("Docs", "#3b82f6"), ("Chunk", "#8b5cf6"), ("Embed", "#f59e0b"),
        ("Retrieve", "#22c55e"), ("LLM", "#ec4899"),
    ]
    return flow_horizontal(steps, y=45 if compact else 45, max_width=260 if compact else 560)


def mini_vector_search() -> str:
    parts = [
        _circle(80, 70, 8, "#3b82f6"), _circle(120, 50, 8, "#3b82f6"), _circle(160, 80, 8, "#3b82f6"),
        _circle(250, 60, 8, "#8b5cf6"), _circle(290, 90, 8, "#8b5cf6"),
        _circle(200, 70, 12, "none", "#ef4444", 3),
        _t(200, 74, "Q", 10, "#ef4444", "middle", "700"),
        _line(200, 70, 120, 50, "#ef4444", 1, "4 3"),
        _line(200, 70, 160, 80, "#ef4444", 1, "4 3"),
        _t(200, 110, "Cosine similarity → top-k", 11, "#64748b", "middle"),
    ]
    return "\n".join(parts)


def mini_langgraph() -> str:
    """Ticket routing graph: classify → billing / technical / escalate."""
    bw = 100
    bh = 32
    cx = 250
    parts = [
        *_label_box(cx - bw / 2, 0, bw, bh, "Classify", "#dbeafe", "#3b82f6", "#1d4ed8").split("\n"),
        _line(cx, bh, 80, bh + 36, "#94a3b8", 1.5),
        _line(cx, bh, cx, bh + 36, "#94a3b8", 1.5),
        _line(cx, bh, 420, bh + 36, "#94a3b8", 1.5),
        *_label_box(30, bh + 36, bw, bh, "Billing", "#dcfce7", "#22c55e", "#15803d").split("\n"),
        *_label_box(cx - bw / 2, bh + 36, bw, bh, "Technical", "#fef3c7", "#f59e0b", "#b45309").split("\n"),
        *_label_box(370, bh + 36, bw, bh, "Escalate", "#fee2e2", "#ef4444", "#b91c1c").split("\n"),
        _t(cx, bh + 88, "Stateful graph workflow", 10, "#64748b", "middle"),
    ]
    return "\n".join(parts)


def mini_state_graph() -> str:
    """LangGraph core concepts: shared State + nodes joined by edges, with a conditional branch."""
    parts = [
        # shared state box spanning the top
        _rect(90, 0, 320, 34, "#fef3c7", "#f59e0b", 2, 8),
        _t(250, 22, "State (shared TypedDict)", 12, "#b45309", "middle", "700"),
        # node A
        *_label_box(40, 74, 110, 34, "Node A", "#dbeafe", "#3b82f6", "#1d4ed8").split("\n"),
        # conditional edge split to B / C
        _line(150, 91, 210, 91, "#64748b", 1.5),
        _t(180, 82, "edge", 9, "#64748b", "middle"),
        *_label_box(210, 74, 110, 34, "Condition?", "#ede9fe", "#7c3aed", "#6d28d9").split("\n"),
        _line(320, 91, 372, 62, "#64748b", 1.5),
        '<polygon points="372,62 362,63 366,71" fill="#64748b"/>',
        _line(320, 91, 372, 120, "#64748b", 1.5),
        '<polygon points="372,120 362,119 366,111" fill="#64748b"/>',
        _t(345, 62, "yes", 9, "#15803d", "middle"),
        _t(345, 122, "no", 9, "#b91c1c", "middle"),
        *_label_box(372, 42, 100, 32, "Node B", "#dcfce7", "#22c55e", "#15803d").split("\n"),
        *_label_box(372, 106, 100, 32, "Node C", "#fee2e2", "#ef4444", "#b91c1c").split("\n"),
        # nodes read/write the state (dashed vertical links)
        _line(95, 74, 120, 34, "#f59e0b", 1, "4 3"),
        _line(265, 74, 255, 34, "#f59e0b", 1, "4 3"),
        _line(410, 42, 385, 34, "#f59e0b", 1, "4 3"),
    ]
    return "\n".join(parts)


def mini_react_loop() -> str:
    steps = [("Thought", "#3b82f6"), ("Action", "#f59e0b"), ("Observation", "#22c55e")]
    x, y, bw, bh, gap = 16, 32, 96, 46, 24
    parts: list[str] = []
    tops: list[float] = []
    for i, (label, color) in enumerate(steps):
        cx = x + bw / 2
        parts += [
            _rect(x, y, bw, bh, color + "22", color, 2, 8),
            _t(cx, y + bh / 2 + 4, label, _label_size(label), color, "middle", "600"),
        ]
        tops.append(cx)
        if i < len(steps) - 1:
            parts.append(_arrow(x + bw, y + bh / 2, x + bw + gap - 8, y + bh / 2, "#64748b", 1.5))
        x += bw + gap
    first_cx, last_cx = tops[0], tops[-1]
    bottom = y + bh
    loop_y = bottom + 42
    parts += [
        f'<path d="M {last_cx} {bottom} L {last_cx} {loop_y} L {first_cx} {loop_y} L {first_cx} {bottom}" '
        f'fill="none" stroke="#64748b" stroke-width="1.5"/>',
        f'<polygon points="{first_cx},{bottom} {first_cx - 5},{bottom + 8} {first_cx + 5},{bottom + 8}" fill="#64748b"/>',
        _t((first_cx + last_cx) / 2, loop_y + 18, "repeat until done", 10, "#64748b", "middle", "600"),
    ]
    return "\n".join(parts)


def mini_mcp() -> str:
    """3-layer MCP architecture: Host contains Client, which talks to Server."""
    parts = [
        # Host box wrapping the client
        _rect(14, 22, 210, 110, "#f1f5f9", "#64748b", 2, 10),
        _t(119, 44, "Host", 12, "#475569", "middle", "700"),
        _t(119, 60, "(Claude / IDE app)", 9, "#94a3b8", "middle"),
        # Client inside host
        _rect(38, 70, 162, 46, "#dbeafe", "#3b82f6", 2, 8),
        _t(119, 91, "MCP Client", 12, "#1d4ed8", "middle", "700"),
        _t(119, 107, "JSON-RPC", 9, "#64748b", "middle"),
        # connection
        _line(224, 93, 300, 93, "#64748b", 2),
        '<polygon points="300,93 292,89 292,97" fill="#64748b"/>',
        _t(262, 84, "stdio/HTTP", 9, "#64748b", "middle"),
        # Server
        _rect(300, 52, 150, 80, "#ede9fe", "#7c3aed", 2, 8),
        _t(375, 80, "MCP Server", 12, "#6d28d9", "middle", "700"),
        _t(375, 100, "Tools / Resources", 10, "#64748b", "middle"),
        _t(375, 116, "Prompts", 10, "#64748b", "middle"),
    ]
    return "\n".join(parts)


def mini_agent_evolution() -> str:
    return flow_horizontal([
        ("Completion", "#3b82f6"), ("RAG", "#8b5cf6"), ("Agent", "#22c55e"),
    ], y=55)


def mini_api_flow() -> str:
    parts = [
        _rect(20, 45, 100, 50, "#dbeafe", "#3b82f6", 2, 8),
        _t(70, 75, "Your App", 11, "#1d4ed8", "middle", "700"),
        _arrow(120, 70, 180, 70),
        _rect(180, 35, 130, 70, "#fef3c7", "#f59e0b", 2, 8),
        _t(245, 62, "POST /chat", 11, "#b45309", "middle", "700"),
        _t(245, 82, "completions", 10, "#64748b", "middle"),
        _arrow(310, 70, 370, 70),
        _rect(370, 45, 100, 50, "#dcfce7", "#22c55e", 2, 8),
        _t(420, 75, "JSON", 12, "#15803d", "middle", "700"),
    ]
    return "\n".join(parts)


def mini_chat_history() -> str:
    parts = [
        _rect(40, 20, 360, 110, "#fff", "#e2e8f0", 1.5, 8),
        _rect(55, 35, 200, 28, "#dbeafe", "#3b82f6", 1.5, 6),
        _t(65, 54, "User: Hello", 10, "#1d4ed8", "start"),
        _rect(180, 70, 200, 28, "#ede9fe", "#7c3aed", 1.5, 6),
        _t(190, 89, "Bot: Hi there!", 10, "#6d28d9", "start"),
        _rect(55, 105, 330, 22, "#f8fafc", "#cbd5e1", 1, 4),
        _t(65, 120, "Type a message...", 10, "#94a3b8", "start"),
    ]
    return "\n".join(parts)


def mini_multi_agent() -> str:
    bw = 96
    bh = 36
    cx = 220
    parts = [
        *_label_box(cx - bw / 2, 4, bw + 24, bh, "Triage", "#dbeafe", "#3b82f6", "#1d4ed8").split("\n"),
        _line(180, 40, 70, 78, "#94a3b8", 1.5),
        _line(cx, 40, cx, 78, "#94a3b8", 1.5),
        _line(260, 40, 370, 78, "#94a3b8", 1.5),
        *_label_box(20, 78, bw, bh, "Billing", "#dcfce7", "#22c55e", "#15803d").split("\n"),
        *_label_box(cx - bw / 2, 78, bw, bh, "Tech", "#fef3c7", "#f59e0b", "#b45309").split("\n"),
        *_label_box(344, 78, bw, bh, "Sales", "#ede9fe", "#7c3aed", "#6d28d9").split("\n"),
    ]
    return "\n".join(parts)


def mini_timeseries() -> str:
    parts = [
        _line(30, 110, 30, 30, "#94a3b8", 1.5),
        _line(30, 110, 380, 110, "#94a3b8", 1.5),
        '  <path d="M40,90 C80,85 120,70 160,75 S240,55 280,50 S340,45 360,40" fill="none" stroke="#3b82f6" stroke-width="2.5"/>',
        '  <path d="M40,90 C80,85 120,70 160,75 S240,55 280,50 S340,45 360,40 L360,110 L40,110 Z" fill="rgba(59,130,246,0.1)"/>',
        _t(200, 125, "Historical demand", 10, "#64748b", "middle"),
    ]
    return "\n".join(parts)


def mini_pricing() -> str:
    parts = [
        _line(40, 110, 40, 30, "#94a3b8", 1.5),
        _line(40, 110, 340, 110, "#94a3b8", 1.5),
        '  <path d="M50,100 C120,95 180,60 240,55 S300,70 330,85" fill="none" stroke="#22c55e" stroke-width="2.5"/>',
        _circle(240, 55, 8, "none", "#ef4444", 3),
        _t(240, 42, "optimal", 10, "#ef4444", "middle", "600"),
        _t(200, 125, "Price vs revenue", 10, "#64748b", "middle"),
    ]
    return "\n".join(parts)


def mini_fusion() -> str:
    parts = [
        _rect(20, 40, 90, 50, "#dbeafe", "#3b82f6", 2, 6),
        _t(65, 70, "Text", 11, "#1d4ed8", "middle", "700"),
        _rect(20, 100, 90, 50, "#fef3c7", "#f59e0b", 2, 6),
        _t(65, 130, "Image", 11, "#b45309", "middle", "700"),
        _arrow(115, 95, 180, 95),
        _rect(180, 60, 120, 70, "#ede9fe", "#7c3aed", 2, 8),
        _t(240, 90, "Late fusion", 12, "#6d28d9", "middle", "700"),
        _t(240, 110, "score", 10, "#64748b", "middle"),
        _arrow(300, 95, 360, 95),
        _rect(360, 75, 80, 40, "#fee2e2", "#ef4444", 2, 6),
        _t(400, 100, "Fraud?", 11, "#b91c1c", "middle", "700"),
    ]
    return "\n".join(parts)


def mini_guardrails() -> str:
    parts = [
        _rect(20, 50, 90, 40, "#dbeafe", "#3b82f6", 2, 6),
        _t(65, 75, "Input", 11, "#1d4ed8", "middle", "700"),
        _arrow(110, 70, 160, 70),
        _rect(160, 45, 100, 50, "#fee2e2", "#ef4444", 2, 6),
        _t(210, 75, "Guardrail", 11, "#b91c1c", "middle", "700"),
        _arrow(260, 70, 310, 70),
        _rect(310, 50, 90, 40, "#dcfce7", "#22c55e", 2, 6),
        _t(355, 75, "Safe out", 11, "#15803d", "middle", "700"),
    ]
    return "\n".join(parts)


def mini_eval_harness() -> str:
    parts = [
        _rect(30, 30, 100, 36, "#dbeafe", "#3b82f6", 2, 6),
        _t(80, 54, "Test cases", 11, "#1d4ed8", "middle", "700"),
        _arrow(130, 48, 180, 48),
        _rect(180, 30, 120, 36, "#ede9fe", "#7c3aed", 2, 6),
        _t(240, 54, "LLM judge", 11, "#6d28d9", "middle", "700"),
        _arrow(300, 48, 350, 48),
        _rect(350, 30, 100, 36, "#dcfce7", "#22c55e", 2, 6),
        _t(400, 54, "Scores", 11, "#15803d", "middle", "700"),
        _t(240, 90, "Regression tracking", 11, "#64748b", "middle"),
    ]
    return "\n".join(parts)


def mini_doc_extract() -> str:
    parts = [
        _rect(20, 35, 80, 90, "#fef3c7", "#f59e0b", 2, 6),
        _t(60, 60, "PDF", 12, "#b45309", "middle", "700"),
        _t(60, 85, "Doc", 10, "#64748b", "middle"),
        _arrow(105, 80, 160, 80),
        _rect(160, 40, 130, 80, "#dbeafe", "#3b82f6", 2, 8),
        _t(225, 65, "Agent", 12, "#1d4ed8", "middle", "700"),
        _t(225, 85, "extract", 10, "#64748b", "middle"),
        _arrow(290, 80, 340, 80),
        _rect(340, 45, 100, 70, "#dcfce7", "#22c55e", 2, 8),
        _t(390, 72, "{JSON}", 12, "#15803d", "middle", "700"),
        _t(390, 92, "schema", 10, "#64748b", "middle"),
    ]
    return "\n".join(parts)


def mini_code_agent() -> str:
    parts = [
        _rect(30, 40, 110, 50, "#dbeafe", "#3b82f6", 2, 8),
        _t(85, 60, "LLM writes", 10, "#1d4ed8", "middle", "700"),
        _t(85, 78, "Python code", 10, "#64748b", "middle"),
        _arrow(140, 65, 190, 65),
        _rect(190, 40, 110, 50, "#fef3c7", "#f59e0b", 2, 8),
        _t(245, 60, "Sandbox", 10, "#b45309", "middle", "700"),
        _t(245, 78, "execute", 10, "#64748b", "middle"),
        _arrow(300, 65, 350, 65),
        _rect(350, 45, 90, 40, "#dcfce7", "#22c55e", 2, 8),
        _t(395, 70, "Result", 11, "#15803d", "middle", "700"),
    ]
    return "\n".join(parts)


def mini_coding_agent() -> str:
    parts = [
        _rect(20, 35, 90, 40, "#dbeafe", "#3b82f6", 2, 6),
        _t(65, 60, "Read repo", 10, "#1d4ed8", "middle", "700"),
        _arrow(110, 55, 155, 55),
        _rect(155, 35, 90, 40, "#fef3c7", "#f59e0b", 2, 6),
        _t(200, 60, "Edit code", 10, "#b45309", "middle", "700"),
        _arrow(245, 55, 290, 55),
        _rect(290, 35, 90, 40, "#dcfce7", "#22c55e", 2, 6),
        _t(335, 60, "Run tests", 10, "#15803d", "middle", "700"),
        _t(200, 95, "Small iterations", 11, "#64748b", "middle"),
    ]
    return "\n".join(parts)

