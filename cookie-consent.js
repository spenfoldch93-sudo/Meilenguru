(function () {
  var STORAGE_KEY = "meilenguru-consent";
  var stored = localStorage.getItem(STORAGE_KEY);

  if (stored === "granted") {
    gtag("consent", "update", { analytics_storage: "granted" });
    return;
  }
  if (stored === "denied") {
    return;
  }

  var isDe = (document.documentElement.lang || "").indexOf("de") === 0;
  var copy = isDe
    ? {
        text: "Wir verwenden Google Analytics, um zu verstehen, wie Besucher unsere Seite nutzen. Ohne deine Zustimmung werden keine Analyse-Cookies gesetzt.",
        privacy: "Datenschutz",
        privacyHref: "datenschutz",
        accept: "Akzeptieren",
        decline: "Ablehnen",
      }
    : {
        text: "We use Google Analytics to understand how visitors use this site. No analytics cookies are set without your consent.",
        privacy: "Privacy Policy",
        privacyHref: "privacy-policy",
        accept: "Accept",
        decline: "Decline",
      };

  var banner = document.createElement("div");
  banner.setAttribute("role", "dialog");
  banner.setAttribute("aria-label", copy.text);
  banner.style.cssText =
    "position:fixed;left:0;right:0;bottom:0;z-index:9999;background:#0a0a0a;color:#faf9f7;" +
    'font-family:"DM Sans",sans-serif;font-size:0.85rem;padding:1rem 1.25rem;' +
    "display:flex;flex-wrap:wrap;align-items:center;justify-content:center;gap:1rem;" +
    "box-shadow:0 -2px 12px rgba(0,0,0,0.15);";

  banner.innerHTML =
    '<span style="max-width:560px;line-height:1.5;">' +
    copy.text +
    ' <a href="' +
    copy.privacyHref +
    '" style="color:#d4ae4e;text-decoration:underline;">' +
    copy.privacy +
    "</a></span>" +
    '<span style="display:flex;gap:0.6rem;flex-shrink:0;">' +
    '<button type="button" data-consent="decline" style="background:transparent;color:#faf9f7;border:0.5px solid #888580;padding:0.5rem 1rem;font-family:inherit;font-size:0.8rem;cursor:pointer;">' +
    copy.decline +
    "</button>" +
    '<button type="button" data-consent="accept" style="background:#b8962e;color:#0a0a0a;border:none;padding:0.5rem 1rem;font-family:inherit;font-size:0.8rem;font-weight:500;cursor:pointer;">' +
    copy.accept +
    "</button>" +
    "</span>";

  document.body.appendChild(banner);

  banner.addEventListener("click", function (e) {
    var action = e.target.getAttribute("data-consent");
    if (!action) return;
    if (action === "accept") {
      localStorage.setItem(STORAGE_KEY, "granted");
      gtag("consent", "update", { analytics_storage: "granted" });
    } else {
      localStorage.setItem(STORAGE_KEY, "denied");
    }
    banner.remove();
  });
})();
