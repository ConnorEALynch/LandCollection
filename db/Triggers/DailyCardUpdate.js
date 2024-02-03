exports = async function() {

  let currentDate = new Date();
  let docsInserted = 0;
  const query = "-type:token -type:basic type:land game:paper date="+currentDate.toISOString().split('T')[0];
  var ScryfallQuery = {"q":[query], "include_extras":["true"], "order":["released"], "unique":["prints"],"language":["all"]};
  console.log("Scryfall API params: "+JSON.stringify(ScryfallQuery));

  const response = await context.http.get({ scheme:"https",host:"api.scryfall.com",path:"/cards/search",query:ScryfallQuery}).catch(err => console.error("Error Making GET call to API", err));
  

  switch(response.statusCode){
    
    case 200:
      // The response body is a BSON.Binary object. Parse it and return.
      const data =  EJSON.parse(response.body.text()).data 
      data.forEach( obj => renameKey( obj, 'id', '_id' ) );
      console.log(`${data.length} new cards`);
      const db = context.services.get("CardCluster").db("CardDB");
      const collection = db.collection("Lands");
     
     try{
  	  const result = await collection.insertMany(data, {ordered:false})
  	  docsInserted = result.insertedIds.length;
     }
     catch(err){
     //cannot parse full error object
     //docsInserted = err.nInserted;
      console.error("Failed to insert records:",err);
      
     }
  	  break;
  	  
	  case 404:
	    console.log("No new cards");
	    break;
	    
    default:
      console.error("bad repsonse from API");
  }
  

  console.log(`${docsInserted} documents were inserted`);
  return docsInserted;
 
  
};

function renameKey ( obj, oldKey, newKey ) {
  obj[newKey] = obj[oldKey];
  delete obj[oldKey];
}

//make function to convert string time into date object
