var _Cookielaw = {
  createCookie: function(name, value, days) {
    var date = new Date();
    var expires = "";
    if (days) {
      date.setTime(date.getTime() + (days * 24 * 60 * 60 * 1000));
      expires = "; expires=" + date.toGMTString();
    }
    document.cookie = name + "=" + value + expires + "; path=/";
  },

  accept: function() {
    this.createCookie('{{ legal_cookielaw_name }}', '1', 10 * 365);
    if (typeof (window.jQuery) === 'function') {
      jQuery('#{{ legal_cookielaw_banner_id }}').slideUp();
    } else {
      document.getElementById('{{ legal_cookielaw_banner_id }}').style.display = 'none';
    }
  }
};
