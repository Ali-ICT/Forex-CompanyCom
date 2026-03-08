// JS for hamburger 

const toggle = document.getElementById('menu-toggle');
const nav = document.getElementById('nav-list');

toggle.addEventListener('click', () => {
    nav.classList.toggle('show');
    toggle.classList.toggle('open'); // transform to X
});

// Hide nav if resized >770px
window.addEventListener('resize', () => {
    if(window.innerWidth > 770) {
        nav.classList.remove('show');
        toggle.classList.remove('open');
    }
});

const apiKey = "3a00424180694f64baaa23fda66c6a53"; // ضع مفتاح API الخاص بك هنا

// الرموز المحددة يدوياً
const symbolsList = [
  {symbol:"XAU/USD", name:"XAUUSD"},
  {symbol:"EUR/USD", name:"EURUSD"},
  {symbol:"GBP/USD", name:"GBPUSD"},
  {symbol:"USD/JPY", name:"USDJPY"},
  {symbol:"USD/CHF", name:"USDCHF"},
];

// إنشاء الجدول
function initTable(){
  const tbody = document.getElementById("marketTable");
  tbody.innerHTML = "";
  symbolsList.forEach(s=>{
    const tr = document.createElement("tr");
    tr.setAttribute("data-code", s.symbol);
    tr.innerHTML = `
      <td>${s.name}</td>
      <td class="price">-</td>
      <td class="change up">-</td>
      <td class="high">-</td>
      <td class="low">-</td>
    `
    tbody.appendChild(tr);
  });
}

// تحديث الأسعار live مع قيمة وهمية للـ Change
async function updateMarket(){
  for(let s of symbolsList){
    try{
      const res = await fetch(`https://api.twelvedata.com/quote?symbol=${s.symbol}&apikey=${apiKey}`);
      const data = await res.json();
      if(data.status === "error") continue;

      const row = document.querySelector(`tr[data-code="${s.symbol}"]`);
      const priceCell = row.querySelector(".price");
      const changeCell = row.querySelector(".change");
      const highCell = row.querySelector(".high");
      const lowCell = row.querySelector(".low");

      const price = parseFloat(data.close);
      priceCell.textContent = price.toFixed(2);

      // Change وهمي: ±2% تقريبا
      const fakeChangePercent = ((Math.random()*4)-2).toFixed(2);
      const arrowChange = fakeChangePercent >= 0 ? "▲" : "▼";
      changeCell.textContent = `${arrowChange} ${fakeChangePercent}%`;
      changeCell.className = "change " + (fakeChangePercent >= 0 ? "up" : "down");

      // High / Low مع سهم
      const high = parseFloat(data.high);
      const low = parseFloat(data.low);

      const highArrow = "▲";
      const lowArrow = "▼";

      highCell.innerHTML = `${high.toFixed(2)} <span class="up">${highArrow}</span>`;
      lowCell.innerHTML = `${low.toFixed(2)} <span class="down">${lowArrow}</span>`;

    } catch(err){
      console.error(Error `fetching ${s.symbol}: ${err.message}`);
    }
  }
}

// بدء التنفيذ
initTable();
updateMarket();
setInterval(updateMarket,15000); // تحديث كل 15 ثانية
