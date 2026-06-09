// Intercepts post/vote/comment/delete forms so the page updates in place
// instead of doing a full POST + reload. set_handle still reloads normally
// (it changes the session and most of the page).
//
// The server responds to these POSTs with a redirect back to the project
// page, so fetch() lands on the fresh full-page HTML. We parse it and swap
// just the regions that changed — no backend changes needed.

const AJAX_ACTIONS = [
  'vote', 'submit_idea', 'suggest_theme', 'comment', 'vote_comment',
  'delete_idea', 'delete_theme', 'delete_comment',
];
const SWAP_SELECTORS = ['.theme-grid', '#ideaList', '.votes-badge'];

// Brainstorm ripple: the electro effect spreads outward from the action
// point like a storm front — each card's animation is delayed by its
// distance from the origin.
function stormRipple(ox, oy) {
  document.querySelectorAll('.site-header, .card, .theme-card, .idea-item, .handle-bar')
    .forEach((el) => {
      const r = el.getBoundingClientRect();
      const dist = Math.hypot(r.left + r.width / 2 - ox, r.top + r.height / 2 - oy);
      el.style.animationDelay = `${Math.round(dist * 0.5)}ms`;
      el.classList.add('electro');
      el.addEventListener('animationend', () => {
        el.classList.remove('electro');
        el.style.animationDelay = '';
      }, { once: true });
    });
}

document.addEventListener('submit', async (e) => {
  const form = e.target;
  if (form.method.toLowerCase() !== 'post') return;
  const action = form.querySelector('input[name="action"]')?.value;
  if (!AJAX_ACTIONS.includes(action)) return;
  e.preventDefault();

  if (action.startsWith('delete_') && !confirm('Delete this post?')) return;

  // Capture the storm origin before the swap removes the form from the page
  const originRect = form.getBoundingClientRect();
  const ox = originRect.left + originRect.width / 2;
  const oy = originRect.top + originRect.height / 2;

  const themeId = form.querySelector('input[name="theme_id"]')?.value;
  const btn = form.querySelector('button[type="submit"]');
  if (btn) btn.disabled = true;

  try {
    const res = await fetch(window.location.href, {
      method: 'POST',
      body: new FormData(form),
    });
    const doc = new DOMParser().parseFromString(await res.text(), 'text/html');

    for (const sel of SWAP_SELECTORS) {
      const fresh = doc.querySelector(sel);
      const cur = document.querySelector(sel);
      if (fresh && cur) cur.replaceWith(fresh);
    }
    form.reset();

    // Keep the active team filter applied to the freshly swapped idea list
    document.querySelector('.filter-btn.active')?.click();

    stormRipple(ox, oy);

    // Extra-bright flash on the element that actually changed
    let target = null;
    if ((action === 'vote' || action === 'comment' || action === 'vote_comment') && themeId) {
      target = document.querySelector(`.theme-card[data-theme-id="${themeId}"]`);
    } else if (action === 'submit_idea') {
      target = document.querySelector('#ideaList .idea-item');
    } else if (action === 'suggest_theme') {
      // Themes sort newest-first
      target = document.querySelector('.theme-grid .theme-card:first-child');
    }
    if (target) target.classList.add('electro-epicenter');
    if (target) target.addEventListener('animationend', () => target.classList.remove('electro-epicenter'), { once: true });
  } catch (err) {
    // Network hiccup — fall back to the classic full submit
    form.submit();
  } finally {
    if (btn) btn.disabled = false;
  }
});
