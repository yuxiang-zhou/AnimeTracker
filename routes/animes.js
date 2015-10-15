var express = require('express');
var router = express.Router();
var mongo = require('mongoskin');

/*
 * GET animelist.
 */
router.get('/animelist', function(req, res) {
    var db = req.db;
    db.collection('animelist').find().toArray(function (err, items) {
        res.json(items);
    });
});


/*
 * GET anime.
 */
router.get('/videos/:cate', function(req, res) {
    var db = req.db;
    db.collection('animes').find({"category":mongo.helper.toObjectID(req.params.cate)}).toArray(function (err, items) {
        res.json(items);
    });
});

module.exports = router;
