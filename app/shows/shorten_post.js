function(doc, req) {  
	// !code lib/utils.js
	return toJSON(shorten(doc, req.max_len || 140));
	
}