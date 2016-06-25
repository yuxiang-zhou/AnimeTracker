var express = require('express');
var router = express.Router();
var mongo = require('mongoskin');
var db = mongo.db("mongodb://178.62.38.12:27017/animedb", {native_parser:true});


/*
 * GET animelist.
 */
router.get('/animelist', function(req, res) {
  db.collection('animes').find(
    {},{'title':1, 'titles':1, 'timestamp':1}
  ).sort({'timestamp':1}).toArray(function (err, items) {
    items.reverse();
    res.json(items);
  });
});

router.get('/animelist/:from/:to', function(req, res) {
  db.collection('animes').find(
    {},{'title':1, 'titles':1, 'timestamp':1}
  ).sort({'timestamp':1}).skip(
    parseInt(req.params.from)
  ).limit(
    parseInt(req.params.to) - parseInt(req.params.from)
  ).toArray(function (err, items) {
    items.reverse();
    res.json(items);
  });
});

router.get('/animelistsize', function(req, res) {
  db.collection('animes').count({},function(err, count){
    res.json({'size':count});
  });
});

/*
 * GET anime.
 */
router.get('/anime/:id', function(req, res) {
  db.collection('animes').find(
    {"_id":mongo.helper.toObjectID(req.params.id)}
  ).toArray(function (err, items) {
    res.json(items[0]);
  });
});

router.get('/anime/search/:query', function(req, res) {
  db.collection('animes').find(
    {"$or": [
      {'title':{'$regex':'.*'+req.params.query+'.*'}},
      {'titles':{'$regex':'.*'+req.params.query+'.*'}}
    ]}
  ).toArray(function (err, items) {
    res.json(items);
  });
});

module.exports = router;
