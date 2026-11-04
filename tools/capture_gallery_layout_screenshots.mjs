import { chromium } from "playwright";
import fs from "node:fs/promises";
import path from "node:path";

const decks = ["fr9", "en9", "enlit", "ensci"];
const base = "http://127.0.0.1:8765";
const out = "/tmp/anki-gallery-layout-shots";
await fs.rm(out, { recursive: true, force: true });
await fs.mkdir(out, { recursive: true });

const browser = await chromium.launch({ headless: true, args: ["--no-sandbox"] });
try {
  for (const deck of decks) {
    for (const viewport of [
      { name: "mobile", width: 390, height: 844 },
      { name: "desktop", width: 1440, height: 1000 }
    ]) {
      const page = await browser.newPage({ viewport: { width: viewport.width, height: viewport.height }, deviceScaleFactor: 1 });
      const errors = [];
      page.on("pageerror", e => errors.push(e.message));
      await page.emulateMedia({ reducedMotion: "reduce" });
      await page.goto(`${base}/${deck}.html`, { waitUntil: "domcontentloaded" });
      await page.evaluate(() => {
        if (typeof window.closeOnboarding === "function") window.closeOnboarding();
        if (typeof window.openGalleryBrowser === "function") window.openGalleryBrowser();
      });
      await page.waitForFunction(() => document.querySelectorAll("#gbGrid .gb-item").length === 100, null, { timeout: 20000 });
      await page.waitForTimeout(700);
      const summary = await page.evaluate(() => ({
        cards: document.querySelectorAll("#gbGrid .gb-item").length,
        imgs: document.querySelectorAll("#gbGrid img.gb-img").length,
        gridVisible: !!document.querySelector("#gbGrid") && getComputedStyle(document.querySelector("#gbGrid")).display !== "none",
        title: document.title
      }));
      if (summary.cards !== 100 || summary.imgs !== 100 || !summary.gridVisible) throw new Error(deck + " " + viewport.name + ": " + JSON.stringify(summary));
      // The gallery browser is a fixed, internally scrollable surface.
      // Capture its actual viewport rather than a misleading full-page image.
      const file = path.join(out, deck + "-" + viewport.name + "-grid-top.png");
      await page.screenshot({ path: file, fullPage: false, animations: "disabled" });
      const grid = page.locator("#gbGrid");
      await grid.evaluate(el => { el.scrollTop = el.scrollHeight; });
      await page.waitForTimeout(450);
      const bottomFile = path.join(out, deck + "-" + viewport.name + "-grid-bottom.png");
      await page.screenshot({ path: bottomFile, fullPage: false, animations: "disabled" });
      await grid.evaluate(el => { el.scrollTop = 0; });
      await page.evaluate(() => {
        if (typeof showOnboarding === "function") showOnboarding();
      });
      await page.waitForSelector("#onboardOverlay .tour-title", { state: "visible", timeout: 10000 });
      const tourFile = path.join(out, deck + "-" + viewport.name + "-tour.png");
      await page.screenshot({ path: tourFile, fullPage: false, animations: "disabled" });
      await page.evaluate(() => {
        if (typeof closeOnboarding === "function") closeOnboarding();
      });
      if (errors.length) throw new Error(deck + " " + viewport.name + " page errors: " + errors.join(" | "));
      console.log("PASS", deck, viewport.name, JSON.stringify(summary), file);
      await page.close();
    }
  }
} finally {
  await browser.close();
}
