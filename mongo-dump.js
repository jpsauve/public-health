// mongoexport --db radar-lcartaxox --collection temp --out jp-30-days.json --fields PostID,LocationKey,Post,TimeStamp
use radar-lcartaxox
db.temp.drop()
var start = '2015-09-12T03:00:00.000Z'
var end = '2015-10-13T03:00:00.000Z'
db.posts.find({
    Source:'Twitter', 
    $and: [{TimeStamp:{$gte: ISODate(start)}}, {TimeStamp:{$lte: ISODate(end)}}],
    FilteredOut: false, 
    $or: [{Removed: false}, {Removed: {$exists: false}}]
}).forEach(function (p) {
    p.Post = p.Post.replace(/[\r\n]/g, " ");
    p.Repeticao = p.RepGroup ? p.RepGroup.length : 0
    db.temp.insert(p)
    // print('id', p._id)
    // print('PostID', p.PostID)
    // print('Post', p.Post)
    // print('LocationKey', p.LocationKey)
    // print('TimeStamp', p.TimeStamp)
})
