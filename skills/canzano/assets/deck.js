/* canzano deck. Fits the slides to the window, numbers them, and moves with the arrow keys. */
(function () {
  const deck = document.querySelector('.deck'), slides = [...deck.querySelectorAll('.slide')];
  slides.forEach(s => { s.dataset.total = String(slides.length).padStart(2, '0'); if (!s.dataset.label) s.dataset.label = deck.dataset.label || ''; });
  function fit() {
    const z = Math.min((innerWidth - 32) / 1280, (innerHeight - 32) / 720);
    deck.style.setProperty('--z', z);
    deck.style.setProperty('--x', Math.max(16, (innerWidth - 1280 * z) / 2) + 'px');
  }
  fit(); addEventListener('resize', fit);
  addEventListener('keydown', e => {
    const fwd = ['ArrowRight', 'ArrowDown', 'PageDown', ' '].includes(e.key), back = ['ArrowLeft', 'ArrowUp', 'PageUp'].includes(e.key);
    if (!fwd && !back) return;
    e.preventDefault();
    const cur = slides.findIndex(s => s.getBoundingClientRect().bottom > 24), to = slides[Math.max(0, Math.min(slides.length - 1, cur + (fwd ? 1 : -1)))];
    scrollTo({ top: to.getBoundingClientRect().top + scrollY - 16 });
  });
})();
