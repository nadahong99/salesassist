/* Global config cached after loadConfig() */
let _cfg = { naver_fee_rate: 0.06, coupang_fee_rate: 0.12, default_extra_cost: 0 };

document.addEventListener("DOMContentLoaded", () => {
  loadConfig();
  loadItems();
});

/* ===== Config ===== */

async function loadConfig() {
  const res = await fetch("/api/config");
  if (!res.ok) return;
  const data = await res.json();
  _cfg = data;
  document.getElementById("naver_fee").value = +(data.naver_fee_rate * 100).toFixed(4);
  document.getElementById("coupang_fee").value = +(data.coupang_fee_rate * 100).toFixed(4);
  document.getElementById("extra_cost").value = data.default_extra_cost;
}

async function saveConfig() {
  const naver_fee_rate = parseFloat(document.getElementById("naver_fee").value) / 100;
  const coupang_fee_rate = parseFloat(document.getElementById("coupang_fee").value) / 100;
  const default_extra_cost = parseFloat(document.getElementById("extra_cost").value) || 0;

  const res = await fetch("/api/config", {
    method: "PUT",
    headers: { "Content-Type": "application/json" },
    body: JSON.stringify({ naver_fee_rate, coupang_fee_rate, default_extra_cost }),
  });
  if (!res.ok) { alert("설정 저장 실패"); return; }
  _cfg = await res.json();
  alert("설정이 저장되었습니다.");
  loadItems();
}

/* ===== Items ===== */

async function loadItems() {
  const res = await fetch("/api/items");
  if (!res.ok) return;
  const items = await res.json();
  renderItems(items);
}

function calcMargin(item, feeRate) {
  const totalCost = item.cost_price + _cfg.default_extra_cost;
  const fee = item.sell_price * feeRate;
  const margin = item.sell_price - totalCost - fee;
  const rate = item.sell_price > 0 ? (margin / item.sell_price) * 100 : 0;
  return rate;
}

function marginClass(rate) {
  if (rate < 10) return "bad";
  if (rate < 20) return "mid";
  return "good";
}

function renderItems(items) {
  const tbody = document.getElementById("items-tbody");
  tbody.innerHTML = "";
  items.forEach((item) => {
    const naverRate = calcMargin(item, _cfg.naver_fee_rate);
    const coupangRate = calcMargin(item, _cfg.coupang_fee_rate);
    const tr = document.createElement("tr");
    tr.innerHTML = `
      <td>${item.id}</td>
      <td>${escHtml(item.name)}</td>
      <td>${escHtml(item.source)}</td>
      <td>${item.cost_price.toLocaleString()}</td>
      <td>${item.sell_price.toLocaleString()}</td>
      <td class="${marginClass(naverRate)}">${naverRate.toFixed(1)}%</td>
      <td class="${marginClass(coupangRate)}">${coupangRate.toFixed(1)}%</td>
      <td>${escHtml(item.option_text)}</td>
      <td>${escHtml(item.memo)}</td>
      <td>${item.url ? `<a href="${escHtml(item.url)}" target="_blank" rel="noopener">링크</a>` : ""}</td>
      <td>
        <button onclick="editItem(${item.id})">수정</button>
        <button onclick="deleteItem(${item.id})">삭제</button>
      </td>
    `;
    tbody.appendChild(tr);
  });
}

async function addItem() {
  const payload = {
    name: document.getElementById("f_name").value.trim(),
    source: document.getElementById("f_source").value.trim(),
    url: document.getElementById("f_url").value.trim(),
    cost_price: parseFloat(document.getElementById("f_cost").value) || 0,
    sell_price: parseFloat(document.getElementById("f_sell").value) || 0,
    option_text: document.getElementById("f_option").value.trim(),
    memo: document.getElementById("f_memo").value.trim(),
  };
  const res = await fetch("/api/items", {
    method: "POST",
    headers: { "Content-Type": "application/json" },
    body: JSON.stringify(payload),
  });
  if (!res.ok) { alert("상품 추가 실패"); return; }
  document.getElementById("add-form").reset();
  loadItems();
}

async function editItem(id) {
  const res = await fetch("/api/items");
  if (!res.ok) return;
  const items = await res.json();
  const item = items.find((i) => i.id === id);
  if (!item) return;

  const name = prompt("상품명:", item.name);
  if (name === null) return;
  const source = prompt("소싱처:", item.source);
  if (source === null) return;
  const url = prompt("소싱 URL:", item.url);
  if (url === null) return;
  const cost_price = prompt("원가:", item.cost_price);
  if (cost_price === null) return;
  const sell_price = prompt("판매가:", item.sell_price);
  if (sell_price === null) return;
  const option_text = prompt("옵션:", item.option_text);
  if (option_text === null) return;
  const memo = prompt("메모:", item.memo);
  if (memo === null) return;

  const payload = {
    name,
    source,
    url,
    cost_price: parseFloat(cost_price) || 0,
    sell_price: parseFloat(sell_price) || 0,
    option_text,
    memo,
  };
  const putRes = await fetch(`/api/items/${id}`, {
    method: "PUT",
    headers: { "Content-Type": "application/json" },
    body: JSON.stringify(payload),
  });
  if (!putRes.ok) { alert("수정 실패"); return; }
  loadItems();
}

async function deleteItem(id) {
  if (!confirm(`ID ${id} 상품을 삭제하시겠습니까?`)) return;
  const res = await fetch(`/api/items/${id}`, { method: "DELETE" });
  if (!res.ok) { alert("삭제 실패"); return; }
  loadItems();
}

/* ===== Export ===== */

async function exportNaver() {
  await downloadFile("/api/export/naver");
}

async function exportCoupang() {
  await downloadFile("/api/export/coupang");
}

async function downloadFile(url) {
  const res = await fetch(url);
  if (!res.ok) { alert("내보내기 실패"); return; }
  const blob = await res.blob();
  const disposition = res.headers.get("content-disposition") || "";
  let filename = "export.xlsx";
  const match = disposition.match(/filename[^;=\n]*=((['"]).*?\2|[^;\n]*)/);
  if (match) filename = match[1].replace(/['"]/g, "");
  const a = document.createElement("a");
  a.href = URL.createObjectURL(blob);
  a.download = filename;
  document.body.appendChild(a);
  a.click();
  a.remove();
  URL.revokeObjectURL(a.href);
}

/* ===== Utility ===== */

function escHtml(str) {
  if (!str) return "";
  return str
    .replace(/&/g, "&amp;")
    .replace(/</g, "&lt;")
    .replace(/>/g, "&gt;")
    .replace(/"/g, "&quot;");
}
