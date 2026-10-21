import sys, pathlib
from playwright.sync_api import sync_playwright
# usage: shot.py board <html> <out.png>   |   shot.py slides <html> <outdir>
mode, html, out = sys.argv[1], pathlib.Path(sys.argv[2]).resolve(), pathlib.Path(sys.argv[3]).resolve()
with sync_playwright() as p:
    b = p.chromium.launch(channel="chrome")
    if mode == "board":
        pg = b.new_page(viewport={"width": 1280, "height": 900})
        pg.goto(html.as_uri(), wait_until="domcontentloaded"); pg.evaluate("document.fonts.ready"); pg.wait_for_timeout(3500)
        print("fonts", pg.evaluate("['800 20px \"Bricolage Grotesque\"','italic 20px \"Instrument Serif\"','20px Geist','20px \"Geist Mono\"'].map(f=>document.fonts.check(f,'ąęłż'))"))
        pg.screenshot(path=str(out), full_page=True)
        pg.set_viewport_size({"width": 390, "height": 844}); pg.wait_for_timeout(600)
        print("mobile overflow", pg.evaluate("document.documentElement.scrollWidth>innerWidth"))
    else:
        out.mkdir(parents=True, exist_ok=True)
        pg = b.new_page(viewport={"width": 1080, "height": 1350}, device_scale_factor=1)
        pg.goto(html.as_uri(), wait_until="domcontentloaded"); pg.evaluate("document.fonts.ready"); pg.wait_for_timeout(3500)
        print("fonts", pg.evaluate("['800 20px \"Bricolage Grotesque\"','italic 20px \"Instrument Serif\"','20px Geist','20px \"Geist Mono\"'].map(f=>document.fonts.check(f,'ąęłż'))"))
        # overflow check: any element inside a slide extending past slide bounds (minus safe margin)
        print("overflow", pg.evaluate("""[...document.querySelectorAll('.slide')].map((s,i)=>{const r=s.getBoundingClientRect();let bad=[];s.querySelectorAll('.body *, .top, .bottom').forEach(e=>{const q=e.getBoundingClientRect();if(q.width&&(q.right>r.right-60||q.left<r.left+60||q.bottom>r.bottom-50||q.top<r.top+50))bad.push(e.className||e.tagName)});return i+1+':'+bad.slice(0,3).join(',')})"""))
        for i, el in enumerate(pg.query_selector_all(".slide"), 1):
            el.screenshot(path=str(out / f"slide-{i:02d}.png"))
        print("slides", i)
    b.close()
