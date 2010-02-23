package net.caprazzi.noname;

public class QueryResolver {

	private UserPrefService userPrefService;

	public void resolve(String messageId, String[] query) {
		for (String ref : query) {
			userPrefService.getUserPrefNeighbour();
		}
	}

	public void setUserPrefService(UserPrefService userPrefService) {
		this.userPrefService = userPrefService;		
	}

}
