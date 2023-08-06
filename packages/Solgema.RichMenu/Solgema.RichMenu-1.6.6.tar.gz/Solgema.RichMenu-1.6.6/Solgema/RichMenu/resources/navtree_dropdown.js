var delayHide;

jQuery.fn.extend({
  showRichMenu: function() {
    var tab = $(this);
    var smenu = $(this).children('.smenu').not('.smenu.always');;
    smenu.stop().clearQueue();
    tab.css('z-index', '300');
    tab.addClass('menuhover');
    smenu.animate({opacity: 1}, 100);
  },
  hideRichMenu: function() {
    var tab = $(this);
    var smenu = $(this).children('.smenu:visible').not('.smenu.always');;
    if (smenu.length>0){
      smenu.stop().clearQueue();
      tab.css('z-index', '200');
      smenu.animate({
        opacity: 0,
        }, 100, function() {
          tab.removeClass('menuhover');
      });
    } else {
      tab.removeClass('menuhover');
    }
  }
});

function hideMenus() {
  $("#portal-globalnav li").hideRichMenu();
}

function initRichMenu() {
  $("#portal-globalnav.hover li > .smenu").not('.smenu.always').css('opacity','0');
  $("#portal-globalnav.click li > .smenu").not('.smenu.always').css('opacity','0');
  $("#portal-globalnav.hover > li").on('mouseenter', function(event){
    if ($('.plone-navbar-toggle').is(":visible")) return;
    event.stopPropagation();
    $("#portal-globalnav").find('.menuhover').not($(this).parents()).not($(this)).hideRichMenu();
    $(this).showRichMenu();
    clearTimeout( delayHide );
  });
  $("#portal-globalnav > li ul li").on('mouseenter touchstart', function(event){
    if ($('.plone-navbar-toggle').is(":visible")) return;
    event.stopPropagation();
    $("#portal-globalnav").find('.menuhover').not($(this).parents()).not($(this)).hideRichMenu();
    $(this).showRichMenu();
    clearTimeout( delayHide );
  });
  $("#portal-globalnav.hover .menuPage li").on('mouseleave touchend', function(event){
    if ($('.plone-navbar-toggle').is(":visible")) return;
    $(this).hideRichMenu();
  });
  $("#portal-globalnav > li > a").on('click touchstart', function(event){
    if ($(this).parent().children().length == 1) return;
    if ($("#portal-globalnav").hasClass('hover') && event.type == 'touchstart') {
      event.stopPropagation();
      event.preventDefault();
      $("#portal-globalnav").find('.menuhover').not($(this).parent().parents()).not($(this).parent()).hideRichMenu();
      if ($(this).parent().find('ul').is(":visible")) {
        $(this).parent().hideRichMenu();
        return
      }
      $(this).parent().showRichMenu();
      clearTimeout( delayHide );
      return
    }
    if (!$('.plone-navbar-toggle').is(":visible") && !$("#portal-globalnav").hasClass('click')) {
      return;
    }
    event.preventDefault();
    event.stopPropagation();
    if (!$(this).parent().hasClass('menuhover')) {
        $("#portal-globalnav").find('.menuhover').not($(this).parents('li')).not($(this).parent()).hideRichMenu();
        $(this).parent().showRichMenu();
    } else {
        $(this).parent().hideRichMenu();
    }
  });
  $('html').click(function(event) {
    delayHide = setTimeout( hideMenus, 300);
  });
};

$(initRichMenu);
