package net.caprazzi.noname;

import java.io.BufferedReader;
import java.io.IOException;
import java.io.StringReader;
import java.net.MalformedURLException;
import java.net.ProtocolException;

import uk.co.magus.fourstore.client.Store;

public class QueryResolver {

	private UserPrefService userPrefService;

	public void resolve(String messageId, String[] query) {
		//1. extract the domain for this profiles
		getDomain(query);
		
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
			while ((data = br.readLine()) != null) {
				//System.out.println("Print the contents from the file :" + data);
				if (firstLine) {
					firstLine = false;
					continue;
				} else {
					String[] splittArray = data.split("\\t");
					String user = splittArray[0];
					String item = splittArray[1];
				}
			}
		} catch (MalformedURLException e) {
			// TODO Auto-generated catch block
			e.printStackTrace();
		} catch (ProtocolException e) {
			// TODO Auto-generated catch block
			e.printStackTrace();
		} catch (IOException e) {
			// TODO Auto-generated catch block
			e.printStackTrace();
		}
		
	}

}
