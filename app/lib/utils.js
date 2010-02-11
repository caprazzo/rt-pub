function shorten(doc, max_len) {
	var len = max_len || 140;
	var body = '';
	
	function clean(str) {
		return str.replace(/shared by[^<]*</i,'<');
	}
	function trim(str) {
		return str.replace(/^\s+/,'').replace(/\s+$/,'').replace(/\s+/g,' ');
	}
	function add(str) {	
		if (len <= 0)
			return 0;
		if (body) body += ' ';
		body += trim(clean(str).replace(/<.*?>/g, '').slice(0, len));
		return len - body.length;
	}	


	if (doc.title) {
		len = add(doc.title, len);
	}
	
	if (doc.subtitle) {
		len = add(doc.subtitle, len);
	}
	
	if (doc.content && doc.content[0] && doc.content[0].value) {
		len = add(doc.content[0].value, len);
	}
	
	if (doc.summary) {
		add(doc.summary, len);
	}
	
	return {
		url: doc.link,
		body: body
	};
}