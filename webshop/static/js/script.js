/********************************************************
 *
 * Custom Javascript code for Enkel Bootstrap theme
 * Written by Themelize.me (http://themelize.me)
 *
 *******************************************************/
$(document).ready(function() {
  var defaultColour = 'orange';

  //IE placeholders
  $('[placeholder]').focus(function() {
    var input = $(this);
    if (input.val() == input.attr('placeholder')) {
      if (this.originalType) {
        this.type = this.originalType;
        delete this.originalType;
      }
      input.val('');
      input.removeClass('placeholder');
    }
  }).blur(function() {
    var input = $(this);
    if (input.val() == '') {
      input.addClass('placeholder');
      input.val(input.attr('placeholder'));
    }
  }).blur();

  //Bootstrap tooltip
  // invoke by adding _tooltip to a tags (this makes it validate)
  $('body').tooltip({
    selector: "a[class*=_tooltip]"
  });

  //Bootstrap popover
  // invoke by adding _popover to a tags (this makes it validate)
  $('body').popover({
    selector: "a[class*=_popover]",
    trigger: "hover"
  });

  //Scroll Top link
  $(window).scroll(function(){
    if ($(this).scrollTop() > 100) {
      $('.scrolltop').fadeIn();
    } else {
      $('.scrolltop').fadeOut();
    }
  });

  $('.scrolltop').click(function(){
    $("html, body").animate({
      scrollTop: 0
    }, 600);
    return false;
  });

  //show hide elements
  $('.show-hide').each(function() {
    $(this).click(function() {
      var state = 'open'; //assume target is closed & needs opening
      var target = $(this).attr('data-target');
      var targetState = $(this).attr('data-target-state');

      //allows trigger link to say target is open & should be closed
      if (typeof targetState !== 'undefined' && targetState !== false) {
        state = targetState;
      }

      if (state == 'undefined') {
        state = 'open';
      }

      $(target).toggleClass('show-hide-'+ state);
      $(this).toggleClass(state);
    });
  });

  //make current background active in switcher
  if ($('.switcher a.background').size() > 0) {
    var bgActive = $('#background-wrapper').attr('class');
    $('.switcher a.background').removeClass('active');
    $('.switcher a.'+ bgActive).addClass('active');
  }

  //background & colour switch
  $('.switcher a').click(function() {
    var c = $(this).attr('href').replace('#','');

    //colours
    if ($(this).hasClass('colour')) {
      if (c != defaultColour) {
        $('#colour-scheme').attr('href','css/colour-'+ c +'.css');
      }
      else {
        $('#colour-scheme').attr('href', '#');
      }

      $('.switcher a.colour').removeClass('active');
    }

    //backgrounds
    if ($(this).hasClass('background')) {
      $('#background-wrapper').removeClass();
      $('#background-wrapper').addClass(c);
      $('.switcher a.background').removeClass('active');
    }

    $('.switcher a.'+ c).addClass('active');
  });

  //flexslider
  $('.flexslider').each(function(i) {
    var currentFlexslider = $(this).attr('id', 'flexslider-'+ i);

    var sliderSettings =  {
      id: 'flexslider-'+ i,
      animation: $(this).data('transition'),
      selector: ".slides > .slide",
      controlNav: true,
      smoothHeight: true,
      start: function(slider) {
        //animate in first slide
        currentFlexslider.find('.slide').eq(1).addClass('animate-in');
      },
      before: function(slider) {
        //pause, animate out currentSlide, play
        currentFlexslider.find('.slide').eq(slider.currentSlide + 1).addClass('animate-out');
      },
      after: function(slider) {
        //remove animate-in & animate-out classes
        currentFlexslider.find('.slide').removeClass('animate-out animate-in');
        currentFlexslider.find('.slide').eq(slider.animatingTo + 1).addClass('animate-in');
      }
    };

    var sliderNav = $(this).data('slidernav');
    if (sliderNav != 'auto') {
      sliderSettings = $.extend({}, sliderSettings, {
        manualControls: sliderNav +' li a',
        controlsContainer: '.flexslider-wrapper'
      });
    }

    $(this).flexslider(sliderSettings);
  });

  //flexslider carousels
  $('.flexslider-carousel').each(function() {
    var carouselSettings =  {
      animation: "slide",
      animationLoop: false,
      selector: ".items > .item",
      itemWidth: $(this).data('item-width'),
      itemMargin: $(this).data('item-margin'),
      move: 1,
      controlNav: typeof $(this).data('item-controls-on') != 'undefined' ? true : false,
      slideshow: false
    };
    $(this).flexslider(carouselSettings);
  });

  //jQuery Quicksand plugin
  //@based on: http://www.evoluted.net/thinktank/web-development/jquery-quicksand-tutorial-filtering
  var $filters = $('#quicksand-categories');
  var $filterType = $filters.find('li.active a').attr('class');
  var $holder = $('ul#quicksand');
  var $data = $holder.clone();

  // react to filters being used
  $filters.find('li a').click(function(e) {
    $filters.find('li').removeClass('active');
    var $filterType = $(this).attr('class');
    $(this).parent().addClass('active');
    if ($filterType == 'all') {
      var $filteredData = $data.find('li');
    }
    else {
      var $filteredData = $data.find('li[data-type=' + $filterType + ']');
    }

    // call quicksand and assign transition parameters
    $holder.quicksand($filteredData, {
      duration: 800,
    });
    e.preventDefault();
  });

  //initialise Stellar.js
  $(window).stellar();

});