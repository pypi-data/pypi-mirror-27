// $Id:  $
// balade_nature

/*global jQuery: true */


jQuery(document).ready(function($) {
    // Hotspots
    var delay = 5000;
    $('.pdocHotspot').each(function() {
        var $hotspot = $(this);
        var $spot = $('#' + $hotspot.attr('id') + 's');
        var scenario = $hotspot.children('span').length;
        if ($spot.length && scenario) {
            $hotspot.css('opacity', 1);
            $hotspot.click(function() {
                if ($hotspot.css('opacity') == 1) {
                    $hotspot.animate({opacity: 0})
                        .delay(delay)
                        .animate({opacity: 1});
                    $spot.css({opacity: 0, display: 'block'})
                        .animate({opacity: 1})
                        .delay(delay)
                        .animate({opacity: 0}, function() {
                            $spot.css({opacity: '', display: ''});  
                        });
                } else {
                    $spot.click(); 
                }
            });

            $spot.click(function() {
                $spot.stop().animate({opacity: 0}, function() {
                    $spot.css({opacity: '', display: ''});  
                });
                $hotspot.stop().animate({opacity: 1});
            });
        }
    });

    // Effect: glow
    var boxProperty = '';
    var $text = null;
    var $spot = null;
    var $box = null;
    var $effectGlow = $('#effectGlow');
    if ($effectGlow.length) {
        $text = $('#effectGlowText');
        $spot = $('#effectGlowSpot');
        $box = $('#effectGlowBox');
        if (typeof $box.css('webkitBoxShadow') == 'string') {
            boxProperty = 'webkitBoxShadow';
        } else if (typeof $box.css('MozBoxShadow') == 'string') {
            boxProperty = 'MozBoxShadow';
        } else if (typeof $box.css('boxShadow') == 'string') {
            boxProperty = 'boxShadow';
        }
        $effectGlow.on('mousemove touchmove', onMouseMove);
    }

    function onMouseMove(e) {
        if (typeof e === 'undefined' || typeof e.clientX === 'undefined') {
            return;
        }
        
        var xm = (e.clientX - Math.floor(window.innerWidth / 2)) * 0.4;
        var ym = (e.clientY - Math.floor(window.innerHeight / 3)) * 0.4;
        var d = Math.round(Math.sqrt(xm*xm + ym*ym) / 5);
        $text.css('textShadow',  -xm + 'px ' + -ym + 'px ' + (d + 10) + 'px black');
        
        if (boxProperty) {
            $box.css(boxProperty, '0 ' + -ym + 'px ' + (d + 30) + 'px black');
        }
        
        xm = e.clientX - Math.floor(window.innerWidth / 2);
        ym = e.clientY - Math.floor(window.innerHeight / 2);
        $spot.css('backgroundPosition', xm + 'px ' + ym + 'px');
    }
});
