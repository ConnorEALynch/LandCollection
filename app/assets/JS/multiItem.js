import Glide from '@glidejs/glide';




window.addEventListener('load', () => {
    const carousels = document.querySelectorAll(".glide");

    Object.values(carousels).map(carousel => {
          const glide = new Glide(carousel, {
            type: 'slider',
            perView: 1,
            focousAt: 0
        });
        glide.mount();

    });

    $( "button" ).on( "click",  function(e){


        if (this.getAttribute("data-component") == "card-backface-button"){
            //toggle classs that flips card
            $(this).closest(".inner-flex").find(".card-image").toggleClass("flip-backside")
            
            //url parsing for query params
            const anchor =  $(this).closest(".inner-flex").find("a")
            const href = anchor.attr("href")
            var result = href
            const paramStart = href.indexOf("?")
            if (paramStart == -1){
            //no params
                result = href+"?back"
            }
            else {
                var params = new URLSearchParams(href.slice(paramStart))
  
                if (params.has("back"))
                {
                    params.delete("back")
                }
                else{
                    params.append("back")
                }
                const path = href.split("?")[0]
                result = params.size > 0 ? path +"?"+params.toString() : path
            }
            anchor.attr("href", result)
        }
      
      });
});


