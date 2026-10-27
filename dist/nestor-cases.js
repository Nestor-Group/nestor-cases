(function () {
function init() {
  var section = document.getElementById('nestor-cases');
  if (!section) return;

  /* ---- Media-locatie: data-media op de section (bv. "https://nestor.be/uploads/cases/") ---- */
  var mediaBase = section.getAttribute('data-media') || 'media/';
  if (!/\/$/.test(mediaBase)) mediaBase += '/';
  function mediaUrl(path) { return path.replace(/^media\//, mediaBase); }
  section.querySelectorAll('[data-src]').forEach(function (el) {
    el.setAttribute('src', mediaUrl(el.getAttribute('data-src')));
    el.removeAttribute('data-src');
  });

  /* ---- Carrousel (onder 1024px) ---- */
  var grid = section.querySelector('.nc__grid');
  var prev = section.querySelector('.nc__navbtn--prev');
  var next = section.querySelector('.nc__navbtn--next');

  var reduceMotion = window.matchMedia('(prefers-reduced-motion: reduce)').matches;

  function items() { return Array.prototype.slice.call(grid.querySelectorAll('.nc__item')); }
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
  updateNav();

  /* ---- Loop-video's op de videokaarten: spelen vanzelf (zonder geluid) zodra de kaart in beeld is ---- */
  var cards = section.querySelectorAll('.nc__card--video');

  function playLoop(card) {
    var loop = card.querySelector('.nc__loop');
    if (!loop) return;
    var p = loop.play();
    if (p && p.then) p.then(function () { card.classList.add('is-playing'); }).catch(function () {});
    else card.classList.add('is-playing');
  }
  function pauseLoop(card) {
    var loop = card.querySelector('.nc__loop');
    if (loop) loop.pause();
  }
  if (!reduceMotion) {
    if ('IntersectionObserver' in window) {
      var io = new IntersectionObserver(function (entries) {
        entries.forEach(function (e) { if (e.isIntersecting) playLoop(e.target); else pauseLoop(e.target); });
      }, { threshold: 0.2 });
      cards.forEach(function (card) { io.observe(card); });
    } else {
      cards.forEach(playLoop);
    }
  }

  cards.forEach(function (card) {
    card.addEventListener('click', function () { openModal(mediaUrl(card.dataset.video || ''), card.dataset.ratio); });
    card.addEventListener('keydown', function (e) {
      if (e.key === 'Enter' || e.key === ' ') { e.preventDefault(); openModal(mediaUrl(card.dataset.video || ''), card.dataset.ratio); }
    });
  });

  /* ---- Modal ---- */
  var modal = document.getElementById('nc-modal');
  /* De popup moet rechtstreeks onder <body> staan: een voorouder met transform (bv. een
     fade-in-animatie van de site) zou "position: fixed" anders ten opzichte van zichzelf plaatsen. */
  if (modal.parentElement !== document.body) document.body.appendChild(modal);
  var body = modal.querySelector('.nc-modal__body');
  var closeBtn = modal.querySelector('.nc-modal__close');
  var lastFocus = null;

  function embedUrl(url) {
    var yt = url.match(/(?:youtube\.com\/(?:watch\?v=|shorts\/|embed\/)|youtu\.be\/)([\w-]{6,})/);
    if (yt) return 'https://www.youtube-nocookie.com/embed/' + yt[1] + '?autoplay=1&rel=0';
    var vm = url.match(/vimeo\.com\/(?:video\/)?(\d+)/);
    if (vm) return 'https://player.vimeo.com/video/' + vm[1] + '?autoplay=1';
    return null;
  }

  function openModal(src, ratio) {
    lastFocus = document.activeElement;
    body.innerHTML = '';
    if (!src) {
      var p = document.createElement('p');
      p.className = 'nc-modal__empty';
      p.textContent = 'Video volgt.';
      body.appendChild(p);
    } else if (/\.(mp4|webm|mov)(\?|$)/i.test(src)) {
      var v = document.createElement('video');
      v.src = src; v.controls = true; v.autoplay = true; v.playsInline = true;
      body.appendChild(v);
    } else {
      var f = document.createElement('iframe');
      f.src = embedUrl(src) || src;
      f.allow = 'autoplay; fullscreen; picture-in-picture';
      f.setAttribute('allowfullscreen', '');
      if (ratio === '9/16') f.classList.add('is-portrait');
      body.appendChild(f);
    }
    modal.hidden = false;
    modal.classList.add('is-open');
    document.body.style.overflow = 'hidden';
    try { closeBtn.focus({ preventScroll: true }); } catch (e) { closeBtn.focus(); }
  }
  function closeModal() {
    modal.classList.remove('is-open');
    modal.hidden = true;
    body.innerHTML = '';
    document.body.style.overflow = '';
    if (lastFocus && lastFocus.focus) { try { lastFocus.focus({ preventScroll: true }); } catch (e) { lastFocus.focus(); } }
  }
  closeBtn.addEventListener('click', closeModal);
  modal.addEventListener('click', function (e) { if (e.target === modal) closeModal(); });
  document.addEventListener('keydown', function (e) { if (e.key === 'Escape' && modal.classList.contains('is-open')) closeModal(); });
}
if (document.readyState === 'loading') document.addEventListener('DOMContentLoaded', init); else init();
})();
