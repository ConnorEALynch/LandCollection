window.addEventListener('load', () => {
    $( ".header-menu-button-container" ).on( "click",  function(e){
       $(".mobile-nav").toggle();
    }); 
});