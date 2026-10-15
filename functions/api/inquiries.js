// Cloudflare Pages Function. Set INQUIRY_WEBHOOK_URL as a Pages secret; never expose it to the browser.
const allowed = new Set(['netapp', 'lto', 'parts', 'rental', 'security', 'ai', 'general']);
const required = ['contact_name', 'company_name', 'phone', 'email', 'service_type', 'requirement'];
const text = value => typeof value === 'string' ? value.trim() : '';

export async function onRequestPost({ request, env }) {
  const length = Number(request.headers.get('content-length') || 0);
  if (length > 16_000) return Response.json({ ok: false, error: 'payload_too_large' }, { status: 413 });
  let data;
  try { data = await request.json(); } catch { return Response.json({ ok: false, error: 'invalid_json' }, { status: 400 }); }
  if (!data || text(data.website)) return Response.json({ ok: true }); // Honeypot: do not reveal detection.
  if (Date.now() - Number(data.started_at || Date.now()) < 2500) return Response.json({ ok: false, error: 'too_fast' }, { status: 400 });
  if (required.some(key => !text(data[key])) || !allowed.has(text(data.service_type))) return Response.json({ ok: false, error: 'validation_error' }, { status: 422 });
  if (!/^[^\s@]+@[^\s@]+\.[^\s@]+$/.test(text(data.email)) || !/^[0-9+()\-\s]{7,24}$/.test(text(data.phone))) return Response.json({ ok: false, error: 'validation_error' }, { status: 422 });
  const clean = Object.fromEntries(Object.entries(data).filter(([key]) => key !== 'website').map(([key, value]) => [key, text(value).slice(0, 3000)]));
  // Bind an optional KV namespace named INQUIRY_RATE_LIMIT for production IP rate limiting.
  const ip = request.headers.get('CF-Connecting-IP') || 'unknown'; const rateKey = `inquiry:${ip}`;
  if (env.INQUIRY_RATE_LIMIT) { if (await env.INQUIRY_RATE_LIMIT.get(rateKey)) return Response.json({ ok: false, error: 'rate_limited' }, { status: 429 }); await env.INQUIRY_RATE_LIMIT.put(rateKey, '1', { expirationTtl: 600 }); }
  if (!env.INQUIRY_WEBHOOK_URL) return Response.json({ ok: false, error: 'notification_unconfigured' }, { status: 503 });
  const notify = await fetch(env.INQUIRY_WEBHOOK_URL, { method: 'POST', headers: { 'Content-Type': 'application/json' }, body: JSON.stringify({ subject: `[網站詢價] ${clean.service_type}｜${clean.company_name}`, submitted_at: new Date().toISOString(), inquiry: clean }) });
  if (!notify.ok) return Response.json({ ok: false, error: 'notification_failed' }, { status: 502 });
  return Response.json({ ok: true });
}
