exports = async function(changeEvent){
  const {fullDocument} = changeEvent;
  const { _id, oracle_id, oracle_text, name, type_line, released_at, image_uris, card_faces} = fullDocument;
  console.log(_id)
  console.log(name);
  let funcResult = {"insert":0, "update":0}
  const info = context.functions.execute("ParseColour", fullDocument);
  const db = context.services.get("CardCluster").db("CardDB");
  const binderCollection = db.collection("Binders");
  const position =  await context.functions.execute("get_volume_page_row", fullDocument);
  let binderDoc = {
    "name": name,
    "oracle_id": oracle_id,
    "oracle_text": oracle_text,
    "type_line": type_line,
    "release_date": released_at,
    "default_image_uris": image_uris,
    "colours": info.colours,
    "copies": [],
    "binder":info.binder,
    "row": position.row,
    "page": position.page,
    "volume": position.volume
  };
  if ("card_faces" in fullDocument)
  {
    //physical cards can only have 2 faces
    binderDoc.oracle_text = [card_faces[0].oracle_text, card_faces[1].oracle_text]
    
  }
  if(info.binder == "Monocolour" ||info.binder == "Enemy" || info.binder == "Ally"){
    const infoCollection = db.collection("BinderInfo")
    const binderInfo = await infoCollection.findOne({name:info.binder}).catch(err => console.error("Failed to find record:", err));
    const position =  binderInfo.order.indexOf(info.colours) 
    // if not found add to back. special case for triomes
    binderDoc["order"] = position == -1 ?  binderInfo.order.length : position
  }
  const binderResult = await binderCollection.insertOne(binderDoc).catch(err => console.error("Failed to insert record:", err));
  funcResult.insert = 1;

  console.log(binderResult.insertedId)
  const landCollection = db.collection("Lands");
  const landResult = await landCollection.updateOne({"_id":_id}, { $set: {"binder": info.binder, "binder_id": binderResult._id } }).catch(err => console.error("Failed to update record:", err));
  funcResult.update = 1;

  console.log(`inserted ${name} into ${info.binder} collection`);
  
  return funcResult
  
//need better error handling
}
