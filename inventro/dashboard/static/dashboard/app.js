/* Global app bootstrap */
document.addEventListener("DOMContentLoaded", () => {
  bootstrapEnableTooltips();
});

function bootstrapEnableTooltips() {
  if (!window.bootstrap) return;
  document
    .querySelectorAll('[data-bs-toggle="tooltip"]')
    .forEach((el) => new bootstrap.Tooltip(el));
}
