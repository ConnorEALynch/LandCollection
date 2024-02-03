exports = async function(arg){
  
    const {binder, item } = arg;
    let position = null;
    const db = context.services.get("CardCluster").db("CardDB");
    let  collection = db.collection("BinderInfo");
    const binderinfo = await collection.findOne({"name":binder}).catch(err => console.error("Failed to insert record:", err));
    collection = db.collection("Binders");
    const lastItem = await collection.find({"binders":binder, "colours":item.colours}).sort({"volume":-1,"page":-1,"row":-1}).limit(1);
    
      let volume = 1;
      let page = 1;
      let row = 1;
    
    if (lastItem != null) {
  
      let vol_max = binderInfo.pages;
      let page_max = binderInfo.items_per_page;
      let page_begining = 1;
      
  
      
      switch(binderInfo.sort){
        case "order":
          section = binderInfo.order.indexOf(item.colours);
          section_offset = Math.floor( page_max / binderInfo.order.length);
          page_begining = section * section_offset;
          page_begining ++;
          page_max = (section++) * section_offset;
          break;
          
        case "name":
          //item is in collection
          await context.function.execute('reorganoze_binder',binderInfo)
          position = await collection.find({"_id":item.id})
          break;
          
          
      }
      
       volume = lastItem.volume;
       page = lastItem.page;
       row = lastItem.row++;
  
      
      if(lastItem.row > page_max){
          row = 1;
          page ++;
      }
      
      if (lastItem.page > vol_max){
        volume++;
        page = page_begining;
        
      }
      if (position != null){
        row = position.row;
        page = position.page;
        volume = position.volume;
      }
  }
  
    return {"volume":volume, "page":page, "row":row};
  };