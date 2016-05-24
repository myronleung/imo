$(function() {

  var navOffset = jQuery("nav-wrapper").offset().top;

  jQuery("nav-wrapper").wrap('<div class = "nav-placeholder"></div>');
  jQuery(".nav-placeholder").height(jQuery("nav-wrapper").outerheight();

  jQuery("nav").wrapInner()

  jQuery(window).scroll(function() {
    var scrollPos = jQuery(window).scrollTop();

    if(scrollPos >= navOffset) {
      jQuery("nav-wrapper").addClass("fixed")
    } else {
      jQuery("nav-wrapper").removeClass("fixed")
    }
});
