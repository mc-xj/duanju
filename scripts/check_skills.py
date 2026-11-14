"""Run local installation smoke tests without editing project documents."""
import json
from pathlib import Path
import subprocess
import sys
import tempfile
from zipfile import ZipFile
import yaml

ROOT = Path(__file__).resolve().parents[1]
SKILLS = ROOT / ".agents/skills"
results = {}

def run(*args):
    result = subprocess.run(args, capture_output=True, text=True, cwd=ROOT)
    if result.returncode:
        raise RuntimeError(result.stderr or result.stdout)
    return result.stdout

for name in ["caveman", "markitdown", "ppt-master", "harness-anything"]:
    text = (SKILLS / name / "SKILL.md").read_text()
    assert text.startswith("---\n"), name
    metadata = yaml.safe_load(text.split("---", 2)[1])
    assert metadata["name"] == name and metadata["description"], name
    results[name] = {"entry": "pass"}

run(sys.executable, "-m", "pip", "check")
run(sys.executable, str(SKILLS / "ppt-master/scripts/attribution_guard.py"))
results["ppt-master"]["integrity"] = "pass"
assert "Never drop not/never/no/only/except" in (SKILLS / "caveman/SKILL.md").read_text()
results["caveman"]["scope"] = "core text skill; no hooks or CLI installed"

with tempfile.TemporaryDirectory(prefix="duanju-skills-") as work:
    work = Path(work)
    # Use an existing Chinese project document; never modify the source.
    import onnxruntime
    onnxruntime.disable_telemetry_events()
    from markitdown import MarkItDown
    source = ROOT / "02_逐场独立分镜/第01段_雨夜翻页_超详细分镜.docx"
    text = MarkItDown(enable_plugins=False).convert_local(str(source)).text_content
    assert "雨夜翻页" in text and "1-1-01" in text
    results["markitdown"]["docx_conversion"] = "pass"
    results["markitdown"]["output_characters"] = len(text)

    # Test the installed CLI's actual project editing path.
    cli = ROOT / ".venv-tools/bin/cli-anything-office"
    run(str(cli), "--help")
    project = work / "office.json"
    run(str(cli), "document", "new", "--type", "writer", "--name", "安装测试", "-o", str(project))
    run(str(cli), "--project", str(project), "writer", "add-paragraph", "--text", "片尾六镜每镜六秒")
    assert "片尾六镜每镜六秒" in json.dumps(json.loads(project.read_text()), ensure_ascii=False)
    results["harness-anything"]["json_edit"] = "pass"
    html = work / "input.html"
    html.write_text('<html><meta charset="utf-8"><body><p>守护与铭记</p></body></html>')
    converted = work / "office.pdf"
    run(sys.executable, str(ROOT / "scripts/harness_convert.py"), str(html), str(converted))
    import fitz
    with fitz.open(converted) as pdf:
        assert len(pdf) == 1 and "守护" in pdf[0].get_text()
    results["harness-anything"]["libreoffice_conversion"] = "pass"
    # Preserve the no-overwrite contract of the thin conversion adapter.
    refusal = subprocess.run([sys.executable, str(ROOT / "scripts/harness_convert.py"), str(html), str(converted)], capture_output=True, text=True)
    assert refusal.returncode != 0 and "FileExistsError" in refusal.stderr
    results["harness-anything"]["existing_output_protected"] = "pass"

    # Exercise the upstream PPT exporter with a text-only smoke-test page.
    sys.path.insert(0, str(SKILLS / "ppt-master/scripts"))
    from svg_to_pptx import create_pptx_with_native_svg
    svg = work / "slide.svg"
    svg.write_text('<svg xmlns="http://www.w3.org/2000/svg" width="1280" height="720" viewBox="0 0 1280 720"><text x="80" y="120" font-family="Noto Sans CJK SC" font-size="36" fill="#142631">技能安装测试</text></svg>')
    pptx = work / "test.pptx"
    assert create_pptx_with_native_svg([svg], pptx, resource_root=work, pptx_structure="flat", verbose=False, workers=1)
    with ZipFile(pptx) as package:
        assert "技能安装测试" in package.read("ppt/slides/slide1.xml").decode()
    results["ppt-master"]["native_pptx_export"] = "pass"

print(json.dumps(results, ensure_ascii=False, indent=2))
