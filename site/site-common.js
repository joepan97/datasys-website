(() => {
  const base = 'https://www.datasys.com.tw/';
  const page = location.pathname.split('/').pop() || 'index.html';
  const serviceMap = { 'netapp.html':'NetApp 儲存設備規劃與維護', 'lto.html':'IBM LTO 磁帶供應', 'parts.html':'二手零件與設備詢料', 'rental.html':'Storage 短期租賃', 'security.html':'資訊安全環境評估', 'ai.html':'AI 流程評估與導入' };
  const serviceTypeByPage = { 'netapp.html':'netapp', 'lto.html':'lto', 'parts.html':'parts', 'rental.html':'rental', 'security.html':'security', 'ai.html':'ai' };
  const header = document.querySelector('header'); const nav = header?.querySelector('nav'); const burger = header?.querySelector('.burger');
  if (burger && nav) {
    // Older generated pages have an inline handler. Remove it so a tap only
    // toggles the menu once; otherwise the inline and delegated handlers cancel out.
    burger.removeAttribute('onclick');
    burger.setAttribute('type', 'button');
    burger.setAttribute('aria-expanded', 'false');
    burger.addEventListener('click', () => {
      const open = nav.classList.toggle('open');
      burger.setAttribute('aria-expanded', String(open));
      burger.setAttribute('aria-label', open ? '關閉選單' : '開啟選單');
    });
    document.addEventListener('keydown', e => {
      if (e.key === 'Escape' && nav.classList.contains('open')) {
        nav.classList.remove('open');
        burger.focus();
        burger.setAttribute('aria-expanded', 'false');
        burger.setAttribute('aria-label', '開啟選單');
      }
    });
  }
  const serviceType = serviceTypeByPage[page];
  if (serviceType) document.querySelectorAll('.hero a[href="contact.html"], .cta-band a[href="contact.html"]').forEach(link => { link.href = `contact.html?service=${serviceType}`; link.dataset.service = serviceType; link.dataset.trackCta = ''; });
  const companyFooter = [...document.querySelectorAll('footer .grid > div')].find(section => section.querySelector('h4')?.textContent.trim() === '公司');
  if (companyFooter && !companyFooter.querySelector('a[href="/privacy-policy"]')) {
    companyFooter.insertAdjacentHTML('beforeend', '<span data-legal-links><a href="/privacy-policy">隱私權政策</a><a href="/data-deletion">資料刪除說明</a></span>');
  }
  document.body.insertAdjacentHTML('beforeend', `<div class="sticky-cta" aria-label="快速聯絡"><a class="call" href="tel:0226973311" data-cta-location="sticky_mobile">電話詢價</a><a class="request" data-track-cta data-cta-location="sticky_mobile" href="/contact.html">填寫需求</a></div>`);
})();
