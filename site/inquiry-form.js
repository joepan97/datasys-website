/* DataSys inquiry form: no credentials or personal data are sent to analytics. */
(() => {
  const services = {
    general: '一般需求', netapp: 'NetApp 儲存', lto: 'LTO 磁帶',
    parts: '二手零件與設備', rental: 'Storage 租賃', security: '資訊安全', ai: 'AI 解決方案'
  };
  const endpoint = '/api/inquiries';
  const tracked = (event, data = {}) => {
    window.dataLayer = window.dataLayer || [];
    window.dataLayer.push({ event, page_path: location.pathname, ...data });
  };
  const esc = (value) => String(value).replace(/[&<>"']/g, c => ({ '&':'&amp;', '<':'&lt;', '>':'&gt;', '"':'&quot;', "'":'&#039;' })[c]);
  const select = (name, label, options, required = false) => `<div class="field"><label for="${name}">${label}${required ? ' <span>必填</span>' : ''}</label><select id="${name}" name="${name}"${required ? ' required' : ''}><option value="">請選擇</option>${options.map(x => `<option value="${esc(x)}">${esc(x)}</option>`).join('')}</select></div>`;
  const input = (name, label, type = 'text', required = false, attrs = '') => `<div class="field"><label for="${name}">${label}${required ? ' <span>必填</span>' : ''}</label><input id="${name}" name="${name}" type="${type}"${required ? ' required' : ''} ${attrs}></div>`;
  const serviceFields = (type) => {
    if (type === 'parts') return input('brand_model', '設備品牌／型號', 'text', true) + input('part_number', '零件編號／Part Number') + input('quantity', '需求數量', 'number', false, 'min="1" step="1" inputmode="numeric"') + select('urgency', '需求類型', ['故障急件','計畫性擴充','備品採購','其他'], true) + input('need_by_date', '期望到貨日期', 'date');
    if (type === 'rental') return input('required_capacity', '所需容量') + input('rental_period', '預計租期') + select('project_type', '專案類型', ['資料搬遷／設備汰換','機房搬遷','POC 測試','設備維修替代','其他']) + input('delivery_location', '交付地點') + input('need_by_date', '需求日期', 'date');
    if (type === 'netapp') return select('workload_type', '主要工作負載', ['檔案服務','虛擬化','資料庫','備份／歸檔','其他']) + input('current_capacity', '目前／預估容量') + input('performance_requirement', '效能需求') + select('deployment_timeline', '預計導入時程', ['一個月內','一至三個月','三個月以上','尚未確定']);
    if (type === 'ai') return input('business_process', '想改善的流程') + input('current_systems', '目前使用的系統') + select('data_sensitivity', '資料敏感程度', ['一般內部資料','含個資／機敏資料','尚待評估']) + select('preferred_deployment', '偏好部署方式', ['雲端','地端','混合式','尚未確定']) + select('project_timeline', '預計時程', ['一個月內','一至三個月','三個月以上','尚未確定']);
    return '';
  };
  const render = (mount, type) => {
    mount.innerHTML = `<form class="form inquiry-form" novalidate data-service="${type}">
      <h2>${type === 'parts' ? '快速詢料：提供型號或料號' : '告訴我們您的需求'}</h2>
      <p class="form-intro">帶有 <span>必填</span> 的欄位為必要資訊。我們會依提供內容確認後聯絡您。</p>
      <div class="form-grid common-fields">
        ${input('contact_name', '聯絡人', 'text', true, 'autocomplete="name"')}
        ${input('company_name', '公司名稱', 'text', true, 'autocomplete="organization"')}
        ${input('phone', '電話', 'tel', true, 'autocomplete="tel" inputmode="tel"')}
        ${input('email', 'Email', 'email', true, 'autocomplete="email"')}
        <div class="field"><label for="service_type">需求類型 <span>必填</span></label><select id="service_type" name="service_type" required>${Object.entries(services).map(([key, value]) => `<option value="${key}"${key === type ? ' selected' : ''}>${value}</option>`).join('')}</select></div>
        <div class="service-fields field-wide">${serviceFields(type)}</div>
        <div class="field field-wide"><label for="requirement">需求說明 <span>必填</span></label><textarea id="requirement" name="requirement" required placeholder="請說明目前環境、需求或遇到的問題"></textarea></div>
      </div>
      <div class="hp-field" aria-hidden="true"><label>不要填寫這個欄位<input name="website" tabindex="-1" autocomplete="off"></label></div>
      <input type="hidden" name="source_page" value="${esc(location.pathname)}"><input type="hidden" name="utm_source"><input type="hidden" name="utm_medium"><input type="hidden" name="utm_campaign"><input type="hidden" name="started_at" value="${Date.now()}">
      <button class="btn submit-btn" type="submit">送出需求</button>
      <p class="privacy-note">實際供貨、相容性與保固條件以正式報價內容為準。</p><p class="form-status" role="status" aria-live="polite"></p>
    </form>`;
    const form = mount.querySelector('form'); const status = form.querySelector('.form-status'); const submit = form.querySelector('[type=submit]');
    const url = new URL(location.href); ['utm_source','utm_medium','utm_campaign'].forEach(k => form.elements[k].value = url.searchParams.get(k) || '');
    const serviceSelect = form.elements.service_type;
    serviceSelect.addEventListener('change', () => { const next = serviceSelect.value; mount.dataset.service = next; render(mount, next); });
    let started = false;
    form.addEventListener('input', () => { if (!started) { started = true; tracked('form_start', { service_type: form.elements.service_type.value, form_id: 'inquiry-form' }); } }, { once: true });
    form.addEventListener('submit', async e => {
      e.preventDefault(); status.className = 'form-status';
      if (!form.checkValidity()) { form.reportValidity(); status.classList.add('is-error'); status.textContent = '請完成必填欄位，並確認 Email 格式。'; return; }
      submit.disabled = true; submit.textContent = '送出中…';
      const payload = Object.fromEntries(new FormData(form).entries());
      tracked('form_submit', { service_type: payload.service_type, form_id: 'inquiry-form' });
      try {
        const response = await fetch(endpoint, { method: 'POST', headers: {'Content-Type':'application/json','Accept':'application/json'}, body: JSON.stringify(payload) });
        const body = await response.json().catch(() => ({}));
        if (!response.ok || !body.ok) throw new Error(body.error || 'submit_failed');
        status.textContent = '已收到您的需求。我們將依提供的資訊確認後儘快聯絡您；實際供貨、相容性與保固條件以正式報價內容為準。';
        tracked('form_submit_success', { service_type: payload.service_type, form_id: 'inquiry-form' }); form.reset();
      } catch (_) {
        status.classList.add('is-error'); status.textContent = '目前無法送出需求，請直接來電 02-2697-3311，或寄信至 sales@datasys.com.tw。';
        tracked('form_submit_error', { service_type: payload.service_type, form_id: 'inquiry-form' });
      } finally { submit.disabled = false; submit.textContent = '送出需求'; }
    });
  };
  document.addEventListener('DOMContentLoaded', () => {
    const fromQuery = new URL(location.href).searchParams.get('service');
    document.querySelectorAll('[data-inquiry-form]').forEach(mount => render(mount, services[fromQuery] ? fromQuery : (mount.dataset.inquiryForm || 'general')));
    document.querySelectorAll('a[href^="tel:"]').forEach(a => a.addEventListener('click', () => tracked('click_phone', { cta_location: a.dataset.ctaLocation || 'inline' })));
    document.querySelectorAll('a[href^="mailto:"]').forEach(a => a.addEventListener('click', () => tracked('click_email', { cta_location: a.dataset.ctaLocation || 'inline' })));
    document.querySelectorAll('[data-track-cta]').forEach(a => a.addEventListener('click', () => tracked('click_cta', { cta_location: a.dataset.ctaLocation || 'inline', service_type: a.dataset.service || 'general' })));
  });
})();
