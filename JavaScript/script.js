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

const symbolsList = [
  {symbol:"XAUUSD", name:"XAUUSD"},
  {symbol:"EURUSD", name:"EURUSD"},
  {symbol:"GBPUSD", name:"GBPUSD"},
  {symbol:"USDJPY", name:"USDJPY"},
  {symbol:"USDCHF", name:"USDCHF"},
];

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
      <td class="low">-</td>`
    ;
    tbody.appendChild(tr);
  });
}

async function updateMarket(){
  try{
    const res = await fetch("http://127.0.0.1:5002/prices");
    const data = await res.json();
    
    symbolsList.forEach(s=>{
      const row = document.querySelector(`tr[data-code="${s.symbol}"]`);
      if(!row) return;

      const priceCell = row.querySelector(".price");
      const changeCell = row.querySelector(".change");
      const highCell = row.querySelector(".high");
      const lowCell = row.querySelector(".low");

      const info = data[s.symbol];
      priceCell.textContent = info.price.toFixed(5);

      const arrowChange = info.change >=0 ? "▲" : "▼";
      changeCell.textContent =`${arrowChange} ${info.change.toFixed(5)}`;
      changeCell.className = "change " + (info.change>=0?"up":"down");

      highCell.innerHTML = `${info.high.toFixed(5)} <span class="up">▲</span>`;
      lowCell.innerHTML = `${info.low.toFixed(5)} <span class="down">▼</span>`;
    });

  }catch(err){
    console.error(err);
  }
}

// البداية
initTable();
setInterval(updateMarket,1000);

// البداية
initTable();
setInterval(updateMarket,1000);
// البداية
initTable();
setInterval(updateMarket,1000); // تحديث كل ثانية

// بداية
initTable();
setInterval(updateMarket,1000); // تحديث كل ثانية
// بدء التنفيذ
initTable();
updateMarket();
setInterval(updateMarket,15000); // تحديث كل 15 ثانية



// =================================

// JavaScript: ظهور العناصر بتأثير fade + slide
document.addEventListener('DOMContentLoaded', () => {
    const sections = document.querySelectorAll('section');

    const observerOptions = {
        root: null,
        rootMargin: '0px',
        threshold: 0.1
    };

    const observer = new IntersectionObserver((entries, observer) => {
        entries.forEach(entry => {
            if(entry.isIntersecting){
                entry.target.classList.add('show');

                // العناصر داخل القسم مع fade-slide تظهر بتأخير متتابع
                const elements = entry.target.querySelectorAll('.fade-slide');
                elements.forEach((el, index) => {
                    el.style.transitionDelay = `${index * 0.2}s`;
                    el.classList.add('show');
                });

                observer.unobserve(entry.target);
            }
        });
    }, observerOptions);

    sections.forEach(section => {
        observer.observe(section);
    });
});

// =================================


// =================================

// Progress Bar مع تغير الألوان حسب المنطقة
window.addEventListener('scroll', () => {
    const scrollTop = window.scrollY;
    const docHeight = document.documentElement.scrollHeight - window.innerHeight;
    const scrollPercent = (scrollTop / docHeight) * 100;

    const progressBar = document.getElementById('progress-bar');
    progressBar.style.width = scrollPercent + "%";

    // تغير اللون عند مناطق محددة
    if (scrollPercent < 25) {
        progressBar.style.background = "linear-gradient(to right, #1e90ff, #00ffcc)";
    } else if (scrollPercent < 50) {
        progressBar.style.background = "linear-gradient(to right, #ff7f50, #ff1493)";
    } else if (scrollPercent < 75) {
        progressBar.style.background = "linear-gradient(to right, #32cd32, #7fff00)";
    } else {
        progressBar.style.background = "linear-gradient(to right, #ff4500, #ffd700)";
    }
});

// =================================

// ================================

// زر العودة للأعلى
const scrollTopBtn = document.getElementById('scroll-top');

window.addEventListener('scroll', () => {
    if (window.scrollY > 200) {
        scrollTopBtn.style.display = 'block';
    } else {
        scrollTopBtn.style.display = 'none';
    }
});

// دالة ease-in للقفز التدريجي
function easeInQuad(t) {
    return t * t; // t من 0 إلى 1
}

// دالة التمرير للأعلى مع التأخير والسرعة التدريجية
function scrollToTopWithDelay(duration, delay) {
    const start = window.scrollY;
    const startTime = performance.now();

    function startScroll() {
        function scrollStep(currentTime) {
            const elapsed = currentTime - startTime;
            let t = Math.min(elapsed / duration, 1);
            t = easeInQuad(t); // تطبيق التسارع
            window.scrollTo(0, start * (1 - t));
            if (t < 1) {
                requestAnimationFrame(scrollStep);
            }
        }
        requestAnimationFrame(scrollStep);
    }

    // الانتظار قبل بدء الحركة
    setTimeout(startScroll, delay);
}

// عند الضغط على الزر
scrollTopBtn.addEventListener('click', (e) => {
    e.preventDefault();
    scrollToTopWithDelay(1000, 600); // duration=1000ms (1s)، delay=600ms
});

// ================================

