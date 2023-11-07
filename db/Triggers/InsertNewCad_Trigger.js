exports = async function(changeEvent){
    const {fullDocument} = changeEvent;
    const { id, oracle_id, oracle_text, name, type_line, released_at, image_uris} = fullDocument;
    console.log(name);
    let funcResult = {"insert":0, "update":0}
    const info = context.functions.execute("ParseColour", fullDocument);
    const db = context.services.get("CardCluster").db("CardDB");
    const binderCollection = db.collection(info.binder);
    let binderDoc = {
      "name": name,
      "oracle_id": oracle_id,
      "oracle_text": oracle_text,
      "type_line": type_line,
      "release_date": released_at,
      "default_image_uris": image_uris, 
      "copies": []
    };
    if (info.hasOwnProperty('colours')){
      console.log("added colours to "+ name)
      binderDoc.colours = info.colours;
    }
      
    const binderResult = await binderCollection.insertOne(binderDoc).catch(err => console.error("Failed to insert record:", err));
    funcResult.insert = 1;

    const landCollection = db.collection("Lands");
    const landResult = await landCollection.updateOne({"id":id}, { $set: {"binder": info.binder, "binder_id": binderResult.insertedId } }).catch(err => console.error("Failed to update record:", err));
    funcResult.update = 1;

    console.log(`inserted ${name} into ${info.binder} collection`);
    
    return funcResult
    

}
