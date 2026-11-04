import { chromium } from "playwright";
import fs from "node:fs/promises";
import path from "node:path";

const decks = ["fr9", "en9", "enlit", "ensci"];
const sampleWords = { fr9: "Leçon", en9: "Student", enlit: "Novel", ensci: "Atom" };
const baseUrl = process.env.GALLERY_BASE_URL || "http://127.0.0.1:8765";
const outputRoot = process.env.GALLERY_PNG_DIR || "/tmp/anki-gallery-preview-png";

await fs.rm(outputRoot, { recursive: true, force: true });
await fs.mkdir(outputRoot, { recursive: true });

const browser = await chromium.launch({ headless: true, args: ["--no-sandbox"] });
try {
  for (const deck of decks) {
    const source = await browser.newPage({ viewport: { width: 390, height: 844 }, deviceScaleFactor: 1 });
    const pageErrors = [];
    source.on("pageerror", error => pageErrors.push(error.message));
    await source.goto(`${baseUrl}/${deck}.html`, { waitUntil: "domcontentloaded" });
    await source.waitForFunction(() =>
      typeof window.__GALLERY_THUMB_DOC__ === "function" &&
      Array.isArray(window.EMBEDDED_DESIGNS_100) &&
      window.EMBEDDED_DESIGNS_100.length === 100,
      null,
      { timeout: 30000 }
    );

    const outputDir = path.join(outputRoot, deck);
    await fs.mkdir(outputDir, { recursive: true });
    const capturePage = await browser.newPage({
      viewport: { width: 440, height: 900 },
      deviceScaleFactor: 1
    });
    let sampleHits = 0;

    for (let i = 0; i < 100; i++) {
      const doc = await source.evaluate(index =>
        window.__GALLERY_THUMB_DOC__(window.EMBEDDED_DESIGNS_100[index]), i);
      if (typeof doc !== "string" || doc.length < 250) {
        throw new Error(`${deck} design ${i + 1}: preview document is empty or invalid`);
      }
      if (doc.includes(sampleWords[deck])) sampleHits++;

      await capturePage.setContent(doc, { waitUntil: "domcontentloaded" });
      await capturePage.addStyleTag({
        content: "html,body{width:440px!important;height:900px!important;margin:0!important;overflow:hidden!important}*,*::before,*::after{animation:none!important;transition:none!important;caret-color:transparent!important}"
      });
      await capturePage.evaluate(() => Promise.race([
        document.fonts ? document.fonts.ready : Promise.resolve(),
        new Promise(resolve => setTimeout(resolve, 1000))
      ]));
      await capturePage.waitForTimeout(65);

      const file = path.join(outputDir, String(i + 1).padStart(3, "0") + ".png");
      await capturePage.screenshot({ path: file, type: "png", fullPage: false });
    }

    if (sampleHits < 1) {
      throw new Error(`${deck}: none of the 100 captured previews contains its expected sample word`);
    }
    if (pageErrors.length) {
      throw new Error(`${deck}: page errors while rendering: ${pageErrors.join(" | ")}`);
    }

    console.log(`PASS ${deck}: captured 100 deck-specific template previews; sample word appears in ${sampleHits}`);
    await capturePage.close();
    await source.close();
  }
} finally {
  await browser.close();
}
