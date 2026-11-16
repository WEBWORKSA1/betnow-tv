/* BetNow.tv site configuration — edit values here, no other file needs changing. */
window.BN_CONFIG = {
  adsenseClient: "ca-pub-6620975821265271",
  /* Donation / support links. Paste your own payment links (PayPal.me, Buy Me a Coffee,
     Stripe Payment Link, Ko-fi, Patreon). Empty = button falls back to the pledge form. */
  donate: {
    paypal: "",       // e.g. "https://www.paypal.com/donate/?hosted_button_id=XXXX"
    buymeacoffee: "", // e.g. "https://www.buymeacoffee.com/yourname"
    stripe: "",       // e.g. "https://buy.stripe.com/xxxx"
    patreon: ""       // e.g. "https://www.patreon.com/yourname"
  },
  /* Support goal shown on the Support page */
  goal: { label: "Season fund: servers, data feeds, prizes & creators", target: 5000, raised: 0, currency: "USD" },
  /* Exit-intent popup: days before showing again */
  popupCooldownDays: 3
};
