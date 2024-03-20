window.onload = function() {
    var stars = document.querySelectorAll('.star');
    stars.forEach(function(star) {
        var duration = Math.random() * (1.5 - 0.5) + 0.5;
        var angle = Math.random() * (360 - 0) + 0;
        star.style.animationDuration = duration + 's';
        star.style.animationDelay = Math.random() + 's';
        star.style.transformOrigin = '0 0';
        star.style.transform = 'rotate(' + angle + 'deg)';
    });
};
