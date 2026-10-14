// Captura una web entera tal como se ve en un movil (para hacer scroll en el video).
// Uso (desde remotion/): node scripts/captura_web.mjs <url o ruta.html> <salida.png> [ancho=390] [selectores,separados,por,comas]
// Con selectores, guarda tambien <salida>.json con la caja de cada elemento (en px de la captura).
import { chromium } from 'playwright-core';
import path from 'path';
import fs from 'fs';
const [src, out, anchoS, sels] = process.argv.slice(2);
const ancho = Number(anchoS) || 390;
const url = /^https?:/.test(src) ? src : 'file://' + path.resolve(src);
const exe = '/opt/pw-browsers/chromium-1194/chrome-linux/chrome';
const b = await chromium.launch(fs.existsSync(exe) ? { executablePath: exe } : {});
const p = await b.newPage({ viewport: { width: ancho, height: 844 }, deviceScaleFactor: 2.5, isMobile: true, hasTouch: true, locale: 'es-ES' });
await p.goto(url, { waitUntil: 'networkidle', timeout: 60000 });
await p.waitForTimeout(1200);
await p.screenshot({ path: out, fullPage: true });
const info = await p.evaluate((sels) => {
  const r = { anchoCss: document.documentElement.scrollWidth, altoCss: document.documentElement.scrollHeight, cajas: {} };
  for (const s of sels) { const e = document.querySelector(s); if (e) { const b = e.getBoundingClientRect(); r.cajas[s] = [b.x + scrollX, b.y + scrollY, b.width, b.height]; } }
  return r;
}, (sels || '').split(',').filter(Boolean));
info.escala = 2.5;
fs.writeFileSync(out.replace(/\.png$/, '.json'), JSON.stringify(info, null, 1));
console.log(out);
await b.close();
