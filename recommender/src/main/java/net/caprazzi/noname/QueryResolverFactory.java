package net.caprazzi.noname;

public class QueryResolverFactory {

	public QueryResolver createResolver() {
		QueryResolver resolver = new QueryResolver();
		UserPrefService userPrefService = new UserPrefService();
		resolver.setUserPrefService(userPrefService);
		return resolver;
	}

}
