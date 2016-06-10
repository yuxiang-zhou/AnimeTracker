var express = require('express');
var router = express.Router();
var mongo = require('mongoskin');
var db = mongo.db("mongodb://178.62.38.12:27017/animedb", {native_parser:true});


/*
 * GET animelist.
 */
router.get('/animelist', function(req, res) {
    db.collection('animes').find(
      {},{'title':1}
    ).sort({'title': 1}).toArray(function (err, items) {
        res.json(items);
    });
});


/*
 * GET anime.
 */
router.get('/anime/:id', function(req, res) {
    db.collection('animes').find({"_id":mongo.helper.toObjectID(req.params.id)}).toArray(function (err, items) {
        res.json(items[0]);
    });
});

module.exports = router;
