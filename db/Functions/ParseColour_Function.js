exports = function(arg){

  
    const { _id, oracle_id, rarity, produced_mana, color_identity, oracle_text, name, type_line, released_at, image_uris } = arg;

    const landToColor = {"Plains":"W","Island":"U", "Swamp":"B", "Mountain":"R","Forest":"G", "white":"W","blue":"U", "black":"B", "red":"R","green":"G" };

    //check rarity
    if (rarity.toLowerCase() == "uncommon" || rarity.toLowerCase() == "common"){
        console.log("common / uncommon");
        //this does not cover all cases like evolving wilds. solution will need to be revised
        return {"binder":"CommonUncommon",  "colours": produced_mana};
    }

    //now it gets difficult 
   
    let colours = [];
    //merge arrays and remove duplicates
    if(color_identity.length !== 0 || produced_mana){
         console.log("Merge arrays");
        colours = Array.from(new Set(produced_mana.concat(color_identity)));
    }
    else{
        console.log("parse from oracle text");
        //no easily identifiable colours. parse from oracle text
        for(const [key, value] of Object.entries(landToColor))
        {
            if(oracle_text.includes(key))
            {
                colours.push(value);
            }
        }
      
    }
    
    console.log(colours);

    
    const tempColours = colours.filter(function(value, index, arr){ 
        return value != "C";
    });
     //5 colour 
    if (tempColours.length >= 5){
        console.log("5 colours");
        console.log(tempColours);
        return {"binder":"5Colour",  "colours": ["W","U","B","R","G"] };
    }
    //mono colour
    if (tempColours.length === 1){
      console.log("mono");
      console.log(tempColours);
      return {"binder":"Monocolour", "colours": tempColours };
    }

    //colourless
    if (tempColours.length === 0){
        console.log("colourless");
        console.log(colours);
        return {"binder":"Colourless", "colours": ["C"]}; 
    }

    //5 colour again
    if (oracle_text.includes("a basic land card")){
        console.log("5 colour serach oracle text");
        return {"binder":"5Colour", "colours": ["W","U","B","R","G"]};
    }
    // 2/3 colour
    if(tempColours.length <= 3){
        //figure out which array to parse
        console.log(tempColours);
        
        const alignment = parseAllyEnemyColour(tempColours);
        return {"binder":alignment,"colours":tempColours.sort()};
    }

    console.log("Unsorted");
    return {"binder":"Unsorted"};


}

function parseAllyEnemyColour(colours)
{
    var colourWheel = new Circular(["W","U","B", "R", "G"]);
    let consecutive = 0;
    while (!colours.includes(colourWheel.current())){
        colourWheel.next();
    }
    console.log("found begining of colour wheel");
    consecutive++;
    
    if (colours.includes(colourWheel.prev())){
      consecutive++;
      if (colours.includes(colourWheel.prev())){
        consecutive++;
      }
      colourWheel.next();
    }
    colourWheel.next();
    if (colours.includes(colourWheel.next())){
      consecutive++;
      if (colours.includes(colourWheel.next())){
        consecutive++;
      }
    }
   
    if (consecutive >= colours.length){
       console.log("Ally");
      return "Ally";
    }
    else
     { 
          console.log("Enemy");
            return "Enemy";
    }
   
}

/**
 * shamelessly stolen from https://gist.github.com/ahmed-musallam/a8792eb488f8ef15e812c0680ea4a4a8
 * A simple circular data structure
 */
function Circular(arr, startIntex){
  this.arr = arr;
  this.currentIndex = startIntex || 0;
}

Circular.prototype.next = function(){
  var i = this.currentIndex, arr = this.arr;
  this.currentIndex = i < arr.length-1 ? i+1 : 0;
  return this.current();
};

Circular.prototype.prev = function(){
  var i = this.currentIndex, arr = this.arr;
  this.currentIndex = i > 0 ? i-1 : arr.length-1;
  return this.current();
};

Circular.prototype.current = function(){
  return this.arr[this.currentIndex];
};