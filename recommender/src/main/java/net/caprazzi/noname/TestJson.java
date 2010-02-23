package net.caprazzi.noname;

import java.io.StringWriter;

import org.json.JSONArray;
import org.json.JSONException;
import org.json.JSONObject;
import org.json.JSONWriter;



public class TestJson {

	/**
	 * @param args
	 * @throws JSONException 
	 */
	public static void main(String[] args) throws JSONException {
		StringWriter stringWriter = new StringWriter();
		new JSONWriter(stringWriter)
			.object()
				.key("message_id")
				.value("xxxx")
				.key("body")
				.object()
					.key("web_query")
					.array().value("azzo").value("ozzo").endArray()
				.endObject()
			.endObject();
		
		String string = stringWriter.toString();
		System.out.println(string);
					
		Object object = JSONObject.stringToValue(string);
		
		JSONObject jsonObject = new JSONObject(string);
		String messageId = (String) jsonObject.get("message_id");
		JSONObject body = (JSONObject) jsonObject.get("body");
		JSONArray query = (JSONArray) body.get("web_query");
		String[] profiles = new String[query.length()];
		for(int i=0; i<query.length(); i++) {
			profiles[i] = query.getString(i);
			System.out.println(profiles[i]);
		}
		System.out.println(profiles);
			
		//JSONReader jsonReader = new JSONReader();
		//jsonReader.read("{}");
	}

}
