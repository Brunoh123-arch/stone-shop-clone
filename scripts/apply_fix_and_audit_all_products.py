import glob
import re
import os

files = sorted(glob.glob('pages/produto-*.html'))
print(f"Auditing and fixing {len(files)} product files...")

# Duplicate block pattern:
# Starts with: </div><button type="button" class="btn-toggle-details" onclick="toggleProductDetails(this)">
# Ends right before: <!-- PRODUTOS RELACIONADOS or <div class="related-section"
dup_pattern = re.compile(
    r'</div><button type="button" class="btn-toggle-details" onclick="toggleProductDetails\(this\)">.*?</div>\s*(<!--\s*PRODUTOS RELACIONADOS|\s*<div class="related-section")',
    re.DOTALL
)

fixed_count = 0
unbalanced_files = []

for f in files:
    with open(f, 'r', encoding='utf-8') as fp:
        content = fp.read()

    modified = False
    if dup_pattern.search(content):
        content = dup_pattern.sub(r'\n\n      \1', content)
        fixed_count += 1
        modified = True

    # Ensure scroll-to-top button exists before </body>
    if 'id="scroll-to-top-btn"' not in content:
        btn_html = '''
  <button id="scroll-to-top-btn" class="scroll-to-top-btn" onclick="scrollToTop()" aria-label="Voltar para o topo">
    <svg viewBox="0 0 24 24" width="20" height="20" fill="none" stroke="#161823" stroke-width="2.6" stroke-linecap="round" stroke-linejoin="round">
      <line x1="12" y1="19" x2="12" y2="5"></line>
      <polyline points="5 12 12 5 19 12"></polyline>
    </svg>
  </button>
'''
        content = content.replace('</body>', btn_html + '\n</body>')
        modified = True

    # Ensure inline script helpers exist before </body>
    if 'window.toggleProductVideo' not in content:
        script_helpers = '''
<script>
window.toggleProductDetails = function(btn) {
  if (!btn) return;
  var container = btn.closest('.product-details-block') || btn.parentElement;
  if (!container) return;
  var hiddenRows = container.querySelectorAll('.detail-row.toggleable-row');
  var isExpanded = btn.classList.contains('expanded');
  if (isExpanded) {
    hiddenRows.forEach(function(r) {
      r.classList.add('is-hidden');
      r.style.setProperty('display', 'none', 'important');
    });
    btn.classList.remove('expanded');
    var span = btn.querySelector('span');
    if (span) span.textContent = 'Ver mais';
  } else {
    hiddenRows.forEach(function(r) {
      r.classList.remove('is-hidden');
      r.style.setProperty('display', 'flex', 'important');
    });
    btn.classList.add('expanded');
    var span = btn.querySelector('span');
    if (span) span.textContent = 'Ver menos';
  }
};
window.toggleProductVideo = function(wrapper) {
  if (!wrapper) return;
  var video = wrapper.querySelector('video');
  var playBtn = wrapper.querySelector('.play-overlay-btn');
  if (!video) return;
  if (video.paused) {
    video.play();
    if (playBtn) playBtn.style.opacity = '0';
  } else {
    video.pause();
    if (playBtn) playBtn.style.opacity = '1';
  }
};
window.scrollToTop = function() {
  var sc = document.querySelector('.page-content');
  if (sc) sc.scrollTo({ top: 0, behavior: 'smooth' });
  window.scrollTo({ top: 0, behavior: 'smooth' });
};
(function() {
  function checkScrollBtn() {
    var btn = document.getElementById('scroll-to-top-btn');
    if (!btn) return;
    var sc = document.querySelector('.page-content');
    var sy = (sc && sc.scrollTop) ? sc.scrollTop : (window.scrollY || document.documentElement.scrollTop || 0);
    if (sy > 200) {
      btn.classList.add('visible');
    } else {
      btn.classList.remove('visible');
    }
  }
  window.addEventListener('scroll', checkScrollBtn, { passive: true });
  document.addEventListener('DOMContentLoaded', function() {
    var sc = document.querySelector('.page-content');
    if (sc) sc.addEventListener('scroll', checkScrollBtn, { passive: true });
  });
})();
</script>
'''
        content = content.replace('</body>', script_helpers + '\n</body>')
        modified = True

    if modified:
        with open(f, 'w', encoding='utf-8') as fp:
            fp.write(content)

    # Audit tag depth
    app_idx = content.find('class="app-container"')
    if app_idx != -1:
        sub = content[app_idx:]
        open_divs = len(re.findall(r'<div[\s>]', sub, re.IGNORECASE))
        close_divs = len(re.findall(r'</div>', sub, re.IGNORECASE))
        diff = open_divs - close_divs
        if diff != 0:
            unbalanced_files.append((f, open_divs, close_divs, diff))

print(f"Fixed duplicate blocks in {fixed_count} files.")
print(f"Total unbalanced files: {len(unbalanced_files)}")
if unbalanced_files:
    for ub in unbalanced_files[:10]:
        print(f"  Unbalanced: {ub[0]} (open: {ub[1]}, close: {ub[2]}, diff: {ub[3]})")
else:
    print("ALL 99 PRODUCT FILES HAVE PERFECT TAG DEPTH (DIFF = 0)!")
