# youtube-captions-db

This server-app handle captions and elastic search over it. 
It has two end points: one for write a bunch of captions to DB and second for search over the whole index of them.
Search route is public: https://you-tickle.herokuapp.com/api/tickle/money . Money is a example key word for search. You can give it a shot!
Write route is private. You can reach it only with access token that only authed user can get.


Built on Flask
