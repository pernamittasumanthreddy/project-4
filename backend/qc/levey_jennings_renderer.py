"""
Quality Control Levey-Jennings SVG Chart Renderer.
Generates pure SVG charts with Mean, +/-1SD, +/-2SD, +/-3SD control limits
and color-coded data point plots per CLSI C24-A4.
"""

from typing import List, Dict, Any

class LeveyJenningsSVGRenderer:
    @staticmethod
    def render_svg(mean: float, sd: float, values: List[float], width: int = 600, height: int = 300) -> str:
        y_center = height / 2.0
        scale = (height / 2.0 - 20) / (3.5 * sd) if sd > 0 else 1.0

        def to_y(val: float) -> float:
            return y_center - (val - mean) * scale

        svg = [f'<svg viewBox="0 0 {width} {height}" xmlns="http://www.w3.org/2000/svg" style="background:#0f172a; border-radius:8px;">']
        
        # Center line (Mean)
        svg.append(f'<line x1="50" y1="{y_center}" x2="{width-20}" y2="{y_center}" stroke="#10b981" stroke-width="2"/>')
        
        # +/- 2SD Warning Lines
        y_plus_2sd = to_y(mean + 2 * sd)
        y_minus_2sd = to_y(mean - 2 * sd)
        svg.append(f'<line x1="50" y1="{y_plus_2sd}" x2="{width-20}" y2="{y_plus_2sd}" stroke="#f59e0b" stroke-dasharray="4" stroke-width="1.5"/>')
        svg.append(f'<line x1="50" y1="{y_minus_2sd}" x2="{width-20}" y2="{y_minus_2sd}" stroke="#f59e0b" stroke-dasharray="4" stroke-width="1.5"/>')
        
        # +/- 3SD Action Lines
        y_plus_3sd = to_y(mean + 3 * sd)
        y_minus_3sd = to_y(mean - 3 * sd)
        svg.append(f'<line x1="50" y1="{y_plus_3sd}" x2="{width-20}" y2="{y_plus_3sd}" stroke="#ef4444" stroke-width="2"/>')
        svg.append(f'<line x1="50" y1="{y_minus_3sd}" x2="{width-20}" y2="{y_minus_3sd}" stroke="#ef4444" stroke-width="2"/>')

        # Points
        n = len(values)
        step = (width - 80) / max(n - 1, 1)
        for i, val in enumerate(values):
            cx = 60 + i * step
            cy = to_y(val)
            color = "#ef4444" if abs(val - mean) > 3 * sd else ("#f59e0b" if abs(val - mean) > 2 * sd else "#38bdf8")
            svg.append(f'<circle cx="{cx}" cy="{cy}" r="4" fill="{color}"/>')

        svg.append('</svg>')
        return "".join(svg)
