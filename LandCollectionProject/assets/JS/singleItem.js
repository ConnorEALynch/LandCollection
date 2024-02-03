import Glide from '@glidejs/glide';



    function getCardDetails (id){
        $.ajax(
        {
            type:"GET",
            url: "/card/id/"+id,
            contentType: "application/json; charset=utf-8",
            data: { format: "json" },
            success: function( data ) 
            {
                var results = JSON.parse(data);
                
                $('.card-text-artist:not(.reserve-list)').text(`Illustrated by: ${results.artist}`);



                //flavour text one sided card
                if( results.hasOwnProperty('flavor_text'))
                {
                
                  $('.card-text-flavor').html(`<p>${results.flavor_text}</p>`)
                }

                //flavour text double sided card
                if( results.hasOwnProperty('card_faces'))
                {
                  var faces = results.card_faces;
                  if(faces[0].flavor_text){
                    $('.card-text-flavor').first().html(`<p>${faces[0].flavor_text}</p>`)
                  }
                  if(faces[1].flavor_text){
                  $('.card-text-flavor').last().html(`<p>${faces[1].flavor_text}</p>`)
                  }

                  if( faces[0].flavor_name)
                  {
                    $('.card-text-flavor-name').first().text(faces[0].flavor_name)
                    $('.card-text-flavor-name').last().text(faces[1].flavor_name)
                  }
                  else {
                    $('.card-text-flavor-name').empty()
                  }
                }



                if( results.hasOwnProperty('watermark'))
                {
                  if ($(".card-text-watermark").length) {
                    $(".card-text-watermark").text(`Watermark: ${results.watermark.charAt(0).toUpperCase() + results.watermark.slice(1)}`)               
                  }
                  else{
                    $(`<div class="card-text-watermark">Watermark: ${results.watermark.charAt(0).toUpperCase() + results.watermark.slice(1)}</div>`).insertBefore('.card-text-artist')
  
                  }
                }
                else {
                  $('.card-text-watermark').remove()
                }

                if( results.hasOwnProperty('flavor_name'))
                {
                  $('.card-text-flavor-name').text(results.flavor_name)
                }
                else {
                  $('.card-text-flavor-name').empty()
                }

              

                $('.prints-current-set-name').text(`${results.set_name} (${results.set.toUpperCase()})`)
                $('.prints-current-set-details').text(`#${results.collector_number} · ${results.rarity.charAt(0).toUpperCase() + results.rarity.slice(1)} · ${results.lang.toUpperCase()}`)
            }
         });
    };

   var glide = new Glide('.glide-card',{
        type: 'carousel',
       perView: 1,
       focousAt: 'center'
     });


     

window.addEventListener('load', () => {



    if($(".glide").length){
      glide.on(['mount.after','run.after'], function() {
          var id = $('.glide__slide--active').find('.card-image').data("id");
          getCardDetails(id);
        });
      
        glide.mount();
    }
    else{
      var id = $('.card-image').data("id");
      getCardDetails(id);
    }



    let params = (new URL(document.location)).searchParams;
    if(params.has("back")){
      $('div.card-image').addClass("flip-backside");
    }


    $("button").click( function(e){

      

      if (this.getAttribute("data-component") == "card-backface-button"){

        params = (new URL(document.location)).searchParams;
        
        if(params.has("back")){
          //will mess up other query params
          window.history.replaceState(null, null,  window.location.href.split("?")[0]);
        }
        else{
          window.history.replaceState(null,null, "?back");
        }

        $('.card-image').toggleClass("flip-backside")
      }
    
    });

});