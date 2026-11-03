// victseng.com 電子報訂閱：把網站表單寫進這份試算表，並寄通知信給你
const NOTIFY = 'victseng.consult@gmail.com';

function doPost(e) {
  const p = e.parameter || {};
  if (p._honey) return out({ ok: true });            // 機器人陷阱
  if (!p.email) return out({ ok: false, error: 'missing email' });
  const sheet = SpreadsheetApp.getActiveSpreadsheet().getSheets()[0];
  const topics = (e.parameters && e.parameters.topics) ? e.parameters.topics.join(', ') : (p.topics || '');
  sheet.appendRow([new Date(), p.name || '', p.email, p.role || '', p.company || '', topics, p.language || '', p.page || '']);
  MailApp.sendEmail(NOTIFY, '【victseng.com】新訂閱：' + (p.name || p.email),
    '稱呼：' + (p.name || '') + '\nEmail：' + p.email + '\n身分：' + (p.role || '') + '\n公司：' + (p.company || '') +
    '\n主題：' + topics + '\n語言：' + (p.language || '') + '\n頁面：' + (p.page || ''));
  return out({ ok: true });
}

function out(obj) {
  return ContentService.createTextOutput(JSON.stringify(obj)).setMimeType(ContentService.MimeType.JSON);
}
