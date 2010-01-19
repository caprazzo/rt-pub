function(doc, req) {  
	var len = req.max_len || 140;
	var body = '';
	
	function clean(str) {
		return str.replace(/shared by[^<]*</i,'<');
	}
	function trim(str) {
		return str.replace(/^\s+/,'').replace(/\s+$/,'').replace(/\s+/g,' ');
	}
	function add(str) {	
		if (body) body += ' ';
		body += trim(clean(str).replace(/<.*?>/g, '').slice(0, len));
		len -= body.length;
	}	

	if (doc.title)
		add(doc.title);
	
	if (doc.content && doc.content[0] && doc.content[0].value) {
		add(doc.content[0].value);
	}
	
	return toJSON({
		url: doc.link,
		body: body
	});
	
}