exports = async function(changeEvent) {
    
    //console.log(JSON.stringify(changeEvent.fullDocument));
    const { fullDocument: {id, name, reprint, oracle_id }} = changeEvent;
    
    
    //find if card has been printed before and give it the same binder position

    const db = context.services.get("CardCluster").db("CardDB");
    const collection = db.collection("Lands");
    const doc = await collection.findOne({"oracle_id": oracle_id,"id":{$ne: id}}).catch(err => console.error("Failed to find record:", err));
    if (doc){
      console.log(name + " found")
      const result = await collection.updateOne({"id":id}, { $set: {"binder":doc.binder, "binder_id":doc.binder_id}}).catch(err => console.error("Failed to update record:", err));
        return "found";
    }
    
    console.log(name + " not found")
    return "not found"
};
