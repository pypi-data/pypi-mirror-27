var delayHide;

jQuery.fn.extend({
  showRichMenu: function() {
    var tab = $(this);
    var smenu = $(this).children('.smenu').not('.smenu.always');
    smenu.stop().clearQueue();
    tab.css('z-index', '300');
    tab.addClass('menuhover');
    smenu.animate({opacity: 1}, 100);
  },
  hideRichMenu: function() {
    var tab = $(this);
    var smenu = $(this).children('.smenu').not('.smenu.always');
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
  $("#portal-globalnav.hover > li").mouseenter(function(event){
    if ($('.plone-navbar-toggle').is(":visible")) return;
    event.stopPropagation();
    $("#portal-globalnav").find('.menuhover').not($(this).parents()).not($(this)).hideRichMenu();
    $(this).showRichMenu();
    clearTimeout( delayHide );
  });
  $("#portal-globalnav > li ul li").mouseenter(function(event){
    if ($('.plone-navbar-toggle').is(":visible")) return;
    event.stopPropagation();
    $("#portal-globalnav").find('.menuhover').not($(this).parents()).not($(this)).hideRichMenu();
    $(this).showRichMenu();
    clearTimeout( delayHide );
  });
  $("#portal-globalnav.hover").mouseleave(function(event){
    if ($('.plone-navbar-toggle').is(":visible")) return;
    delayHide = setTimeout( hideMenus, 300);
  });
  $("#portal-globalnav.hover .menuPage li").mouseleave(function(event){
    if ($('.plone-navbar-toggle').is(":visible")) return;
    $(this).hideRichMenu();
  });
  $("#portal-globalnav > li > a").click(function(event){
    if (!$('.plone-navbar-toggle').is(":visible") && !$("#portal-globalnav").hasClass('click')) return;
    if ($(this).parent().children().length == 1) return;
    event.preventDefault();
    event.stopPropagation();
    $("#portal-globalnav").find('.menuhover').not($(this).parents('li')).not($(this).parent()).hideRichMenu();
    $(this).parent().showRichMenu();
  });
  $('html').click(function(event) {
    delayHide = setTimeout( hideMenus, 300);
  });
};

$(initRichMenu);


// MOBILE MENU FOR Plone 4

var menu_gln = null;
var menu_min_limit = 768;
var windowwidth = null;

function menu_overflow() {
    if ($(window).width() == windowwidth) return;
    windowwidth = $(window).width();
    if ( $('#visual-portal-wrapper').innerWidth() < menu_min_limit ) {
        menu_gln.hide();
    } else {
        menu_gln.show();
    }
};

$(function(){
    menu_gln = $('#portal-globalnav');
    if (menu_gln.length == 0) return;
    if ($("#mobile_menu").length == 0) {
        $('#portal-globalnavWrapper').prepend('<div id="mobile_menu" class="plone-navbar-toggle"><span class="icon-bar"></span><span class="icon-bar"></span><span class="icon-bar"></span></div>');
    }
    menu_overflow();
    $(window).on('resize', menu_overflow);
    $("#mobile_menu").off('click').click(function(){
        menu_gln.toggle();
    });
});
