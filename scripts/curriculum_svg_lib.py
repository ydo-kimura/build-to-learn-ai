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


def diagram_card(title: str, body: str, subtitle: str = "", accent: str = "#3b82f6", h: int = 320) -> str:
    sub = f'\n  {_t(350, h - 24, subtitle, 13, "#64748b", "middle")}' if subtitle else ""
    body_h = h - 108
    inner = f"""  <rect width="700" height="{h}" rx="12" fill="#f8fafc"/>
  {_rect(24, 20, 652, 52, "#fff", accent, 2, 8)}
  {_t(350, 52, title, 20, accent, "middle", "700")}
  {_rect(24, 84, 652, body_h, "#fff", "#e2e8f0", 1.5, 8)}
  <g transform="translate(40, 100)">{body}</g>{sub}"""
    return svg_doc(700, h, inner, title)


def diagram_compare(title_l: str, body_l: str, title_r: str, body_r: str, caption: str = "") -> str:
    h = 300
    sub = f'\n  {_t(350, h - 16, caption, 13, "#64748b", "middle")}' if caption else ""
    inner = f"""  <rect width="720" height="{h}" rx="12" fill="#f8fafc"/>
  {_t(130, 28, title_l, 15, "#dc2626", "middle", "700")}
  {_t(540, 28, title_r, 15, "#059669", "middle", "700")}
  {_rect(20, 40, 320, 220, "#fff", "#e2e8f0", 1.5, 8)}
  <g transform="translate(30, 50)">{body_l}</g>
  {_rect(380, 40, 320, 220, "#fff", "#e2e8f0", 1.5, 8)}
  <g transform="translate(390, 50)">{body_r}</g>{sub}"""
    return svg_doc(720, h, inner, f"{title_l} vs {title_r}")


def flow_horizontal(steps: list[tuple[str, str]], y: int = 40) -> str:
    """steps: [(label, color), ...]"""
    parts: list[str] = []
    x = 0
    box_w = min(110, max(70, 520 // max(len(steps), 1) - 20))
    gap = 36
    for i, (label, color) in enumerate(steps):
        parts.append(_rect(x, y, box_w, 44, color + "22", color, 2, 8))
        parts.append(_t(x + box_w / 2, y + 28, label, 11, color, "middle", "600"))
        if i < len(steps) - 1:
            parts.append(_arrow(x + box_w, y + 22, x + box_w + gap - 8, y + 22, "#64748b", 1.5))
        x += box_w + gap
    return "\n".join(parts)


def mini_tree(root: str, left: str, right: str, ll: str = "", lr: str = "") -> str:
    parts = [
        _rect(190, 0, 100, 28, "#dbeafe", "#3b82f6", 2, 6),
        _t(240, 20, root, 11, "#1d4ed8", "middle", "600"),
        _line(240, 28, 120, 58, "#94a3b8", 1.5),
        _line(240, 28, 360, 58, "#94a3b8", 1.5),
        _rect(70, 58, 100, 28, "#dcfce7", "#22c55e", 2, 6),
        _t(120, 78, left, 11, "#15803d", "middle", "600"),
        _rect(310, 58, 100, 28, "#fef3c7", "#f59e0b", 2, 6),
        _t(360, 78, right, 11, "#b45309", "middle", "600"),
    ]
    if ll:
        parts += [
            _line(360, 86, 320, 116, "#94a3b8", 1.5),
            _line(360, 86, 400, 116, "#94a3b8", 1.5),
            _rect(270, 116, 100, 28, "#ede9fe", "#8b5cf6", 2, 6),
            _t(320, 136, ll, 11, "#6d28d9", "middle", "600"),
            _rect(350, 116, 100, 28, "#fce7f3", "#ec4899", 2, 6),
            _t(400, 136, lr, 11, "#be185d", "middle", "600"),
        ]
    return "\n".join(parts)


def mini_animal_tree() -> str:
    """Feathers? → Yes: Bird | No: Walks? → Yes: Dog / No: Cat"""
    return "\n".join([
        _rect(190, 0, 100, 28, "#dbeafe", "#3b82f6", 2, 6),
        _t(240, 20, "Feathers?", 11, "#1d4ed8", "middle", "600"),
        _line(240, 28, 120, 58, "#94a3b8", 1.5),
        _line(240, 28, 360, 58, "#94a3b8", 1.5),
        _rect(70, 58, 100, 28, "#dcfce7", "#22c55e", 2, 6),
        _t(120, 78, "Bird", 11, "#15803d", "middle", "600"),
        _rect(310, 58, 100, 28, "#fef3c7", "#f59e0b", 2, 6),
        _t(360, 78, "Walks?", 11, "#b45309", "middle", "600"),
        _line(360, 86, 320, 116, "#94a3b8", 1.5),
        _line(360, 86, 400, 116, "#94a3b8", 1.5),
        _rect(270, 116, 100, 28, "#ede9fe", "#8b5cf6", 2, 6),
        _t(320, 136, "Dog", 11, "#6d28d9", "middle", "600"),
        _rect(350, 116, 100, 28, "#fce7f3", "#ec4899", 2, 6),
        _t(400, 136, "Cat", 11, "#be185d", "middle", "600"),
    ])


def mini_rf_vote() -> str:
    trees = [(40, 10), (200, 10), (360, 10)]
    parts = []
    votes = ["A", "A", "B"]
    for i, (tx, ty) in enumerate(trees):
        parts += [
            _line(tx + 30, ty + 40, tx + 15, ty + 55, "#22c55e", 1.5),
            _line(tx + 30, ty + 40, tx + 45, ty + 55, "#22c55e", 1.5),
            _circle(tx + 30, ty + 25, 16, "#dcfce7", "#22c55e", 2),
            _t(tx + 30, ty + 30, "?", 12, "#15803d", "middle", "700"),
            _t(tx + 30, ty + 68, f"→ {votes[i]}", 11, "#475569", "middle", "600"),
        ]
    parts += [
        _rect(130, 88, 180, 32, "#ede9fe", "#7c3aed", 2, 8),
        _t(220, 110, "Majority → A", 13, "#6d28d9", "middle", "700"),
    ]
    return "\n".join(parts)


def mini_parallel_trees() -> str:
    parts = []
    for i, x in enumerate([60, 180, 300, 420]):
        parts += [
            _circle(x, 40, 16, "#dbeafe", "#3b82f6", 2),
            _line(x, 56, x - 12, 80, "#3b82f6", 1.5),
            _line(x, 56, x + 12, 80, "#3b82f6", 1.5),
            _t(x, 95, f"T{i+1}", 10, "#64748b", "middle"),
        ]
    parts += [_rect(120, 110, 280, 32, "#dbeafe", "#3b82f6", 2, 8), _t(260, 132, "Parallel vote", 13, "#1d4ed8", "middle", "700")]
    return "\n".join(parts)


def mini_sequential_boost() -> str:
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


def mini_kmeans() -> str:
    pts = [(60, 100), (80, 90), (100, 110), (300, 60), (320, 70), (310, 50)]
    parts = []
    for i, (x, y) in enumerate(pts):
        c = "#f97316" if i < 3 else "#8b5cf6"
        parts.append(_circle(x, y, 10, c))
    parts += [
        _circle(80, 100, 14, "none", "#f97316", 2),
        _circle(310, 60, 14, "none", "#8b5cf6", 2),
        _t(80, 130, "Centroid A", 10, "#c2410c", "middle"),
        _t(310, 90, "Centroid B", 10, "#6d28d9", "middle"),
    ]
    return "\n".join(parts)


def mini_dbscan() -> str:
    parts = [
        _circle(80, 70, 8, "#3b82f6"), _circle(95, 80, 8, "#3b82f6"), _circle(70, 85, 8, "#3b82f6"),
        _circle(280, 60, 8, "#8b5cf6"), _circle(300, 75, 8, "#8b5cf6"), _circle(290, 90, 8, "#8b5cf6"),
        _circle(200, 110, 6, "#94a3b8"), _circle(220, 115, 6, "#94a3b8"),
        _rect(50, 40, 80, 60, "none", "#3b82f6", 1.5, 20),
        _rect(260, 40, 70, 65, "none", "#8b5cf6", 1.5, 20),
        _t(200, 130, "noise", 10, "#64748b", "middle"),
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
    layers = [(40, ["x1", "x2", "x3"]), (180, ["h1", "h2"]), (320, ["y"])]
    parts = []
    for lx, nodes in layers:
        for i, n in enumerate(nodes):
            cy = 40 + i * 36
            parts += [_circle(lx, cy, 14, "#dbeafe", "#3b82f6", 2), _t(lx, cy + 5, n, 9, "#1d4ed8", "middle", "600")]
    for i in range(3):
        for j in range(2):
            parts.append(_line(54, 40 + i * 36, 166, 40 + j * 36, "#cbd5e1", 1))
    for j in range(2):
        parts.append(_line(194, 40 + j * 36, 306, 58, "#cbd5e1", 1))
    return "\n".join(parts)


def mini_training_loop() -> str:
    return flow_horizontal([("Forward", "#3b82f6"), ("Loss", "#ef4444"), ("Backward", "#f59e0b"), ("Update", "#22c55e")], y=55)


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


def mini_loss_curves() -> str:
    parts = [
        _line(30, 120, 30, 30, "#94a3b8", 1.5),
        _line(30, 120, 380, 120, "#94a3b8", 1.5),
        _t(20, 25, "loss", 10, "#64748b", "middle"),
        '  <path d="M40,110 C80,100 120,70 180,55 S280,40 360,35" fill="none" stroke="#ef4444" stroke-width="2.5"/>',
        '  <path d="M40,115 C100,108 160,95 220,88 S320,82 360,80" fill="none" stroke="#3b82f6" stroke-width="2.5"/>',
        _t(280, 50, "MSE", 10, "#ef4444", "start", "600"),
        _t(280, 65, "Cross-entropy", 10, "#3b82f6", "start", "600"),
    ]
    return "\n".join(parts)


def mini_optimizers() -> str:
    parts = [
        _line(40, 100, 40, 30, "#94a3b8", 1.5),
        _line(40, 100, 360, 100, "#94a3b8", 1.5),
        '  <path d="M60,90 L100,70 L140,75 L180,50 L220,55 L260,40 L300,45 L340,30" fill="none" stroke="#3b82f6" stroke-width="2" stroke-dasharray="6 3"/>',
        '  <path d="M60,90 C120,75 180,55 240,42 S320,30 340,28" fill="none" stroke="#22c55e" stroke-width="2.5"/>',
        _t(250, 22, "Adam (adaptive)", 10, "#22c55e", "start", "600"),
        _t(250, 88, "SGD (fixed step)", 10, "#3b82f6", "start", "600"),
    ]
    return "\n".join(parts)


def mini_overfit() -> str:
    parts = [
        _line(20, 110, 20, 20, "#94a3b8", 1.5),
        _line(20, 110, 280, 110, "#94a3b8", 1.5),
        '  <path d="M30,100 C60,95 90,40 120,60 S180,90 220,50 S260,30 270,35" fill="none" stroke="#ef4444" stroke-width="2.5"/>',
        _circle(60, 85, 4, "#3b82f6", None, 0),
        _circle(120, 70, 4, "#3b82f6", None, 0),
        _circle(180, 80, 4, "#3b82f6", None, 0),
        _circle(240, 55, 4, "#3b82f6", None, 0),
        _t(40, 125, "Memorizes noise", 10, "#b91c1c", "start"),
    ]
    return "\n".join(parts)


def mini_dropout() -> str:
    nodes = [(60, 40), (60, 80), (60, 120), (180, 60), (180, 100), (300, 80)]
    active = [True, False, True, True, False, True]
    parts = []
    for (x, y), on in zip(nodes, active):
        if on:
            parts.append(_circle(x, y, 14, "#dbeafe", "#3b82f6", 2))
        else:
            parts.append(_circle(x, y, 14, "#f1f5f9", "#94a3b8", 2))
            parts.append(_line(x - 10, y - 10, x + 10, y + 10, "#94a3b8", 2))
    parts.append(_t(180, 140, "Randomly zero neurons", 11, "#64748b", "middle"))
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


def mini_tfidf() -> str:
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


def mini_embedding() -> str:
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
        _rect(80, 40, 280, 70, "#ede9fe", "#7c3aed", 2, 8),
        _t(220, 62, "LSTM Cell", 14, "#6d28d9", "middle", "700"),
        _t(130, 88, "Forget", 10, "#64748b", "middle"),
        _t(220, 88, "Input", 10, "#64748b", "middle"),
        _t(310, 88, "Output", 10, "#64748b", "middle"),
        _rect(60, 55, 40, 20, "#fee2e2", "#ef4444", 1.5, 4),
        _rect(150, 55, 40, 20, "#dcfce7", "#22c55e", 1.5, 4),
        _rect(240, 55, 40, 20, "#dbeafe", "#3b82f6", 1.5, 4),
        _rect(330, 55, 40, 20, "#fef3c7", "#f59e0b", 1.5, 4),
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


def mini_rag() -> str:
    return flow_horizontal([
        ("Docs", "#3b82f6"), ("Chunk", "#8b5cf6"), ("Embed", "#f59e0b"),
        ("Retrieve", "#22c55e"), ("LLM", "#ec4899"),
    ], y=45)


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


def mini_react_loop() -> str:
    parts = [
        _rect(40, 40, 90, 36, "#dbeafe", "#3b82f6", 2, 6),
        _t(85, 64, "Thought", 12, "#1d4ed8", "middle", "700"),
        _arrow(130, 58, 170, 58),
        _rect(170, 40, 90, 36, "#fef3c7", "#f59e0b", 2, 6),
        _t(215, 64, "Action", 12, "#b45309", "middle", "700"),
        _arrow(260, 58, 300, 58),
        _rect(300, 40, 110, 36, "#dcfce7", "#22c55e", 2, 6),
        _t(355, 64, "Observation", 11, "#15803d", "middle", "700"),
        _t(220, 100, "↺ repeat until done", 11, "#64748b", "middle"),
    ]
    return "\n".join(parts)


def mini_mcp() -> str:
    parts = [
        _rect(30, 45, 120, 60, "#dbeafe", "#3b82f6", 2, 8),
        _t(90, 72, "MCP Client", 12, "#1d4ed8", "middle", "700"),
        _t(90, 90, "(Host app)", 10, "#64748b", "middle"),
        _line(150, 75, 280, 75, "#64748b", 2),
        f'<polygon points="280,75 272,71 272,79" fill="#64748b"/>',
        _rect(280, 45, 120, 60, "#ede9fe", "#7c3aed", 2, 8),
        _t(340, 72, "MCP Server", 12, "#6d28d9", "middle", "700"),
        _t(340, 90, "Tools + resources", 10, "#64748b", "middle"),
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
    parts = [
        _rect(160, 10, 120, 36, "#dbeafe", "#3b82f6", 2, 6),
        _t(220, 34, "Triage", 12, "#1d4ed8", "middle", "700"),
        _line(190, 46, 100, 80, "#94a3b8", 1.5),
        _line(250, 46, 220, 80, "#94a3b8", 1.5),
        _line(220, 46, 340, 80, "#94a3b8", 1.5),
        _rect(40, 80, 100, 36, "#dcfce7", "#22c55e", 2, 6),
        _t(90, 104, "Billing", 11, "#15803d", "middle", "700"),
        _rect(170, 80, 100, 36, "#fef3c7", "#f59e0b", 2, 6),
        _t(220, 104, "Tech", 11, "#b45309", "middle", "700"),
        _rect(300, 80, 100, 36, "#ede9fe", "#7c3aed", 2, 6),
        _t(350, 104, "Sales", 11, "#6d28d9", "middle", "700"),
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

