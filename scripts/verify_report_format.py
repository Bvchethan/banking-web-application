import docx
from docx.shared import Inches, Pt
import sys

doc = docx.Document("output/final-report/NovaBank_Final_Report_Chethan_BV.docx")
print("=== VERIFYING WORD DOCUMENT FORMATTING ===")

errors = []

# Verify margins
for idx, section in enumerate(doc.sections):
    margins = {
        "top": section.top_margin.inches,
        "bottom": section.bottom_margin.inches,
        "left": section.left_margin.inches,
        "right": section.right_margin.inches
    }
    print(f"Section {idx} Margins: {margins}")
    for margin_name, val in margins.items():
        if abs(val - 1.0) > 0.01:
            errors.append(f"Section {idx} {margin_name} margin is not 1 inch: {val} inches")

# Verify Paragraph Font and Line Spacing
p_count = 0
for idx, p in enumerate(doc.paragraphs):
    if not p.text.strip():
        continue
    p_count += 1
    
    # Check line spacing
    spacing = p.paragraph_format.line_spacing
    # If line spacing is not set on the paragraph itself, it inherits, but we explicitly set it.
    if spacing is not None and abs(spacing - 1.5) > 0.01:
        # Check if it is a heading or custom paragraph
        # Heading styles might have different spacing, but we set line_spacing = 1.5 in add_para
        errors.append(f"Paragraph {idx} ('{p.text[:30]}...') does not have 1.5 line spacing: {spacing}")

    # Check font in runs
    for r_idx, run in enumerate(p.runs):
        if run.text.strip() and run.font.name and run.font.name != "Times New Roman":
            errors.append(f"Paragraph {idx} Run {r_idx} does not use Times New Roman: {run.font.name}")

print(f"Verified {p_count} non-empty paragraphs.")
if errors:
    print(f"Verification FAILED with {len(errors)} errors:")
    for err in errors[:20]:
         print(f"  - {err}")
    sys.exit(1)
else:
    print("Verification PASSED! Formatting is correct.")
    sys.exit(0)
