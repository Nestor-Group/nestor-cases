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

}
if (document.readyState === 'loading') document.addEventListener('DOMContentLoaded', init); else init();
})();
