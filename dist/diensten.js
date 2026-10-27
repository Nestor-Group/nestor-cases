(function () {
function init() {
  var section = document.getElementById('nestor-diensten');
  if (!section) return;

  /* ---- Media-locatie: data-media op de section (voor eventuele afbeeldingen met data-src) ---- */
  var mediaBase = section.getAttribute('data-media') || 'media/';
  if (!/\/$/.test(mediaBase)) mediaBase += '/';
  section.querySelectorAll('[data-src]').forEach(function (el) {
    el.setAttribute('src', el.getAttribute('data-src').replace(/^media\//, mediaBase));
    el.removeAttribute('data-src');
  });

  /* ---- Carrousel (onder 640px containerbreedte) ---- */
  var grid = section.querySelector('.nd__grid');
  var prev = section.querySelector('.nd__navbtn--prev');
  var next = section.querySelector('.nd__navbtn--next');
  var reduceMotion = window.matchMedia('(prefers-reduced-motion: reduce)').matches;

  function items() { return Array.prototype.slice.call(grid.querySelectorAll('.nd__item')); }
  function gutter() { return parseFloat(getComputedStyle(grid).paddingLeft) || 0; }
  function itemLeft(item) {
    return item.getBoundingClientRect().left - grid.getBoundingClientRect().left + grid.scrollLeft - gutter();
  }
  function currentIndex() {
    var list = items(), idx = 0;
    for (var i = 0; i < list.length; i++) { if (itemLeft(list[i]) <= grid.scrollLeft + 2) idx = i; }
    return idx;
  }
  function goTo(i) {
    var list = items();
    i = Math.max(0, Math.min(list.length - 1, i));
    grid.scrollTo({ left: itemLeft(list[i]), behavior: reduceMotion ? 'auto' : 'smooth' });
  }
  function updateNav() {
    var max = grid.scrollWidth - grid.clientWidth - 1;
    prev.disabled = grid.scrollLeft <= 0;
    next.disabled = grid.scrollLeft >= max;
  }
  prev.addEventListener('click', function () { goTo(currentIndex() - 1); });
  next.addEventListener('click', function () { goTo(currentIndex() + 1); });
  grid.addEventListener('scroll', updateNav, { passive: true });
  window.addEventListener('resize', updateNav);
  if ('ResizeObserver' in window) new ResizeObserver(updateNav).observe(grid);   /* ook als alleen de container van breedte verandert */
  updateNav();
}
if (document.readyState === 'loading') document.addEventListener('DOMContentLoaded', init); else init();
})();
