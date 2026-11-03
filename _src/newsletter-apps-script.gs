// victseng.com 電子報訂閱
// 1) 把網站表單寫進這份試算表  2) 寄通知信給你  3) 依語言寄歡迎確認信給訂閱者
const NOTIFY = 'victseng.consult@gmail.com';

const WELCOME = {
  zh: {
    subject: '歡迎訂閱《讀懂非洲》｜Victor Tseng 曾浩瑜',
    hi: n => (n ? n + '，你好：' : '你好：'),
    lines: [
      '謝謝你訂閱《讀懂非洲》通訊，我已經收到你的資料。',
      '之後「讀懂非洲」專欄有新文章上線時，我會寄信通知你，內容涵蓋非洲藝術與品味、生活風格、跨文化溝通，以及非洲商業與市場。',
      '在等下一封信的同時，歡迎先逛逛專欄：'
    ],
    cta: '閱讀「讀懂非洲」專欄', url: 'https://victseng.com/notes/',
    topics: '你選擇的主題：',
    unsub: '不想再收到信？直接回覆這封信，寫「取消訂閱」就可以。',
    sign: 'Victor Tseng 曾浩瑜<br>跨文化市場開發顧問・駐點阿比讓'
  },
  en: {
    subject: 'Welcome to the Reading Africa letter | Victor Tseng',
    hi: n => (n ? 'Hi ' + n + ',' : 'Hi,'),
    lines: [
      'Thank you for subscribing to the Reading Africa letter. Your details are safely received.',
      'I will email you when a new article goes live in the column, covering African art and taste, lifestyle, cross-cultural communication, and African business and markets.',
      'While you wait for the next letter, feel free to explore the column:'
    ],
    cta: 'Read the Reading Africa column', url: 'https://victseng.com/en/notes/',
    topics: 'Topics you chose:',
    unsub: 'Don\'t want these emails? Just reply with "unsubscribe".',
    sign: 'Victor Tseng<br>Cross-cultural market development · Based in Abidjan'
  },
  fr: {
    subject: 'Bienvenue dans la lettre « Lire l\'Afrique » | Victor Tseng',
    hi: n => (n ? 'Bonjour ' + n + ',' : 'Bonjour,'),
    lines: [
      'Merci de votre inscription à la lettre « Lire l\'Afrique ». J\'ai bien reçu vos informations.',
      'Je vous écrirai à chaque nouvelle chronique : art africain et goût, art de vivre, communication interculturelle, business et marchés africains.',
      'En attendant la prochaine lettre, découvrez les chroniques :'
    ],
    cta: 'Lire les chroniques', url: 'https://victseng.com/fr/notes/',
    topics: 'Vos thèmes :',
    unsub: 'Vous ne souhaitez plus recevoir ces e-mails ? Répondez simplement « désinscription ».',
    sign: 'Victor Tseng<br>Développement de marchés · Interculturel · Basé à Abidjan'
  }
};

function doPost(e) {
  const p = e.parameter || {};
  if (p._honey) return out({ ok: true });            // 機器人陷阱
  if (!p.email) return out({ ok: false, error: 'missing email' });
  const sheet = SpreadsheetApp.getActiveSpreadsheet().getSheets()[0];
  const topics = (e.parameters && e.parameters.topics) ? e.parameters.topics.join(', ') : (p.topics || '');
  const lang = WELCOME[p.language] ? p.language : 'zh';
  sheet.appendRow([new Date(), p.name || '', p.email, p.role || '', p.company || '', topics, lang, p.page || '']);

  // 通知你
  MailApp.sendEmail(NOTIFY, '【victseng.com】新訂閱：' + (p.name || p.email),
    '稱呼：' + (p.name || '') + '\nEmail：' + p.email + '\n身分：' + (p.role || '') + '\n公司：' + (p.company || '') +
    '\n主題：' + topics + '\n語言：' + lang + '\n頁面：' + (p.page || ''));

  // 歡迎確認信給訂閱者（依語言）
  try { sendWelcome(p.email, p.name || '', topics, lang); } catch (err) { console.error(err); }
  return out({ ok: true });
}

function sendWelcome(to, name, topics, lang) {
  const w = WELCOME[lang];
  const esc = s => String(s).replace(/[&<>"]/g, c => ({ '&': '&amp;', '<': '&lt;', '>': '&gt;', '"': '&quot;' }[c]));
  const html =
    '<div style="background:#F4EFE7;padding:32px 16px;font-family:Georgia,\'Noto Serif TC\',serif;color:#161412">' +
    '<div style="max-width:560px;margin:0 auto;background:#FBF8F3;border:1px solid #E3DACB;padding:36px 32px">' +
    '<p style="letter-spacing:6px;font:13px Arial,sans-serif;margin:0 0 28px">VICTOR TSENG</p>' +
    '<p style="font-size:17px;margin:0 0 18px">' + esc(w.hi(name)) + '</p>' +
    w.lines.map(l => '<p style="font-size:15px;line-height:1.8;margin:0 0 14px">' + esc(l) + '</p>').join('') +
    (topics ? '<p style="font-size:13px;color:#7C7266;margin:0 0 20px">' + esc(w.topics) + ' ' + esc(topics) + '</p>' : '') +
    '<p style="margin:24px 0 30px"><a href="' + w.url + '?utm_source=newsletter&utm_medium=email&utm_campaign=welcome" ' +
    'style="background:#161412;color:#F4EFE7;text-decoration:none;padding:14px 22px;font:13px Arial,sans-serif;letter-spacing:2px">' +
    esc(w.cta) + ' →</a></p>' +
    '<p style="font-size:14px;line-height:1.7;margin:0 0 24px">' + w.sign + '</p>' +
    '<p style="font-size:12px;color:#9A9083;border-top:1px solid #E3DACB;padding-top:16px;margin:0">' + esc(w.unsub) + '</p>' +
    '</div></div>';
  const text = w.hi(name) + '\n\n' + w.lines.join('\n') + '\n' + w.url + '\n\n' + w.sign.replace('<br>', '\n') + '\n\n' + w.unsub;
  MailApp.sendEmail({ to: to, subject: w.subject, body: text, htmlBody: html, name: 'Victor Tseng', replyTo: NOTIFY });
}

function out(obj) {
  return ContentService.createTextOutput(JSON.stringify(obj)).setMimeType(ContentService.MimeType.JSON);
}
