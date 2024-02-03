exports = async function(arg){
    const db = context.services.get("CardCluster").db("CardDB");
    let collection = db.collection("BinderInfo");
    const info = await collection.find({}).toArray();
    collection = db.collection("Binders");
    let pipeline = null;
    let result = true;
    
    const mergeCol = 'Binders';
    const failOption = 'fail';


      for (const item of info){
      
      const per_page = item.items_per_page;
      const sort_order = item.order;
      let per_volume = null;
      let sort_length = null;

      
      switch(item.sort[0]){
     
      case "order":
        per_volume = item.pages;
        sort_length = item.order.length;
        pipeline = [{'$match': {'binder': item.name}}, {'$sort': {'order': 1, 'release_date': 1}}, {'$group': {'_id': '$order', 'entries': {'$push': {'_id': '$_id', 'colours': '$colours'}}}}, {'$sort': {'_id': 1}}, {'$unwind': {'path': '$entries', 'includeArrayIndex': 'indexOrder'}}, {'$project': {'_id': '$entries._id', 'colours': '$entries.colours', 'indexOrder': '$indexOrder', 'order': '$_id'}}, {'$set': {'row': {'$add': [{'$mod': ['$indexOrder', per_page]}, 1]}, 'page': {'$add': [{'$floor': {'$mod': [{'$divide': ['$indexOrder', per_page]}, {'$divide': [per_volume, per_page]}]}}, 1, {'$multiply': [{'$floor': {'$divide': [per_volume, sort_length]}}, '$order']}]}, 'volume': {'$add': [{'$floor': {'$divide': ['$indexOrder', {'$multiply': [{'$floor': {'$divide': [per_volume, sort_length]}}, per_page]}]}}, 1]}}}, {'$project': {'_id': 1, 'row': 1, 'page': 1, 'volume': 1}},{'$merge':{'into':mergeCol,'on':'_id','whenMatched':'merge','whenNotMatched':failOption}}];
        break;
      case "name":
        sort_length = item.order.length;
        pipeline = [{'$match':{'binder':item.name}},{'$sort':{'name':1,'release_date':1}},{'$bucket':{'groupBy':{'$substr':['$name',0,1]},'boundaries':sort_order,'output':{'entries':{'$push':{'_id':'$_id','name':'$name'}}}}},{'$unwind':{'path':'$entries','includeArrayIndex':'indexOrder'}},{'$project':{'_id':'$entries._id','indexOrder':1,'bucket':'$_id'}},{'$set':{'page':{'$add':['$indexOrder',1]},'volume':{'$add':[{'$indexOfArray':[sort_order,'$bucket']},1]}}},{'$unset': ['bucket', 'indexOrder']},{'$merge':{'into':mergeCol,'on':'_id','whenMatched':'merge','whenNotMatched':failOption}}]
        break;
      case "release_date":
        per_volume = item.pages;
        pipeline = [{'$match':{'binder': item.name}},{'$sort':{'release_date':1,'name':1}},{'$group':{'_id':{},'entries':{'$push':{'_id':'$_id'}}}},{'$unwind':{'path':'$entries','includeArrayIndex':'indexOrder'}},{'$project':{'_id':'$entries._id','colours':'$entries.colours','binder':'$entries.binder','indexOrder':1}},{'$set':{'row':{'$add':[{'$mod':['$indexOrder',per_page]},1]},'page':{'$add':[{'$floor':{'$mod':[{'$divide':['$indexOrder',per_page]},per_volume]}},1]},'volume':{'$add':[{'$floor':{'$divide':['$indexOrder',{'$multiply':[per_volume,per_page]}]}},1]}}},{'$unset': 'indexOrder'},{'$merge':{'into':mergeCol,'on':'_id','whenMatched':'merge','whenNotMatched':failOption}}];
  
        break;
      }
      try {
        await collection.aggregate(pipeline).toArray();
      } catch (error) {
        result = false
        console.error(error);
      }
      }


  return { result: result };
};