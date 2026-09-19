// Phóng to duy nhất 1 bức ảnh (Image Lightbox)
function openLightbox(imgSrc, imgAlt) {
  const lb = document.getElementById('image-lightbox');
  const img = document.getElementById('lightbox-img');
  if (!lb || !img) return;
  const src = (typeof imgSrc === 'string') ? imgSrc : (imgSrc && imgSrc.src ? imgSrc.src : '');
  const alt = imgAlt || (imgSrc && imgSrc.alt) || '';
  img.src = src;
  img.alt = alt;
  const caption = document.getElementById('lightbox-caption');
  if (caption) caption.textContent = alt;
  lb.classList.add('active');
  document.body.style.overflow = 'hidden';
}

function closeLightbox() {
  const lb = document.getElementById('image-lightbox');
  if (lb) lb.classList.remove('active');
  document.body.style.overflow = '';
}

// Chuyển slide banner hero & sự kiện bàn phím Escape
document.addEventListener('DOMContentLoaded', () => {
  const slides = document.querySelectorAll('.hero-slide');
  const dots = document.querySelectorAll('.dot');
  let current = 0;
  const showSlide = (idx) => {
    current = idx;
    slides.forEach((s, i) => s.classList.toggle('active', i === current));
    dots.forEach((d, i) => d.classList.toggle('active', i === current));
  };
  dots.forEach((dot, i) => dot.onclick = () => showSlide(i));
  if (slides.length > 1) setInterval(() => showSlide((current + 1) % slides.length), 5000);
  document.addEventListener('keydown', (e) => { if (e.key === 'Escape') closeLightbox(); });
});
