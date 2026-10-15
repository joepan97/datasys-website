(() => {
  const base = 'https://www.datasys.com.tw/';
  const page = location.pathname.split('/').pop() || 'index.html';
  const serviceMap = { 'netapp.html':'NetApp 儲存設備規劃與維護', 'lto.html':'IBM LTO 磁帶供應', 'parts.html':'二手零件與設備詢料', 'rental.html':'Storage 短期租賃', 'security.html':'資訊安全環境評估', 'ai.html':'AI 流程評估與導入' };
  const serviceTypeByPage = { 'netapp.html':'netapp', 'lto.html':'lto', 'parts.html':'parts', 'rental.html':'rental', 'security.html':'security', 'ai.html':'ai' };
  const org = { '@context':'https://schema.org', '@graph': [
    { '@type':'Organization', '@id':base+'#organization', name:'元僑科技有限公司', alternateName:'DataSys Technologies', url:base, email:'sales@datasys.com.tw', telephone:'+886-2-2697-3311' },
    { '@type':'LocalBusiness', '@id':base+'#localbusiness', name:'元僑科技有限公司', url:base, telephone:'+886-2-2697-3311', email:'sales@datasys.com.tw', address:{ '@type':'PostalAddress', addressCountry:'TW', addressRegion:'新北市', addressLocality:'汐止區', streetAddress:'新台五路一段99號31樓之3' } },
    { '@type':'WebSite', '@id':base+'#website', url:base, name:'元僑科技' }
  ]};
  if (serviceMap[page]) org['@graph'].push({ '@type':'Service', name:serviceMap[page], provider:{ '@id':base+'#organization' }, areaServed:{ '@type':'Country', name:'Taiwan' }, url:base+page });
  org['@graph'].push({ '@type':'BreadcrumbList', itemListElement:[{ '@type':'ListItem', position:1, name:'首頁', item:base }, { '@type':'ListItem', position:2, name:document.querySelector('h1')?.textContent.trim() || '頁面', item:base+page }] });
  const questions = [...document.querySelectorAll('details.faq')].map(item => ({ '@type':'Question', name:item.querySelector('summary')?.textContent.trim(), acceptedAnswer:{ '@type':'Answer', text:item.querySelector('p')?.textContent.trim() } }));
  if (questions.length) org['@graph'].push({ '@type':'FAQPage', mainEntity:questions });
  const script = document.createElement('script'); script.type = 'application/ld+json'; script.textContent = JSON.stringify(org); document.head.append(script);
  const header = document.querySelector('header'); const nav = header?.querySelector('nav'); const burger = header?.querySelector('.burger');
  if (burger && nav) { burger.setAttribute('aria-expanded', 'false'); burger.addEventListener('click', () => { const open = nav.classList.toggle('open'); burger.setAttribute('aria-expanded', String(open)); burger.setAttribute('aria-label', open ? '關閉選單' : '開啟選單'); }); document.addEventListener('keydown', e => { if (e.key === 'Escape' && nav.classList.contains('open')) { nav.classList.remove('open'); burger.focus(); burger.setAttribute('aria-expanded','false'); } }); }
  const serviceType = serviceTypeByPage[page];
  if (serviceType) document.querySelectorAll('.hero a[href="contact.html"], .cta-band a[href="contact.html"]').forEach(link => { link.href = `contact.html?service=${serviceType}`; link.dataset.service = serviceType; link.dataset.trackCta = ''; });
  document.body.insertAdjacentHTML('beforeend', `<div class="sticky-cta" aria-label="快速聯絡"><a class="call" href="tel:0226973311" data-cta-location="sticky_mobile">電話詢價</a><a class="request" data-track-cta data-cta-location="sticky_mobile" href="contact.html">填寫需求</a></div>`);
})();
