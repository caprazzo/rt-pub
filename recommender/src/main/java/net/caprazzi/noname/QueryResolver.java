package net.caprazzi.noname;

import java.io.BufferedReader;
import java.io.IOException;
import java.io.StringReader;
import java.net.MalformedURLException;
import java.net.ProtocolException;

import uk.co.magus.fourstore.client.Store;

public class QueryResolver {

	private UserPrefService userPrefService;

	public void resolve(String messageId, String[] profiles) {
		//1. extract the domain for this profiles
		//getDomain(profiles[0]);
		String query = "SELECT ?other_user ?any_item WHERE {" +
		    "<http://www.google.com/reader/shared/04542763409539038815> ?rel ?item ." +    
		    "?other_user ?any_rel ?item" +
		    "?other_user ?other_rel ?any_item" +
		"}";
		query.hashCode();
		//2. transpose refs and domain to numbers
		//3. ask recommender
		//4. put response on the channel
		
	}

	public void setUserPrefService(UserPrefService userPrefService) {
		this.userPrefService = userPrefService;		
	}
	
	void getDomain(String[] query) {
		Store store;
		
		try {
			store = new Store("http://localhost:8080");
			String response = store.query("", Store.OutputFormat.TAB_SEPARATED, 50000);
			BufferedReader br = new BufferedReader(new StringReader(response));
			String data = null;
			boolean firstLine = true;
			// skip header line, exit if empty
			if (br.readLine() == null) {
				return;
			}
			while ((data = br.readLine()) != null) {
				String[] splittArray = data.split("\\t");
				String user = splittArray[0];
				String item = splittArray[1];
			}
		} catch (Exception e) {
			throw new RuntimeException(e);
		}
		
	}

}
