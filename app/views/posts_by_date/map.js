function(doc) {
	// !code lib/utils.js
	if (doc.fetcher) {
		emit(doc.published, shorten(doc, 140));
	}
}